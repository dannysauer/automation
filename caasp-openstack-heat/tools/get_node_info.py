#!/usr/bin/env python3

import json
import os
import subprocess
import sys


def _openstack(args):
    proc = subprocess.run('openstack {} -f json'.format(args),
                          encoding='utf-8',
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    if proc.returncode != 0:
        print(proc.stderr)
        sys.exit(proc.returncode)

    return json.loads(proc.stdout)


def get_server_info(node_id, node_role, node_index=None):
    print('Building {} Details: {}'.format(node_role.capitalize(), node_id))
    response = _openstack('server show {}'.format(node_id))
    ipv4s = response['addresses'].split(', ')
    private_ipv4 = ipv4s[0].split('=')[1]

    node_info = {'role': node_role,
                 'fqdn': response['name'],
                 'addresses': {'privateIpv4': private_ipv4},
                 'index': node_index,
                 'minionId': response['id'].replace('-', ''),
                 'status': "unused"}

    if len(ipv4s) > 1:
        node_info['addresses']['publicIpv4'] = ipv4s[1]

    return node_info


def build_master_info(environment, masters):
    lb_public_ipv4 = None
    is_multi_master = len(masters) > 1

    if is_multi_master:
        master_lb_floating_ip = _openstack('stack resource show {} master_lb_floating_ip'.format(stack_name))
        lb_public_ipv4 = master_lb_floating_ip['attributes']['floating_ip_address']

    for master in masters:
        master['index'] = len(environment['minions'])
        if lb_public_ipv4:
            master['addresses']['publicIpv4'] = lb_public_ipv4

        environment['minions'].append(master)


def build_worker_info(environment, workers):
    for worker in workers:
        worker['index'] = len(environment['minions'])
        worker['proxyCommand'] = 'ssh -i {} ' \
                                 '-o UserKnownHostsFile=/dev/null ' \
                                 '-o StrictHostKeyChecking=no ' \
                                 'root@{} -W %h:%p'.format(environment["sshKey"], admin["addresses"]["publicIpv4"])
        environment['minions'].append(worker)


if __name__ == '__main__':
    admin = None
    masters = []
    workers = []
    stack_name = sys.argv[1]
    environment = {'sshUser': 'root',
                   'sshKey': os.path.normpath(os.path.join(os.getcwd(), '../misc-files/id_shared'))}

    for server in _openstack('stack resource list --filter type="OS::Nova::Server" -n 10 {}'.format(stack_name)):
        if '-worker-' in server['stack_name']:
            workers.append(get_server_info(server['physical_resource_id'], 'worker'))
        elif server['resource_name'] in ['master', 'master_server']:
            masters.append(get_server_info(server['physical_resource_id'], 'master'))
        elif server['resource_name'] == 'admin':
            admin = get_server_info(server['physical_resource_id'], 'admin', node_index=0)

    environment['minions'] = [admin]
    build_master_info(environment, masters)
    build_worker_info(environment, workers)
    environment['dashboardHost'] = admin['addresses']['privateIpv4']
    environment['dashboardExternalHost'] = admin['addresses']['publicIpv4']
    environment['kubernetesExternalHost'] = masters[0]['addresses']['publicIpv4']

    with open('environment.json', 'w') as f:
        json.dump(environment, f, indent=4)
