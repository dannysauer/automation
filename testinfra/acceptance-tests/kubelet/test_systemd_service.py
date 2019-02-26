import pytest


@pytest.mark.common
def test_kubelet_is_running(host):
    assert host.service("kubelet").is_running
