# [bsc#1121145] Disable the kubelet servers on the admin node.
# https://github.com/SUSE/kubic-caasp-container-manifests-security-fixes/pull/2
# https://github.com/SUSE/kubic-caasp-container-manifests-security-fixes/pull/6 (Backport)

import pytest


@pytest.mark.admin
def test_server_is_disabled_in_kubelet_config(host):
    config = host.file("/etc/kubernetes/kubelet").content_string

    assert "--enable-server=false" in config


@pytest.mark.admin
def test_healthz_is_disabled_in_kubelet_config(host):
    config = host.file("/etc/kubernetes/kubelet").content_string

    assert "--healthz-port=0" in config


@pytest.mark.admin
def test_kubelet_is_running(host):
    assert host.service("kubelet").is_running
