import pytest


@pytest.mark.common
def test_apiserver_is_running(host):
    assert host.service("kube-apiserver").is_running
