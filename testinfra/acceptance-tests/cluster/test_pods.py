import pytest


@pytest.mark.master
def test_pods_in_kubesystem_ns_are_ready(host):
    non_running_pods = host.run("kubectl -n kube-system get po --no-headers | grep -v 'Running'")

    assert non_running_pods.rc == 1
