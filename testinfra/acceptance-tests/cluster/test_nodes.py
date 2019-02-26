import pytest


@pytest.mark.master
def test_all_nodes_are_ready(host):
    non_ready_nodes = host.run("kubectl get nodes --no-headers | grep -v 'Ready'")

    assert non_ready_nodes.rc == 1
