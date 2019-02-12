# [3.0] Disable anonymous access to Kubelet API (bsc#1121146)
# https://github.com/SUSE/kubic-salt-security-fixes/pull/4
# https://github.com/SUSE/kubic-salt-security-fixes/pull/2 (backport)

import pytest
import yaml


@pytest.mark.master
@pytest.mark.worker
def test_auth_is_disabled_in_kubelet_config_file(host):
    config = host.file("/etc/kubernetes/kubelet-config.yaml").content_string
    config = yaml.load(config)

    assert config["authentication"]["anonymous"]["enabled"] == False


@pytest.mark.master
def test_cert_config_in_apiserver_config(host):
    config = host.file("/etc/kubernetes/apiserver").content_string

    assert "--kubelet-certificate-authority=/etc/pki/trust/anchors/SUSE_CaaSP_CA.crt" in config
    assert "--kubelet-client-certificate=/etc/pki/kube-apiserver-kubelet-client.crt" in config
    assert "--kubelet-client-key=/etc/pki/kube-apiserver-kubelet-client.key" in config


@pytest.mark.master
@pytest.mark.parametrize("service", [
    "kube-apiserver",
    "kube-controller-manager",
    "kube-scheduler",
    "kubelet",
    "kube-proxy"
])
def test_services_running_masters(host, service):
    host_service = host.service(service)
    assert host_service.is_running


@pytest.mark.worker
@pytest.mark.parametrize("service", [
    "kubelet",
    "kube-proxy"
])
def test_services_running_workers(host, service):
    host_service = host.service(service)
    assert host_service.is_running
