import pytest
import yaml


@pytest.mark.master
@pytest.mark.worker
@pytest.mark.bsc1121146
def test_auth_is_disabled(host):
    config = host.file("/etc/kubernetes/kubelet-config.yaml").content_string
    config = yaml.load(config)

    assert config["authentication"]["anonymous"]["enabled"] == False


@pytest.mark.master
@pytest.mark.worker
@pytest.mark.bsc1123650
def test_exp_critical_pod_is_enabled(host):
    config = host.file("/etc/kubernetes/kubelet-config.yaml").content_string
    config = yaml.load(config)

    assert config["featureGates"]["ExperimentalCriticalPodAnnotation"] == True


@pytest.mark.master
@pytest.mark.worker
@pytest.mark.bsc1117942
def test_volume_dir_configured(host):
    config = host.file("/etc/kubernetes/kubelet").content_string

    assert "--volume-plugin-dir=/var/lib/kubelet/plugins" in config


@pytest.mark.admin
@pytest.mark.bsc1121145
def test_server_is_disabled(host):
    config = host.file("/etc/kubernetes/kubelet").content_string

    assert "--enable-server=false" in config


@pytest.mark.admin
@pytest.mark.bsc1121145
def test_healthz_is_disabled(host):
    config = host.file("/etc/kubernetes/kubelet").content_string

    assert "--healthz-port=0" in config
