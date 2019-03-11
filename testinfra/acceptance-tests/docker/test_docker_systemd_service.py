import pytest


@pytest.mark.common
def test_docker_is_running(host):
    assert host.service("docker").is_running
