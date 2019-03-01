import pytest


@pytest.mark.master
@pytest.mark.bsc1121146
def test_certs_are_configured(host):
    config = host.file("/etc/kubernetes/apiserver").content_string

    assert "--kubelet-certificate-authority=/etc/pki/trust/anchors/SUSE_CaaSP_CA.crt" in config
    assert "--kubelet-client-certificate=/etc/pki/kube-apiserver-kubelet-client.crt" in config
    assert "--kubelet-client-key=/etc/pki/kube-apiserver-kubelet-client.key" in config


@pytest.mark.master
@pytest.mark.bsc1121148
def test_insecure_api_is_disabled(host):
    config = host.file("/etc/kubernetes/apiserver").content_string

    assert "--insecure-bind-address=127.0.0.1" not in config
    assert "--insecure-port=0" in config
