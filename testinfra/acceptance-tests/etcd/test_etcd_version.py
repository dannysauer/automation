import pytest


@pytest.mark.bsc1121850
@pytest.mark.common
@pytest.mark.parametrize("package", ["etcd", "etcdctl"])
@pytest.mark.parametrize("min_version", ["3.3.11"])
def test_etcd_packages_version_is_superior_to_3_3_11(host, package, min_version):
    etcd = host.package(package)

    host_version = etcd.version.split("-")[0].split(".")
    host_major = int(host_version[0])
    host_minor = int(host_version[1])
    host_patch = int(host_version[2])

    min_major = int(min_version.split(".")[0])
    min_minor = int(min_version.split(".")[1])
    min_patch = int(min_version.split(".")[2])

    assert host_major >= min_major

    if host_major == min_major:
        assert host_minor >= min_minor

        if host_minor == min_minor:
            assert host_patch >= min_patch
