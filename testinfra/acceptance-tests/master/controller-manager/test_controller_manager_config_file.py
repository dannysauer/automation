import pytest


@pytest.mark.master
@pytest.mark.bsc1117942
def test_flexvolume_is_configured(host):
    config = host.file("/etc/kubernetes/controller-manager").content_string

    assert "--flex-volume-plugin-dir=/var/lib/kubelet/plugins" in config
