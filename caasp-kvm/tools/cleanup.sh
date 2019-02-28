#!/bin/bash

# Cleanup KVM: delete VMs, networks, volumes and terraform states
# This script is idempotent and can be run at the beginning of CI runs

set -euo pipefail
DIR="$( cd "$( dirname "$0" )" && pwd )"

echo "Starting cleanup script"

echo "--> Cleaning up VMs"
sudo virsh list --all | (grep -E "(admin|([Mm]aster|[Ww]orker)_[0-9]+)" || :)
sudo virsh list --all | (grep -E "(admin|([Mm]aster|[Ww]orker)_[0-9]+)" || :) | awk '{print $2}' | \
  xargs --no-run-if-empty -n1 -I{} sh -c 'sudo virsh destroy {}; sudo virsh undefine {}'

echo "--> Cleaning up Networks"
sudo virsh net-list --all | (grep "caasp-dev-net" || :)
sudo virsh net-list --all | (grep "caasp-dev-net" || :) | awk '{print $1}' | \
  xargs --no-run-if-empty -n1 -I{} sh -c 'sudo virsh net-destroy {}; sudo virsh net-undefine {}'

echo "--> Cleaning up Volumes"
pools="$(sudo virsh pool-list --all | sed 1,2d | awk '{print $1}')"
echo "    Pools: $pools"
for pool in $pools; do
sudo virsh vol-list --pool "$pool" | \
  (grep -E -e "admin(_cloud_init)?" \
           -e "([Mm]aster|[Ww]orker)(_cloud_init)?_(disk)?[0-9]+" \
           -e "additional-worker-volume" \
           -e "kvm-devel" \
           -e "SUSE-CaaS-Platform-.*KVM.*Build[0-9]+\.[0-9]+" \
  || :) | \
  awk '{print $1}' \
  | xargs --no-run-if-empty -n1 -I{} sudo virsh vol-delete --pool "$pool" '{}'
done

echo "--> Cleaning up Terraform states from caasp-kvm"
pushd $DIR/.. > /dev/null
rm -vf cluster.tf terraform.tfstate*
popd  > /dev/null

# keep files pointed at by kvm-* symlinks, and the newest of each release
echo "--> Cleaning up old KVM image downloads"
pushd $DIR/../../downloads > /dev/null
shopt -s extglob
typeset -A newest=()
typeset -A keepers=()
for F in kvm-+([[:alnum:]]); do
  if [[ -L "$F" ]]; then
    T="$(readlink -fs "$F")"
    [[ -f "$T" ]] && keepers[$(basename $T)]=1
  fi
done
for F in *.qcow2; do
  # only process files (which aren't symlinks to files)
  [[ -f "$F" && ! -L "$F" ]] || continue
  # filename looks like one of:
  #  SUSE-CaaS-Platform-3.0-for-KVM-and-Xen.x86_64-3.0.0-Build14.30.qcow2.tmp
  #  openSUSE-Tumbleweed-Kubic.x86_64-15.0-CaaSP-Stack-hardware-x86_64-Build8.178.qcow2
  prefix=${F%%-+(.|[[:digit:]])-*} # get prefix by deleting after first "-3.0"
  release=${F#"$prefix-"}          # delete that prefix and the hyphen
  release=${release%%-*}           # delete everything from the first hyphen on
  if [[ -z "${newest[$release]:-}" ]]; then
    # no previous newest
    newest[$release]="$F"
  elif [[ "$F" -nt "${newest[$release]}" ]]; then
    # $F is newer than the prev newest; rm that one unless it was a keeper
    [[ -z "${keepers[$(basename "${newest[$release]}")]:-}" ]] \
      && rm -v "${newest[$release]}"
    newest[$release]=$F
  else
    [[ -z "${keepers[$(basename "$F")]:-}" ]] \
      && rm -v "$F"
  fi
done
shopt -u extglob
popd  > /dev/null

echo "--> Cleaning up screenshots"
pushd $DIR/../../velum-bootstrap > /dev/null
rm -vrf screenshots
popd  > /dev/null

echo "Cleanup done"
