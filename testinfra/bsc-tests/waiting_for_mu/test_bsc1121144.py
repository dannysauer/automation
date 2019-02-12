# Limit access to KUBE-APISERVER port 6444 on master nodes, bsc#1121144
# https://github.com/SUSE/kubic-salt-security-fixes/pull/11
# https://github.com/SUSE/kubic-salt-security-fixes/pull/14 (backport)

import pytest


@pytest.mark.master
def test_iptables_0_0_6444_accept_disabled(host):
    input_rules = host.iptables.rules('filter', 'INPUT')
    rule = "-A INPUT -p tcp -m state --state NEW -m tcp --dport 6444 -j ACCEPT"

    assert rule not in input_rules


@pytest.mark.master
def test_iptables_localhost_6444_accept_enabled(host):
    input_rules = host.iptables.rules('filter', 'INPUT')
    rule = "-A INPUT -s 127.0.0.1/32 -p tcp -m state --state NEW -m tcp --dport 6444 -j ACCEPT"

    assert rule in input_rules


@pytest.mark.master
def test_iptables_host_net_6444_accept_enabled(host):
    input_rules = host.iptables.rules('filter', 'INPUT')

    host_ip = host.run("ip -f inet -o address show dev eth0 | awk '{ print $4 }' | sed 's/\/.*//'").stdout
    host_ip = host_ip.strip('\n')

    host_network = host.run("ip -f inet route list | grep {0} | awk '{{ print $1 }}'".format(host_ip)).stdout
    host_network = host_network.strip('\n')

    rule = "-A INPUT -s {0} -p tcp -m state --state NEW -m tcp --dport 6444 -j ACCEPT".format(
            host_network)

    assert rule in input_rules


@pytest.mark.master
def test_iptables_pod_subnet_6444_accept_enabled(host):
    input_rules = host.iptables.rules('filter', 'INPUT')
    rule = "-A INPUT -s 172.16.0.0/13 -p tcp -m state --state NEW -m tcp --dport 6444 -j ACCEPT"

    assert rule in input_rules


@pytest.mark.master
def test_iptables_0_0_6444_drop_enabled(host):
    input_rules = host.iptables.rules('filter', 'INPUT')
    rule = "-A INPUT -p tcp -m state --state NEW -m tcp --dport 6444 -j DROP"

    assert rule in input_rules


@pytest.mark.master
def test_pods_in_kubesystem_ns_are_ready(host):
    non_running_pods = host.run("kubectl -n kube-system get po --no-headers | grep -v 'Running'")

    assert non_running_pods.rc == 1


@pytest.mark.master
def test_all_nodes_are_ready(host):
    non_ready_nodes = host.run("kubectl get nodes --no-headers | grep -v 'Ready'")

    assert non_ready_nodes.rc == 1
