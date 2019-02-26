import pytest


@pytest.mark.master
@pytest.mark.bsc1121148
def test_insecure_api_is_disabled(host):
    request = host.run("curl http://localhost:8080/version").stderr

    assert "Connection refused" in request
