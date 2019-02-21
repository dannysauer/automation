# [3.0] Disable insecure port in kube-apiserver (bsc#1121148)
# https://github.com/SUSE/kubic-salt-security-fixes/pull/9
# https://github.com/SUSE/kubic-salt-security-fixes/pull/10 (backport)

import pytest


@pytest.mark.master
def test_insecure_api_is_disabled_in_apiserver_config(host):
    config = host.file("/etc/kubernetes/apiserver").content_string

    assert "--insecure-bind-address=127.0.0.1" not in config
    assert "--insecure-port=0" in config


@pytest.mark.master
def test_apiserver_service_is_running(host):
    assert host.service("kube-apiserver").is_running


@pytest.mark.master
def test_insecure_api_is_disabled(host):
    request = host.run("curl http://localhost:8080/version").stderr

    assert "Connection refused" in request
