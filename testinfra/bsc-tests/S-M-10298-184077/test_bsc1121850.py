import pytest
import json


@pytest.mark.common
@pytest.mark.parametrize("package", ["etcd", "etcdctl"])
def test_etcd_packages_version_is_superior_to_3_3_11(host, package):
    etcd = host.package(package)
    version = etcd.version.split("-")[0].split(".")

    major = int(version[0])
    minor = int(version[1])
    patch = int(version[2])

    assert major >= 3

    if major == 3:
        assert minor >= 3

        if minor == 3:
            assert patch >= 11


@pytest.mark.master
def test_etcd_is_running(host):
    assert host.service("etcd").is_running


@pytest.mark.master
def test_etcd_is_healthy(host):
    etcd_health = host.run("curl -kL --capath /etc/pki --cacert /etc/pki/trust/anchors/SUSE_CaaSP_CA.crt --cert /etc/pki/kubelet.crt --key /etc/pki/kubelet.key https://localhost:2379/health").stdout
    etcd_heatlh_json = json.loads(etcd_health)

    assert etcd_heatlh_json["health"] == "true"
