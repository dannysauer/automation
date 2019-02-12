# Add log rotation options to docker daemon (bug#1114832)
# https://github.com/kubic-project/salt/pull/683
# https://github.com/kubic-project/salt/pull/692 (backport)

import pytest
import json


@pytest.mark.common
def test_file_daemon_json_exists(host):
    assert host.file("/etc/daemon.json").is_file


@pytest.mark.common
def test_file_daemon_json_content(host):
    config = host.file("/etc/daemon.json").content_string
    config = json.loads(config)

    assert config["log-level"]
    # the next two ones are introduced by the PR
    assert config["log-driver"]
    assert config["log-opts"]


@pytest.mark.common
def test_docker_is_started(host):
    assert host.service("docker").is_running
