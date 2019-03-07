import pytest


@pytest.mark.master
@pytest.mark.bsc1121146
@pytest.mark.parametrize("option", [
    "--kubelet-certificate-authority=/etc/pki/trust/anchors/SUSE_CaaSP_CA.crt",
    "--kubelet-client-certificate=/etc/pki/kube-apiserver-kubelet-client.crt",
    "--kubelet-client-key=/etc/pki/kube-apiserver-kubelet-client.key"])
def test_certs_are_configured(host, option):
    config = host.file("/etc/kubernetes/apiserver").content_string

    assert option in config


@pytest.mark.master
@pytest.mark.bsc1121148
@pytest.mark.parametrize("option", [
    "--insecure-bind-address=127.0.0.1",
    "--insecure-port=0"])
def test_insecure_api_is_disabled(host, option):
    config = host.file("/etc/kubernetes/apiserver").content_string

    assert option in config
