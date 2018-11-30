import os
import logging

from .container_test import ContainerTests

logger = logging.getLogger(name=__file__)


def test_open_ldap(open_ldap_server, dockerfile):
    with ContainerTests('open-ldap', dockerfile=dockerfile, image_tag='external-auth-test') as ct:
        ct.start_test('setup',
                      'pytest --junit-xml /results/open-ldap-setup-{}.xml -m "setup and open_ldap" /tests'.format(ct.start_time),
                      network='{}_default'.format(open_ldap_server.name),
                      volumes={os.path.dirname(__file__): {'bind': '/tests', 'mode': 'rw'}})
