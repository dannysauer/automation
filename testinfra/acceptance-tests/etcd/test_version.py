import pytest


@pytest.mark.bsc1121850
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
