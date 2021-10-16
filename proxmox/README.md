# Proxmox VE 6.0 / 7.0

- [Udemy Proxmox VE 6 Course](https://www.udemy.com/course/proxmox-ve-5)
- [Udemy Proxmox VE HA with Corosync & CEPH](https://www.udemy.com/course/high-availability-cluster-with-proxmox-and-ceph)

## Prepare installation media (USB)

- [https://pve.proxmox.com/pve-docs/chapter-pve-installation.html#_prepare_a_usb_flash_drive_as_installation_medium](https://pve.proxmox.com/pve-docs/chapter-pve-installation.html#_prepare_a_usb_flash_drive_as_installation_medium)
- [https://www.thegeekstuff.com/2011/09/parted-command-examples/](https://www.thegeekstuff.com/2011/09/parted-command-examples/)
- [https://www.tecmint.com/create-disk-partitions-in-linux/](https://www.tecmint.com/create-disk-partitions-in-linux/)
- [https://www.geeksforgeeks.org/dd-command-linux/](https://www.geeksforgeeks.org/dd-command-linux/)
- [Proxmox VE ISO Images](https://www.proxmox.com/en/downloads/category/iso-images-pve)

```Shell
# If needed create bootable partitions on USB

# Be very careful to find USB media /dev/<name> label. In this example /dev/sdb is the removable media
sudo parted -l

Model:  USB  SanDisk 3.2Gen1 (scsi)
Disk /dev/sdb: 30.8GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

# Start partition process for this drive
sudo parted /dev/sdb
# Create partition table (gpt)
(parted) mklabel gpt
Warning: The existing disk label on /dev/sdb will be destroyed and all data on this disk will be lost. Do you want to continue?
Yes/No? yes

# Show info
(parted) print
Model:  USB  SanDisk 3.2Gen1 (scsi)
Disk /dev/sdb: 30.8GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start  End  Size  File system  Name  Flags

# Get help on all options for mkpart
(parted) help mkpart
  mkpart PART-TYPE [FS-TYPE] START END     make a partition

    PART-TYPE is one of: primary, logical, extended
        FS-TYPE is one of: zfs, udf, btrfs, nilfs2, ext4, ext3, ext2, f2fs, fat32, fat16, hfsx, hfs+, hfs, jfs, swsusp, linux-swap(v1), linux-swap(v0), ntfs, reiserfs, freebsd-ufs, hp-ufs,
        sun-ufs, xfs, apfs2, apfs1, asfs, amufs5, amufs4, amufs3, amufs2, amufs1, amufs0, amufs, affs7, affs6, affs5, affs4, affs3, affs2, affs1, affs0, linux-swap, linux-swap(new),
        linux-swap(old)
        START and END are disk locations, such as 4GB or 10%.  Negative values count from the end of the disk.  For example, -1s specifies exactly the last sector.

        'mkpart' makes a partition without creating a new file system on the partition.  FS-TYPE may be specified to set an appropriate partition ID.

# Create first partition bootable (primary) 4gb (start:0 end:4096MB). You can also ommit fstype
(parted) mkpart primary xfs 0 4096MB
Warning: The resulting partition is not properly aligned for best performance: 34s % 2048s != 0s
Ignore/Cancel? I
(parted) print
Model:  USB  SanDisk 3.2Gen1 (scsi)
Disk /dev/sdb: 30.8GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name     Flags
 1      17.4kB  4096MB  4096MB  xfs          primary

# Create second bootable partition (e.g. 2nd live usb distro in same usb drive)
(parted) mkpart primary xfs 4096MB 8192MB
Warning: The resulting partition is not properly aligned for best performance: 8000001s % 2048s != 0s
Ignore/Cancel? I
(parted) print
Model:  USB  SanDisk 3.2Gen1 (scsi)
Disk /dev/sdb: 30.8GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name     Flags
 1      17.4kB  4096MB  4096MB  xfs          primary
 2      4096MB  8192MB  4096MB  xfs          primary

# Set boot flags on both
(parted) set 1 boot on
(parted) set 2 boot on
(parted) print
Model:  USB  SanDisk 3.2Gen1 (scsi)
Disk /dev/sdb: 30.8GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name     Flags
 1      17.4kB  4096MB  4096MB               primary  boot, esp
 2      4096MB  8192MB  4096MB               primary  boot, esp

# Quit and review partitioned disks with lsblk
(parted) quit
lsblk

# ...
sdb             8:16   1  28.7G  0 disk
├─sdb1          8:17   1   3.8G  0 part
└─sdb2          8:18   1   3.8G  0 part

# Copy the .iso image for Proxmox VE to /dev/sdb1 live USB
sudo dd bs=1M conv=fdatasync if=~/Downloads/iso/proxmox-ve_7.0-2.iso of=/dev/sdb1
```
