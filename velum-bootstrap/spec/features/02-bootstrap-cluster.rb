require "spec_helper"
require "yaml"

feature "Boostrap cluster" do
  let(:hostnames) { environment["minions"].map { |m| m["fqdn"] if m["role"] != "admin" }.compact }
  let(:minion_ids) { environment["minions"].map { |m| m["minionId"] }.compact }

  before do
    login unless inspect.include? "User registers"
  end

  # Using append after in place of after, as recommended by
  # https://github.com/mattheworiordan/capybara-screenshot#common-problems
  append_after do
    Capybara.reset_sessions!
  end

  # User registration and cluster configuration has already been done in 01-setup-velum.rb
  # After login we simply press Next to reach the minion discovery page
  scenario "User reaches minion discovery page" do
    with_screenshot(name: :view_setup_page) do
      with_status_ok do
        visit "/setup"
      end
    end
    puts ">>> Reaching discovery page"
    click_on "Next"
    puts "<<< Ready to start discovery"
  end

  scenario "User accepts all minions" do
    with_status_ok do
      visit "/setup/discovery"
    end

    puts ">>> Wait until all #{node_number} minions are pending to be accepted"
    with_screenshot(name: :pending_minions) do
      expect(page).to have_selector("a", text: "Accept", count: node_number, wait: 400)
    end
    puts "<<< All minions are pending to be accepted"

    puts ">>> Wait for accept-all button to be enabled"
    with_screenshot(name: :accept_button_enabled) do
      expect(page).to have_button("accept-all", disabled: false, wait: 20)
    end
    puts "<<< accept-all button enabled"

    puts ">>> Click to accept all minion keys"
    with_screenshot(name: :accept_button_click) do
      click_button("accept-all")
    end

    with_status_ok do
      visit "/setup/discovery"
    end

    # Min of 240 seconds, Max of 600 seconds, ideal = nodes * 30
    accept_timeout = [[240, node_number * 30].max, 600].min
    puts ">>> Wait until Minion keys are accepted by salt (Timeout: #{accept_timeout})"
    with_screenshot(name: :accepted_keys) do
      expect(page).to have_css(".master-btn", count: node_number, wait: accept_timeout)
    end
    puts "<<< Minion keys accepted in Velum"

    puts ">>> Waiting until Minions are accepted in Velum"
    with_screenshot(name: :accepted_minions) do
      expect(page).to have_text("#{node_number} nodes found", wait: 60)
    end
    puts "<<< Minions accepted in Velum"

    # They should also appear in the UI
    hostnames.each do |hostname|
      # Case-insensitive hostname matching
      expect(page.body.downcase).to have_content(hostname.downcase)
    end
  end

  scenario "User selects minion roles" do
    with_status_ok do
      visit "/setup/discovery"
    end

    puts ">>> Waiting for page to settle"
    with_screenshot(name: :wait_for_settle) do
      expect(page).to have_text("You currently have no nodes to be accepted for bootstrapping",
               wait: 240)
    end
    puts "<<< Page has settled"

    puts ">>> Selecting minion roles"
    with_screenshot(name: :select_minion_roles) do
      environment["minions"].each do |minion|
        next unless %w[master worker].include?(minion["role"])
        within("tr", text: minion["minionId"]) do
          find(".#{minion["role"]}-btn").click
        end
      end
    end
    puts "<<< Minion roles selected"

    puts ">>> Confirm roles selection"
    with_screenshot(name: :roles_selection) do
      click_button("set-roles")
    end

    if node_number < 3
      # a modal with a warning will appear as we only have #{node_number} nodes
      with_screenshot(name: :cluster_too_small) do
        expect(page).to have_content("Cluster is too small")
        click_button "Proceed anyway"
      end
    end
  end

  scenario "User bootstraps the cluster" do
    with_status_ok do
      visit "/setup/bootstrap"
    end

    puts ">>> Configuring last settings"
    with_screenshot(name: :bootstrap_cluster_settings) do
      fill_in "settings_apiserver", with: environment["kubernetesExternalHost"]
      fill_in "settings_dashboard_external_fqdn", with: environment["dashboardExternalHost"]
    end
    puts "<<< Last settings configured"

    puts ">>> Bootstrapping cluster"
    with_screenshot(name: :bootstrap_cluster) do
      expect(page).to have_button(value: "Bootstrap cluster", disabled: false)
      click_on "Bootstrap cluster"
    end

    # Min of 3600 seconds, Max of 7200 seconds, ideal = nodes * 120 seconds
    orchestration_timeout = [[3600, node_number * 120].max, 7200].min
    puts ">>> Wait until orchestration is complete (Timeout: #{orchestration_timeout})"
    with_screenshot(name: :orchestration_complete) do
      within(".nodes-container") do
        expect(page).to have_css(".fa-check-circle-o, .fa-times-circle",
         count: node_number, wait: orchestration_timeout)
      end
    end
    puts "<<< Orchestration completed"

    puts ">>> Checking if orchestration succeeded"
    with_screenshot(name: :orchestration_succeeded) do
      within(".nodes-container") do
        expect(page).to have_css(".fa-check-circle-o", count: node_number, wait: 5)
      end
    end
    puts "<<< Orchestration succeeded"

    minion_ids.each do |id|
      environment(
        action: :update,
        body:   set_minion_status(id, "bootstrapped")
      )
    end
  end
end
