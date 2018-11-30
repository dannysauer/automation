import logging
import subprocess
import tarfile
import os
import uuid

import docker
import pytest
import testinfra

logging.basicConfig()
logger = logging.getLogger(name=__file__)


# @pytest.fixture(scope='session')
# def host(request):
#     client = docker.from_env()
#     image_tag = 'external-auth-test-{}'.format(uuid.uuid4())
#
#     # build the image
#     client.images.build(path='.', tag=image_tag)
#
#     # start the container
#     external_auth_test_container = client.containers.run(image_tag, detach=True)
#
#     # return a testinfra connection to the container
#     yield testinfra.get_host('docker://{}'.format(external_auth_test_container.id))
#
#     # at the end of the test suite, destroy the container
#     external_auth_test_container.remove(v=True, force=True)
#     # remove the image
#     client.images.remove(image_tag)


@pytest.yield_fixture(scope='session')
def open_ldap_server():
    subprocess.check_call(['docker-compose', '-f', 'open-ldap-server/docker-compose.yml', 'up', '--build', '-d'])

    client = docker.from_env()

    yield client.containers.get('openldap')

    subprocess.check_call(['docker-compose', '-f', 'open-ldap-server/docker-compose.yml', 'down', '-v'])


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
