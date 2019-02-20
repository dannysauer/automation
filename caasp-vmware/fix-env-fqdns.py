
# Temporary script to inject hostnames in environment.json

import json
import time
import sys
import subprocess


def fetch_hostname(ipaddr):
    cmd = ("ssh -tt -i ../misc-files/id_shared root@{} "
           "-oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null"
           " hostname").format(ipaddr)
    print("Running %r" % cmd)
    for retry_cnt in range(1, 100):
        try:
            out = subprocess.check_output(cmd, shell=True,
                                          stderr=subprocess.PIPE)
            out = out.decode().strip()
            print("---")
            print(out)
            print("---")
            return out
        except subprocess.CalledProcessError as e:
            print("Error on try %d: %r" % (retry_cnt, e.stderr.decode()))
            time.sleep(5)
    print("ERROR - giving up")
    sys.exit(1)


def main():
    domain = ".qa.prv.suse.net"

    with open('environment.json') as f:
        ej = json.load(f)

    for minion in ej["minions"]:
        ipaddr = minion["fqdn"]
        hostname = fetch_hostname(ipaddr)
        hostname = hostname + domain
        # replace ipaddr with real fqdn
        print("{} <- {}".format(ipaddr, hostname))
        minion["fqdn"] = hostname

    with open('environment.json', 'w') as f:
        json.dump(ej, f, sort_keys=True, indent=2)



if __name__ ==  '__main__':
    main()
