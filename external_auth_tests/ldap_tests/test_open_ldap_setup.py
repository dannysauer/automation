# Copyright 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging

import pytest

from time import sleep

from ldap3 import (Server, Connection, ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES)
from ldap3.core.exceptions import LDAPException

logger = logging.getLogger(name=__file__)


@pytest.mark.open_ldap
@pytest.mark.setup
class TestOpenLdapSetup:

    @pytest.fixture()
    def host(self):
        return 'ldaptest.com'

    @pytest.fixture()
    def base_dn(self):
        return 'dc=ldaptest,dc=com'

    @pytest.yield_fixture()
    def ldap_conn(self, host, base_dn):
        timeout = 30

        server = Server(host, get_info=ALL, use_ssl=True)
        conn = Connection(server, user='cn=admin,{}'.format(base_dn), password='admin', raise_exceptions=True)

        while not conn.bound and timeout > 0:
            try:
                conn.bind()
            except LDAPException as err:
                logger.warning(err)
            finally:
                timeout -= 1
                sleep(1)

        yield conn

        conn.unbind()

    def test_ldap_server_up(self, ldap_conn):
        assert ldap_conn.bound

    def test_ldap_server_simple_tls(self, ldap_conn, base_dn):
        assert ldap_conn.bound

        ldap_conn.search(base_dn,
                         '(&(objectclass=person)(cn=test))',
                         attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])

        assert ldap_conn.entries

    def test_ldap_anon(self, host, base_dn):
        with Connection(host) as conn:
            assert conn.bound

            conn.search(base_dn,
                        '(&(objectclass=person)(cn=test))',
                        attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])

            assert conn.entries

    def test_ldap_start_tls(self, host, base_dn):
        server = Server(host, get_info=ALL)
        conn = Connection(server, user='cn=admin,{}'.format(base_dn), password='admin', raise_exceptions=True)
        conn.bind()

        assert conn.bound

        conn.start_tls()

        assert conn.tls_started

        conn.unbind()

