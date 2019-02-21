# Use a writable directory for volume plugins (bsc#1117942)
# https://github.com/kubic-project/salt/pull/724
# https://github.com/SUSE/kubic-salt-security-fixes/pull/23 (backport)

import pytest


@pytest.mark.master
def test_flexvolume_is_configured_in_controller_manager_config(host):
    config = host.file("/etc/kubernetes/controller-manager").content_string

    assert "--flex-volume-plugin-dir=/var/lib/kubelet/plugins" in config


@pytest.mark.master
def test_controller_manager_is_running(host):
    assert host.service("kube-controller-manager").is_running


@pytest.mark.master
@pytest.mark.worker
def test_volume_dir_configured_in_kubelet_configu(host):
    config = host.file("/etc/kubernetes/kubelet").content_string

    assert "--volume-plugin-dir=/var/lib/kubelet/plugins" in config


@pytest.mark.master
@pytest.mark.worker
@pytest.mark.parametrize("service", [
    "kubelet",
    "kube-proxy"
])
def test_services_running(host, service):
    host_service = host.service(service)
    assert host.service.is_running
