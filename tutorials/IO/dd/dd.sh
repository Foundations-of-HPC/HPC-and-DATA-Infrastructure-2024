#!/bin/bash
DISK=${1:-sda} 
FS_TYPE=${2:-xfs}
BS="4M"
COUNT=2000

echo "Testing /dev/${DISK}"
dd if=/dev/zero of=/dev/${DISK} bs=${BS} count=${COUNT}

echo "Testing /dev/${DISK} with direct flag"
dd if=/dev/zero of=/dev/${DISK} oflag=direct  bs=${BS} count=${COUNT}


echo "Build a fs of type ${FS_TYPE}"
mkfs.${FS_TYPE} /dev/${DISK}

mkdir -p /mnt/mydisk
mount /dev/${DISK} /mnt/mydisk

echo "Testing /dev/${DISK} with ${FS_TYPE}"
dd if=/dev/zero of=/mnt/mydisk/testfile  bs=${BS} count=${COUNT}

echo "Testing /dev/${DISK} with ${FS_TYPE} and direct flag"
dd if=/dev/zero of=/mnt/mydisk/testfile oflag=direct  bs=${BS} count=${COUNT}

umount /mnt/mydisk
wipefs -a /dev/${DISK}
