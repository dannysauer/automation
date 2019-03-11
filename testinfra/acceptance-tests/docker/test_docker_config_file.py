import pytest
import json


@pytest.mark.common
@pytest.mark.bsc1114832
def test_file_daemon_json_exists(host):
    assert host.file("/etc/docker/daemon.json").is_file


@pytest.mark.common
@pytest.mark.bsc1114832
def test_file_daemon_json_content(host):
    config = host.file("/etc/docker/daemon.json").content_string
    config = json.loads(config)

    assert config["log-level"]
    assert config["log-driver"]
    assert config["log-opts"]
