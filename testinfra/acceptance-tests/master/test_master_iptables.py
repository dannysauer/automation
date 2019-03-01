import pytest


@pytest.mark.master
@pytest.mark.bsc1121144
def test_iptables_0_0_6444_accept_disabled(host):
    input_rules = host.iptables.rules('filter', 'INPUT')
    rule = "-A INPUT -p tcp -m state --state NEW -m tcp --dport 6444 -j ACCEPT"

    assert rule not in input_rules


@pytest.mark.master
@pytest.mark.bsc1121144
def test_iptables_localhost_6444_accept_enabled(host):
    input_rules = host.iptables.rules('filter', 'INPUT')
    rule = "-A INPUT -s 127.0.0.1/32 -p tcp -m state --state NEW -m tcp --dport 6444 -j ACCEPT"

    assert rule in input_rules


@pytest.mark.master
@pytest.mark.bsc1121144
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
@pytest.mark.bsc1121144
def test_iptables_pod_subnet_6444_accept_enabled(host):
    input_rules = host.iptables.rules('filter', 'INPUT')
    rule = "-A INPUT -s 172.16.0.0/13 -p tcp -m state --state NEW -m tcp --dport 6444 -j ACCEPT"

    assert rule in input_rules


@pytest.mark.master
@pytest.mark.bsc1121144
def test_iptables_0_0_6444_drop_enabled(host):
    input_rules = host.iptables.rules('filter', 'INPUT')
    rule = "-A INPUT -p tcp -m state --state NEW -m tcp --dport 6444 -j DROP"

    assert rule in input_rules
