# The Job Hopper

Useful onboarding instructions and how-to guides for "job-hopping" Linux workstations.
This guide is meant to be followed top to bottom, skipping the parts you may not need.

## Change Passwords

### Disk Encryption

To change the disk encryption passphrase:

```bash
sudo cryptsetup luksChangeKey /dev/nvme0n1p3
```

To add a second passphrase, keeping the old one:

```bash
sudo cryptsetup luksAddKey /dev/nvme0n1p3
```

### User Password

To change your user's password:

```bash
passwd
```

## Backup and Adjust Partition Size

> This section is optional and may be dangerous; if you do not pay attention
you may format your disk(s).

The laptop comes with almost the whole disk formatted as a single partition and
a tiny swap partition. Some people might need a larger swap partition in order
to __enable hibernation__, or want to have some unallocated space available they can
later use as they see fit.

### Create, Boot Kubuntu Live Image

The easiest way to repartition is to use KDE's partitionmanager as it can work
on all devices and not just physical ones. In our case our device is the volume
group (VG) stored in the large encrypted partition.

[Download the Kubuntu LTS image.](https://kubuntu.org/getkubuntu/)

Once you have the ISO, the easiest path is to write it to a USB flash drive.

> The contents of the drive will be deleted in the process. We will format it!

If you are on a Linux machine, use `ddrescue`. Plugin your USB flash drive,
check with `dmesg` its disk descriptor (something like `/dev/sdX`), verify with
`fdisk -l /dev/sdX` to make sure you got the correct drive. You can also check
under `/dev/disk/by-id` to find it with a more descriptive name. E.g:
`/dev/disk/by-id/usb-Kingston_DataTraveler_3.0_00190F0C02A9BW32A67E4211-0:0`.

Now write the image:

```bash
ddrescue -v -f -D /path/to/kubuntu-20.04.2.0-desktop-amd64.iso /dev/sdX
```

Reboot your computer. During boot press __F12__ to enter the boot menu and
select the USB key. Once you are in Kubuntu, select the option to try Kubuntu,
__do not select install__.

### Backup

It is always a good idea to take a backup now. If you have an external disk, connect
it to your laptop.

Open a terminal, mount your disk and take a backup. The backup should take
around 30-50GB of space and less than an hour, as we use pigz to compress the
image using all cores.

```Shell
# Flash drive is on /dev/sdY
mount /dev/sdY /mnt
apt update
apt install pigz pv
pv -pterab /dev/nvme0n1 | pigz --processes 6 --stdout > /mnt/laptop-backup.img
sync # This can take quite long if you used a flash drive for the backup
umount /mnt
```

### Repartition

Once your backup is ready, run the KDE Partition Manager (`partitionmanager`).
Select the Ubuntu VG and do the steps in the following order:

1. Resize `/dev/ubuntu-vg/root`
2. Resize `/dev/ubuntu-vg/swap_1`

Do not do any more steps. If you are not sure, press undo and complete
everything in two steps. Then press apply.

The choices are completely personal. I resized my root to 677GB which I think
are enough, then resized the swap to 72GB so I can enable hibernation on it. I
left 202GB unallocated which I can later add them back to root, or create new
partitions, such as a `BTRFS` partition to more efficiently store docker images.

![KDE Partition Manager screenshot](partitionmanager.png)

Once ready reboot your computer.

## Basic System Tweaks

### Improve Battery Life

Install and enable TLP:

```bash
sudo apt install tlp tlp-rdw
sudo tlp start
```

Optionally edit `/etc/tlp.conf` to tweak settings.

### Sleep Issues

Dell's latest laptops do not seem to support deep sleep on Linux —known as S3
state. As a consequence, putting our laptop to sleep, means it stays a bit warm
and eats battery at a much higher rate than usual (12%-24% during a night's
sleep).

If you try to enforce S3 sleep, your computer will not be able to come back from
sleep and you will have to force power it off by keeping the power button
pressed.

Thus the solution is to use hibernation instead for when you need your computer
to stay asleep for more than a few hours.

### Enable Hibernation

During hibernation your computers stores the RAM contents on disk (inside the
swap) then powers off. To hibernate, your computer needs a swap file larger than
your memory. In our case our memory is 64GB, so our swap should be over 64GB. I
recommend 72GB.

If you followed the repartition guide, you already have a large enough swap
space. If you do not want to repartition, you can use a file instead. I have
only tested the swap partition, so I will only describe how to enable
hibernation via a swap partition. You can find resources on the internet on how
to use a file for swap.

Start by finding the UUID of your swap partition. Run the command `blkid` to do
that, like in the example below:

```bash
$ blkid
/dev/mapper/nvme0n1p3_crypt: UUID="b659c5a3-0882-4a8f-a609-dfd656159257" TYPE="LVM2_member"
/dev/mapper/ubuntu--vg-swap_1: UUID="973b0396-303f-4159-b2fe-ea6d42a6497b" TYPE="swap"
/dev/mapper/ubuntu--vg-root: UUID="894e5175-2267-4600-b4cc-0a5bf3f29851" TYPE="ext4"
```

In the example output the swap UUID is `973b0396-303f-4159-b2fe-ea6d42a6497b`.

Edit `/etc/default/grub` and find the line starting with
`GRUB_CMDLINE_LINUX_DEFAULT`. There add the entries
`resume=UUID=[UUID-WE-JUST-FOUND] nmi_watchdog=0`. In the end this line should
look a lot like this:

```Shell
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash resume=UUID=973b0396-303f-4159-b2fe-ea6d42a6497b nmi_watchdog=0"
```

Then update grub with the new settings:

```bash
sudo update-grub
```

To permit screen managers and desktop environments to hibernante the machine,
add a polkit rule by running the command below:

```bash
cat << "EOF" > /etc/polkit-1/localauthority/50-local.d/com.ubuntu.enable-hibernate.pkla
[Re-enable hibernate by default in upower]
Identity=unix-user:*
Action=org.freedesktop.upower.hibernate
ResultActive=yes

[Re-enable hibernate by default in logind]
Identity=unix-user:*
Action=org.freedesktop.login1.hibernate;org.freedesktop.login1.handle-hibernate-key;org.freedesktop.login1;org.freedesktop.login1.hibernate-multiple-sessions;org.freedesktop.login1.hibernate-ignore-inhibit
ResultActive=yes
EOF
```

You need to logout and login for your desktop to see the change.  Now you can
hibernate.

### Random Freezes

The laptop seems to freeze randomly on Linux. There are various reports in the
internet for precision and xps laptops with the same issue.

Things I am currently trying to solve the issue:

- Disable _Sleep_ in BIOS
- Update to latest BIOS (1.9.1). Check the [Firmware Update section](#firmware-update)
- Update to latest Linux kernel (5.13). Better skip this step unless you are
  able to find a way to revert when needed, and recognize issues due to
  unsupported Kernel. This also has the repercussion that it disables nVidia
  drivers since they are build for the LTS kernel.

  ```Shell
  wget https://raw.githubusercontent.com/pimlie/ubuntu-mainline-kernel.sh/master/ubuntu-mainline-kernel.sh
  chmod +x ubuntu-mainline-kernel.sh
  sudo mv ubuntu-mainline-kernel.sh /usr/local/bin/
  sudo ubuntu-mainline-kernel.sh -i
  ```

  Or switch to the latest supported non-LTS kernel (preffered) which seems to be on version 5.11:

  ```Shell
  sudo apt install linux-generic-hwe-20.04
  ```

- Disable Intel GPU Panel Self Refresh
  __most promising__
  Edit `/etc/default/grub` and find the line starting with
  `GRUB_CMDLINE_LINUX_DEFAULT`. There add the entry
  `i915.enable_psr=0`. In the end this line should look similar to this:

  ```Shell
  GRUB_CMDLINE_LINUX_DEFAULT="quiet splash i915.enable_psr=0"
  ```

  Then update grub with the new settings:

  ```bash
  sudo update-grub
  ```

### Install System Tools

These tools might help you track temperature, disk and system health:

```bash
sudo apt install htop i7z lm-sensors smartmontools
```

- htop: process viewer/manager via cli
- i7z: track CPU states and frequency via cli
- lm-sensors: track temperatures (system, CPU, graphics) and fan speed
- smartmontools: track disk health

## Other System Tweaks - Optional

### Install default KDE

If you prefer KDE to Ubuntu's Gnome, it is easy to install.

If you want the default KDE coming with 20.04 run:

```bash
sudo apt install kde-full
```

At the menu screen during the KDE installation, __select SDDM as the session manager__.

### Install Kubuntu Latest KDE

If you want the latest KDE from Kubuntu —though it might be better to avoid it— run:

```bash
sudo add-apt-repository ppa:kubuntu-ppa/backports
sudo apt install kubuntu-desktop
```

If you ever login to a blank desktop, open a terminal (Alt+F2 → Konsole), then
run `killall plasmashell && kstart5 plasmashell`.

If you want to remove Kubuntu and keep Ubuntu's default, logout from KDE and
login to an Ubuntu session, then:

```bash
sudo apt remove kubuntu-desktop
sudo apt autoremove
sudo apt insta ppa-purge
sudo ppa-purge ppa:kubuntu-ppa/backports
sudo rm /etc/apt/sources.list.d/kubuntu-ppa-ubuntu-backports-focal.list
sudo apt install kde-full
```

### Firmware Update

The laptop may indicate that there is a BIOS update available. In my case I got
the laptop with BIOS 1.5.3 and after a couple days was offered an update to
1.9.1.

Before proceeding to the update make sure:

- The laptop is fully charged.
- You have a USB flash drive with a Live Linux image you can boot into. This is
  important because __after the update your Ubuntu will not be able to boot__.

To download the new firmware, prepare the laptop for the update and reboot:

```bash
sudo fwupdmgr refresh
sudo fwupdmgr get-updates
sudo fwupdmgr update
```

The computer will reboot into the firmware update state and will start updating
multiple firmwares (UEFI, BIOS, USB-PD controllers, and more).  Once the update
is finished your computer will boot into a black screen and stay there. As it is
very common with UEFI updates, it broke our bootloader. To fix it:

1. Connect your USB flash drive with the Live Linux image
2. Power off the laptop (keep the power off button pressed for a few seconds)
3. Start it up and press F12 or DEL to get into the boot menu
4. Boot via the Live USB image
5. Once into Linux, unlock your encrypted hard drive, mount it, chroot into
   Ubuntu and fix the bootloader like this:

   ```Shell
   sudo su
   cryptsetup luksOpen /dev/nvme0n1p3 mydisk
   mount /dev/mapper/ubuntu--vg-root /mnt
   mount /dev/nvme0n1p2 /mnt/boot
   mount -t proc proc /mnt/proc
   mount -t sysfs sys /mnt/sys
   mount -o bind /dev /mnt/dev
   cp -L /etc/resolv.conf /mnt/etc/resolv.conf
   chroot /mnt /bin/bash
   update-grub
   exit
   umount /mnt/dev
   umount /mnt/sys
   umount /mnt/proc
   umount /mnt/boot
   umount /mnt
   reboot
   ```

### Yubikey Authentication

Yubikeys in the browser should work automatically. You can further install tools
to manage your Yubikey or use it for authentication and other cryptographic
functions within the operating system.

Add the Yubico repository and install necessary programs:

```bash
sudo add-apt-repository ppa:yubico/stable
sudo apt install yubikey-manager yubikey-personalization-gui libpam-yubico libpam-u2f
```

To register your key under your user account, connect your key to your computer
and run:

```bash
pamu2fcfg | sudo tee /etc/u2f_keys
sudo chmod 644 /etc/u2f_keys
```

To enable authentication via PAM, create the file `/etc/pam.d/common-u2f` with
contents:

```Shell
auth sufficient pam_u2f.so authfile=/etc/u2f_keys cue
```

Note that the keyword `sufficient` means that the Yubikey alone is enough to log
you in, which might not be acceptable unless you make sure you never leave the
Yubikey attached to your system. If you change the keyword to `required`, then
the Yubikey will serve as an additional step to password login (2FA).

Now in order to use the Yubikey for various functions, you need to add the line
`@include common-u2f` before the line `@include common-auth` in the various
configuration files under `/etc/pam.d`.

A few examples, for Yubikey-based sudo, your `/etc/pam.d/sudo` should look like
this:

```Shell
#%PAM-1.0

session    required   pam_env.so readenv=1 user_readenv=0
session    required   pam_env.so readenv=1 envfile=/etc/default/locale user_readenv=0
@include common-u2f
@include common-auth
@include common-account
@include common-session-noninteractive
```

To unlock the KDE lock screen, you should create the file `/etc/pam.d/kde` with
contents:

```Shell
@include common-u2f
@include common-auth
@include common-account
@include common-password
@include common-session
```

The `/etc/pam.d/sddm` manages login in the SDDM login screen.

### AptX (Bluetooth HQ Audio)

Linux supports AptX and other Hi-Fi codes via custom pulseaudio modules. If you
have a headset that supports such a codec (e.g AptX, LDAC, etc) install the
codecs:

```bash
sudo add-apt-repository ppa:berglh/pulseaudio-a2dp
sudo apt update
sudo apt install pulseaudio-modules-bt libldac
```

Restart your computer or just PulseAudio via:

```bash
pulseaudio -k
```

Make sure your headphones are in the stereo sink profile (the one used for
listening to music) and check which codec they use:

```bash
pactl list sinks | grep a2dp_codec
```

Enjoy your music! Unfortunately for now HD codecs for sources (mic) are not
supported.

### Mount /tmp on tmpfs

```bash
sudo systemctl enable /usr/share/systemd/tmp.mount
Created symlink /etc/systemd/system/local-fs.target.wants/tmp.mount → /usr/share/systemd/tmp.mount.
Created symlink /etc/systemd/system/tmp.mount → /usr/share/systemd/tmp.mount.
```
