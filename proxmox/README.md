# Proxmox VE 6.0 / 7.0

- [Udemy Proxmox VE 6 Course](https://www.udemy.com/course/proxmox-ve-5)
- [Udemy Proxmox VE HA with Corosync & CEPH](https://www.udemy.com/course/high-availability-cluster-with-proxmox-and-ceph)

## Prepare installation media (USB)

- [https://pve.proxmox.com/pve-docs/chapter-pve-installation.html#_prepare_a_usb_flash_drive_as_installation_medium](https://pve.proxmox.com/pve-docs/chapter-pve-installation.html#_prepare_a_usb_flash_drive_as_installation_medium)
- [https://www.thegeekstuff.com/2011/09/parted-command-examples/](https://www.thegeekstuff.com/2011/09/parted-command-examples/)
- [https://www.tecmint.com/create-disk-partitions-in-linux/](https://www.tecmint.com/create-disk-partitions-in-linux/)
- [https://www.geeksforgeeks.org/dd-command-linux/](https://www.geeksforgeeks.org/dd-command-linux/)
- [Proxmox VE ISO Images](https://www.proxmox.com/en/downloads/category/iso-images-pve)

Partitioning does not work for bootable UEFI drive, needs single partition with `dd` command.

```Shell
# Optional slow: Wipe the whole USB disk & parition info. Might need to create 1 partition afterwards (?)
sudo dd bs=1M if=/dev/zero of=/dev/sdb bs=1M status=progress

# Copy the .iso image for Proxmox VE to /dev/sdb live USB, warning: copy to whole disk not partition.
sudo dd bs=1M conv=fdatasync if=~/Downloads/iso/proxmox-ve_7.0-2.iso of=/dev/sdb status=progress

# You can create more partitions for data to utilize USB disk space, and the live boot will be usable.
sudo parted /dev/sdb

# Show partition info
sudo fdisk -l /dev/sdb

# Create partition auto-mountable in Linux/Windows (fat32) - Start last Gap1 +1 kb, end: end of sector/Mb or 100%
(parted) mkpart primary fat32 <start> 100%
# Rename label for partition 5
(parted) name 5
# Name can be Data
Partition name?  []? Data
# Print partition info
(parted) print
(parted) quit
# Format the partition with mkfs.fat (fat32 by default)
sudo mkfs.fat /dev/sdb5
```

## Storage

### Create new LVM, LVM-Thin storage from secondary disk

- [https://www.hostfav.com/blog/index.php/2017/02/01/add-a-new-physical-hard-drive-to-proxmox-ve-4x-5x/](https://www.hostfav.com/blog/index.php/2017/02/01/add-a-new-physical-hard-drive-to-proxmox-ve-4x-5x/)
- [https://forum.proxmox.com/threads/how-to-create-an-lvm-thinpool-and-vz-directory-on-the-same-disk.62901/](https://forum.proxmox.com/threads/how-to-create-an-lvm-thinpool-and-vz-directory-on-the-same-disk.62901/)
- [https://www.tecmint.com/manage-and-create-lvm-parition-using-vgcreate-lvcreate-and-lvextend/](https://www.tecmint.com/manage-and-create-lvm-parition-using-vgcreate-lvcreate-and-lvextend/)
- [https://www.reddit.com/r/Proxmox/comments/7jw6m0/trying_to_add_a_lvm_new_hard_drive_but_not/](https://www.reddit.com/r/Proxmox/comments/7jw6m0/trying_to_add_a_lvm_new_hard_drive_but_not/)

```Shell
# Carefully identify disk with lsblk
# Create partition on empty disk
fdisk /dev/sdb

# Create new partition type n and hit enter

Command (m for help): n
Partition type
 p primary (0 primary, 0 extended, 4 free)
 e extended (container for logical partitions)

# Select partition type p for Primary and select default value for Partition Number, First Sector and Last Sector.

Partition number (1-4, default 1):
First sector (2048-16777215, default 2048):
Last sector, +sectors or +size{K,M,G,T,P} (2048-16777215, default 16777215):

Created a new partition 1 of type 'Linux' and of size 8 GiB.

# Save partition – type w and hit enter.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.

# Can be better if parted is used.

# Uknown: Create filesystem ext4 (better for resizing) or xfs (resize only up supported)
mkfs.ext4 /dev/sdb1

# Now new drive is ready. Using following commands we are going to create LVM Volumes.

# Create Physical LVM volume
pvcreate /dev/sdb1
Physical volume "/dev/sdb1" successfully created.

# List physical volumes and display volume info
pvs
pvdisplay /dev/sdb1

# Create Logical Volume Group
vgcreate newdrivegroup /dev/sdb1
Volume group "newdrivegroup" successfully created

# List logical volume groups and display vg group info
vgs
vgdisplay newdrivegroup

# Create Logical Volume, type LVM Thin. Name is newvol. Size is relative 100% available
lvcreate newdrivegroup -n newvol --type thin-pool -l 100%FREE /dev/sdb1
# Alternative
lvcreate newdrivegroup -n newvol --thin/-T -l 100%FREE /dev/sdb1

# List logical volumes and display volume info
lvs
lvdisplay newvol

# Logical Volume rename example
lvrename /dev/newdrivegroup/newvol /dev/newdrivegroup/data_secondary

# Convert Volume from LVM to thinpool and other types.
lvconvert --type thin-pool newvol

# Scan PVE Storage for volumes
pvesm scan lvmthin newvol

# Add storage either from dashboard or using pvesm add command. For LVM use pvesm add lvm <name> --vgname <vgname>
pvesm add lvmthin local-lvm-secondary --vgname newdrivegroup --thinpool newvol
```

### Create new DIR Storage

- [https://manjaro.site/how-to-add-extra-hard-drives-to-proxmox-6-2-ve/](https://manjaro.site/how-to-add-extra-hard-drives-to-proxmox-6-2-ve/)