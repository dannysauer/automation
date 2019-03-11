import pytest


@pytest.mark.admin
@pytest.mark.bsc1121163
def test_velum_user_permissions_in_setup_for_mariadb(host):
    path = "/usr/share/caasp-container-manifests/setup/mysql/setup-mysql.sh"
    config = host.file(path).content_string

    old_priv = "GRANT ALL PRIVILEGES ON velum_$ENV.* TO velum@localhost;"
    new_priv = "GRANT CREATE,DROP,ALTER,SELECT,INSERT,DELETE,UPDATE,INDEX ON velum_$ENV.* TO velum@localhost;"

    assert old_priv not in config
    assert new_priv in config


@pytest.mark.admin
@pytest.mark.bsc1121163
def test_velum_user_permission_in_mariadb(host):
    # The privileges are slightly formatted differently
    # from the setup.sh file and from the mysql outputs
    old_priv = "GRANT ALL PRIVILEGES ON `velum_production`.* TO 'velum'@'localhost'"
    new_priv = "GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON `velum_production`.* TO 'velum'@'localhost'"

    cmd = "docker exec $(docker ps -q --filter name=velum-mariadb) mysql -p$(cat /var/lib/misc/infra-secrets/mariadb-root-password) -e \"SHOW GRANTS FOR velum@localhost\""

    velum_current_priv = host.run(cmd).stdout

    assert old_priv not in velum_current_priv
    assert new_priv in velum_current_priv
