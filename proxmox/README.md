# Proxmox VE 6.0 / 7.0

- [Udemy Proxmox VE 6 Course](https://www.udemy.com/course/proxmox-ve-5)
- [Udemy Proxmox VE HA with Corosync & CEPH](https://www.udemy.com/course/high-availability-cluster-with-proxmox-and-ceph)
- [Hardware Info commands](https://medium.com/technology-hits/basic-linux-commands-to-check-hardware-and-system-information-62a4436d40db)

## Prepare installation media (USB)

- [https://pve.proxmox.com/pve-docs/chapter-pve-installation.html#_prepare_a_usb_flash_drive_as_installation_medium](https://pve.proxmox.com/pve-docs/chapter-pve-installation.html#_prepare_a_usb_flash_drive_as_installation_medium)
- [https://www.thegeekstuff.com/2011/09/parted-command-examples/](https://www.thegeekstuff.com/2011/09/parted-command-examples/)
- [https://www.tecmint.com/create-disk-partitions-in-linux/](https://www.tecmint.com/create-disk-partitions-in-linux/)
- [https://www.geeksforgeeks.org/dd-command-linux/](https://www.geeksforgeeks.org/dd-command-linux/)
- [Proxmox VE ISO Images](https://www.proxmox.com/en/downloads/category/iso-images-pve)
- [https://www.reddit.com/r/linuxquestions/comments/hb5nlv/question_on_the_tool_wipefs_and_dd/](https://www.reddit.com/r/linuxquestions/comments/hb5nlv/question_on_the_tool_wipefs_and_dd/)
- [https://superuser.com/questions/831486/complete-wiping-of-hard-drive-shred-wipe-or-dd](https://superuser.com/questions/831486/complete-wiping-of-hard-drive-shred-wipe-or-dd)
- [https://medium.com/@liamcs98/functional-proxmox-homelab-framework-1bc7a68cc559](https://medium.com/@liamcs98/functional-proxmox-homelab-framework-1bc7a68cc559)
- [https://gateway-it.com/turn-your-old-laptop-into-perfect-proxmox-server/](https://gateway-it.com/turn-your-old-laptop-into-perfect-proxmox-server/)

Partitioning does not work for bootable UEFI drive, needs single partition with `dd` command.

```Shell
# Optional slow: Wipe the whole USB disk & parition info. Might need to create 1 partition afterwards (?)
sudo dd bs=1M if=/dev/zero of=/dev/sdb bs=1M status=progress
# Use wipefs --all for faster results
sudo wipefs --all /dev/sdb

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
- [https://www.cyberciti.biz/faq/howto-add-disk-to-lvm-volume-on-linux-to-increase-size-of-pool/](https://www.cyberciti.biz/faq/howto-add-disk-to-lvm-volume-on-linux-to-increase-size-of-pool/)

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

### Extend LVM size with additional Hard Drive

```Shell
# List physical volumes and display volume info
pvs
# List logical volume groups and display vg group info
vgs
# List logical volumes and display volume info
lvs

# Create Physical LVM volume - new hard drive is /dev/sda
pvcreate /dev/sda
# Scan for usable LVM volumes
pvs
lvmdiskscan -l

# Extend volume group: pve
vgextend pve /dev/sda
# Extend logical volume/thinpool /dev/pve/data
lvextend /dev/pve/data /dev/sda

# See extended config
lsblk

NAME                 MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda                    8:0    0 931.5G  0 disk
└─pve-data_tdata     253:3    0   1.2T  0 lvm
  └─pve-data-tpool   253:4    0   1.2T  0 lvm
    └─pve-data       253:5    0   1.2T  1 lvm
sdb                    8:16   0 465.8G  0 disk
├─sdb1                 8:17   0  1007K  0 part
├─sdb2                 8:18   0   512M  0 part /boot/efi
└─sdb3                 8:19   0 465.3G  0 part
  ├─pve-swap         253:0    0     7G  0 lvm  [SWAP]
  ├─pve-root         253:1    0    96G  0 lvm  /
  ├─pve-data_tmeta   253:2    0   3.5G  0 lvm
  │ └─pve-data-tpool 253:4    0   1.2T  0 lvm
  │   └─pve-data     253:5    0   1.2T  1 lvm
  └─pve-data_tdata   253:3    0   1.2T  0 lvm
    └─pve-data-tpool 253:4    0   1.2T  0 lvm
      └─pve-data     253:5    0   1.2T  1 lvm
sr0                   11:0    1  1024M  0 rom

lsblk -f

NAME                 FSTYPE      FSVER    LABEL UUID                                   FSAVAIL FSUSE% MOUNTPOINT
sda                  LVM2_member LVM2 001       nERO3j-yhSh-24Sc-lAKZ-5kku-MVJn-bqYkhN
└─pve-data_tdata
  └─pve-data-tpool
    └─pve-data
sdb
├─sdb1
├─sdb2               vfat        FAT32          42A7-FA0D                               510.7M     0% /boot/efi
└─sdb3               LVM2_member LVM2 001       gCCc4U-SLc8-IINz-wZUs-sKqd-V718-KxsXDf
  ├─pve-swap         swap        1              175d6aea-5106-41df-9799-0fef61682ab1                  [SWAP]
  ├─pve-root         ext4        1.0            1aa9b353-b744-4e19-8d47-11e1ceb70cb6     85.8G     4% /
  ├─pve-data_tmeta
  │ └─pve-data-tpool
  │   └─pve-data
  └─pve-data_tdata
    └─pve-data-tpool
      └─pve-data
sr0

# Final listings
pvs # 2 physical volumes

  PV         VG  Fmt  Attr PSize    PFree
  /dev/sda   pve lvm2 a--   931.51g      0
  /dev/sdb3  pve lvm2 a--  <465.26g <16.00g

lvs # same LVs (thinpool) as before with extended size

  LV   VG  Attr       LSize  Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  data pve twi-aotz--  1.24t             0.00   0.60
  root pve -wi-ao---- 96.00g
  swap pve -wi-ao----  7.00g

vgs # single volume group

  VG  #PV #LV #SN Attr   VSize VFree
  pve   2   3   0 wz--n- 1.36t <16.00g
```

### Create new DIR Storage

- [https://manjaro.site/how-to-add-extra-hard-drives-to-proxmox-6-2-ve/](https://manjaro.site/how-to-add-extra-hard-drives-to-proxmox-6-2-ve/)

## Cool Stuff

- [Access the Web Dashboard without X-windows](https://linuxconfig.org/how-to-run-x-applications-without-a-desktop-or-a-wm)
- [Lightweight Browsers to Install](https://linuxhint.com/top_lightweight_web_browsers_linux/)

## Udemy Course: Proxmox VE 6

### Networking

### PVE Firewall

- Firewall configuration is stored on proxmox `pmxcfs` - Proxmox Cluster FS
  - Mounted on `/etc/pve` - `dev/fuse             128M   16K  128M   1% /etc/pve`
- Rules `iptables` run on each cluster node - full isolation, better bandwidth management.
- Full support for `IPV6` - no need to maintain different rules.
- PVE Firewall Zones:
  - __Host__ traffic from/to nodes
  - __VM__ traffic from/to VM (LXC also)
- PVE-Firewall `pve-firewall.service` service automatically updates rules `iptables` on changes.
- Enable firewall
  - GUI: Datacenter -> Firewall
  - CLI: `/etc/pve/firewall/cluster.fw`
- Firewall __enabled__: Traffic to all hosts is __blocked by default__
  - Exceptions: WebGui(8006) & SSH(22) from __local network__
  - On PVE 7 upgrade on `pve-kernel` is necessary with `apt-get dist-upgrade` for firewall to work correctly.