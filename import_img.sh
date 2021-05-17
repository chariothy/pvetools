IMG=$1
VMID=$2
echo IMG=$IMG
echo VMID=$VMID
size=`ls -l $IMG | awk '{print $5}'`
pad_size=`python3 /root/pveutils/pad_disk_size.py $size`
echo SIZE=$size
echo PAD_SIZE=$pad_size

dd if=/dev/zero bs=1 count=$pad_size >> $IMG
DISK=vm-$VMID-disk.qcow2
echo DISK=$DISK
qemu-img convert -f raw -O qcow2 $IMG $DISK
/sbin/qm importdisk $VMID $DISK local-zfs
rm $IMG
rm $DISK