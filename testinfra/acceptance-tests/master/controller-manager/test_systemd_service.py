import pytest


@pytest.mark.common
def test_controller_manager_is_running(host):
    assert host.service("kube-controller-manager").is_running
