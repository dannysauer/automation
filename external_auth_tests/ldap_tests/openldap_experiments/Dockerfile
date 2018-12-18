FROM opensuse/leap:15.0
# enable repo w/ geckodriver
RUN zypper addrepo -f --check https://download.opensuse.org/repositories/openSUSE:/infrastructure:/software.opensuse.org/openSUSE_Leap_15.0/openSUSE:infrastructure:software.opensuse.org.repo
RUN zypper --gpg-auto-import-keys ref

# install necessary SUSE packages
RUN zypper --no-refresh install -y \
    python3-selenium \
    chromedriver \
    geckodriver
#chromium \
# install any other python modules?
RUN zypper --no-refresh install -y \
    python3-kubernetes

ENTRYPOINT /bin/bash
