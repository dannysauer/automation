#!/bin/bash

set -euo pipefail

OPENRC=$1
CHANNEL=$2

IMAGE_FILENAME=$(readlink ../downloads/openstack-${CHANNEL})
IMAGE_BUILD=$(echo $IMAGE_FILENAME | sed -n 's/.*\(Build.*\).qcow2/\1/p')
IMAGE_VERSION=$(echo $IMAGE_FILENAME | sed -n 's/.*\(CaaS-Platform\|CaaSP\)-\(.*\)-\(for\|CaaSP\).*-OpenStack-Cloud.*/\1/p')
IMAGE_NAME="CaaSP-${CHANNEL}-${IMAGE_VERSION}-${IMAGE_BUILD}"

[[ -e $OPENRC ]] && source $OPENRC
echo "[+] Checking if we already have this image: $IMAGE_NAME"

if [[ $(openstack image list -c ID -f value --property caasp-version="${IMAGE_VERSION}" --property caasp-channel="${CHANNEL}" --property caasp-build="${IMAGE_BUILD}") == "" ]]; then
    echo "[+] Uploading SUSE CaaSP qcow2 VM image: $IMAGE_NAME"
    if openstack image create $IMAGE_NAME --private --disk-format qcow2 --container-format bare --min-disk 40 --file $IMAGE_FILENAME \
        --property caasp-version="$IMAGE_VERSION" \
        --property caasp-build="$IMAGE_BUILD" \
        --property caasp-channel="$CHANNEL"; then
        echo "[+] Deleting previous SUSE CaaSP qcow2 VM image for {version=$IMAGE_VERSION, channel=$CHANNEL}"
        for image in $(openstack image list -c Name -f value --property caasp-version="${IMAGE_VERSION}" --property caasp-channel="${CHANNEL}"); do
            [[ $image == $IMAGE_NAME ]] && continue
            openstack image delete $image
        done
    else
        echo "Failed to upload new image ${IMAGE_NAME}"
        exit 1
    fi
else
   echo "[+] Skipping upload, we already have this image"
fi
