import logging
import subprocess
import tarfile
import os

import docker
import pytest

logging.basicConfig()
logger = logging.getLogger(name=__file__)


def pytest_addoption(parser):
    parser.addoption('--dockerfile',
                     action='store',
                     default=os.path.join(os.path.dirname(__file__), 'Dockerfile'),
                     help='Path to the Dockerfile to run the test in.')


@pytest.fixture(scope='session')
def dockerfile(request):
    return request.config.getoption('--dockerfile')


@pytest.yield_fixture(scope='session')
def open_ldap_server():

    compose_file = os.path.join(os.path.dirname(__file__), 'ldap_tests/open-ldap-server/docker-compose.yml')

    build_output = subprocess.check_output(['docker-compose', '-f', compose_file, 'build'])

    logger.info(build_output)

    run_output = subprocess.check_output(['docker-compose', '-f', compose_file, 'up', '-d'])

    logger.info(run_output)

    client = docker.from_env()

    yield client.containers.get('open-ldap-server')

    subprocess.check_call(['docker-compose', '-f', compose_file, 'down', '-v'])


@pytest.yield_fixture(scope='session')
def open_ldap_certificate(open_ldap_server):
    tar_stream = open_ldap_server.get_archive('/container/service/:ssl-tools/assets/default-ca/')[0]

    with open('open-ldap-certs.tar', mode='wb') as f:
        for chunk in tar_stream:
            f.write(chunk)

    open_ldap_certs_tar = tarfile.open('open-ldap-certs.tar')

    print(open_ldap_certs_tar.list())

    with open('open-ldap-certs/ldap.crt', mode='wb') as f:
        f.write(open_ldap_certs_tar.extractfile('default-ca/default-ca.pem').read())

    with open('open-ldap-certs/ca.pem', mode='wb') as f:
        f.write(open_ldap_certs_tar.extractfile('default-ca/default-ca.pem').read())

    with open('open-ldap-certs/ldap.key', mode='wb') as f:
        f.write(open_ldap_certs_tar.extractfile('default-ca/default-ca-key.pem').read())

    os.remove('open-ldap-certs.tar')

    yield {'ca': os.path.join(os.path.dirname(__file__), 'open-ldap-certs/ca.pem'),
           'cert': os.path.join(os.path.dirname(__file__), 'open-ldap-certs/ldap.crt'),
           'key': os.path.join(os.path.dirname(__file__), 'open-ldap-certs/ldap.key')}
