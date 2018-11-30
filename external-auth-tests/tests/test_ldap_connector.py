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
import docker
import pytest


@pytest.mark.ldap_connector
class TestLdapConnector:

    @pytest.fixture(scope='class')
    def velum_container(self):
        client = docker.from_env()
        containers = client.list(filters={'name': 'velum-dashboard'})

        return containers[0]

    def test_velum_feature(self, velum_container):
        results = velum_container.exec_run('entrypoint.sh bash -c "RAILS_ENV=test '
                                           'bundle exec rspec spec/features/dex_connector_ldap_feature_spec.rb"')

        with open('results/velum_container.log', 'w') as f:
            f.write(results[1])

        assert results[0] == 0

        with open('results/rspec_results.tar', 'wb') as f:
            stream = velum_container.get_archive('/srv/velum/public/coverage')
            for chunk in stream:
                f.write(chunk)
