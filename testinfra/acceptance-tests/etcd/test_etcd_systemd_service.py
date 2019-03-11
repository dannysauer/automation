import pytest
import json


@pytest.mark.master
def test_etcd_is_running(host):
    assert host.service("etcd").is_running


@pytest.mark.master
def test_etcd_is_healthy(host):
    etcd_health = host.run("curl -kL --capath /etc/pki --cacert /etc/pki/trust/anchors/SUSE_CaaSP_CA.crt --cert /etc/pki/kubelet.crt --key /etc/pki/kubelet.key https://localhost:2379/health").stdout
    etcd_heatlh_json = json.loads(etcd_health)

    assert etcd_heatlh_json["health"] == "true"
