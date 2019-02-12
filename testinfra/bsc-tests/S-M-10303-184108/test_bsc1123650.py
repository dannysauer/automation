# [3.0] Enable `ExperimentalCriticalPodAnnotation`
# feature gate in the kubelet
# https://github.com/kubic-project/salt/pull/682 (backport)

import pytest
import yaml

@pytest.mark.master
@pytest.mark.worker
def test_exp_critical_pod_is_enabled_in_kubelet_config_file(host):
    config = host.file("/etc/kubernetes/kubelet-config.yaml").content_string
    config = yaml.load(config)

    assert config["featureGates"]["ExperimentalCriticalPodAnnotation"] == True


@pytest.mark.master
@pytest.mark.worker
def test_kubelet_is_running(host):
    assert host.service("kubelet").is_running
