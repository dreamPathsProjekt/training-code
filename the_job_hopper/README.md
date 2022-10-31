# The Job Hopper

Useful onboarding instructions and how-to guides for "job-hopping" Linux workstations.
This guide is meant to be followed top to bottom, skipping the parts you may not need.

- [The Job Hopper](#the-job-hopper)
  - [Change Passwords](#change-passwords)
    - [Disk Encryption](#disk-encryption)
    - [User Password](#user-password)
  - [Backup and Adjust Partition Size](#backup-and-adjust-partition-size)
    - [Create, Boot Kubuntu Live Image](#create-boot-kubuntu-live-image)
    - [Backup](#backup)
    - [Repartition](#repartition)
  - [Basic System Tweaks](#basic-system-tweaks)
    - [Improve Battery Life](#improve-battery-life)
    - [Sleep Issues](#sleep-issues)
    - [Enable Hibernation](#enable-hibernation)
    - [Random Freezes](#random-freezes)
    - [Install System Tools](#install-system-tools)
  - [Other System Tweaks - Optional](#other-system-tweaks---optional)
    - [Install default KDE](#install-default-kde)
    - [Install Kubuntu Latest KDE](#install-kubuntu-latest-kde)
    - [Firmware Update](#firmware-update)
    - [Yubikey Authentication](#yubikey-authentication)
    - [AptX (Bluetooth HQ Audio)](#aptx-bluetooth-hq-audio)
    - [Mount /tmp on tmpfs](#mount-tmp-on-tmpfs)
  - [Install Productivity Tools](#install-productivity-tools)
    - [Chrome](#chrome)
    - [Slack](#slack)
      - [Via Deb Package](#via-deb-package)
      - [Via Snap Package](#via-snap-package)
    - [OpenVPN](#openvpn)
    - [OpenVPN3 - Terminal](#openvpn3---terminal)
      - [OpenVPN3 Installation](#openvpn3-installation)
      - [OpenVPN3 Usage](#openvpn3-usage)
    - [Screenrecorder](#screenrecorder)
  - [Install Development Tools](#install-development-tools)
    - [Common](#common)
  - [Developer Tweaks](#developer-tweaks)
    - [Bash completion](#bash-completion)
    - [GPG Agent](#gpg-agent)
    - [SSH Agent](#ssh-agent)
    - [Verify Jenkinsfiles](#verify-jenkinsfiles)
    - [Terminal and Editor customization](#terminal-and-editor-customization)
      - [Terminator Themes](#terminator-themes)
      - [Bash Git Prompt](#bash-git-prompt)
      - [Vim Colorschemes](#vim-colorschemes)
      - [K8s Prompt](#k8s-prompt)

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

[Check Swap Size](https://www.cyberciti.biz/faq/linux-check-swap-usage-command/)

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
# On some systems boot partition is on nvme0n1p1 and root on nvme0n1p3
pv -pterab /dev/nvme0n1p3 | pigz --processes 6 --stdout > /mnt/laptop-backup.img
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

## Install Productivity Tools

### Chrome

> Remember to separate your work profile from your personal profile. Store
work-related passwords only to the work profile. Also remember to import bookmarks from your profile/(s).

To install Chrome via Google's repositories:

```bash
curl -L https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable
```

If Chrome comes pre-installed, fix your repo signing key with:

```bash
curl -L https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo apt update
```

### Slack

Like Zoom you can install Slack manually via deb, or via snap. Via deb it is
more performant. Also it installs automatically its repository so you get
updates via apt, thus there is no reason to choose snap.

#### Via Deb Package

Download [Slack Deb package from Slack's
website](https://slack.com/intl/en-gr/downloads/linux) and install:

```bash
sudo apt install ~/Downloads/slack-desktop-4.19.2-amd64.deb
```

You will have to do the same every time you want to update.

#### Via Snap Package

```bash
sudo snap install --classic slack
```

### OpenVPN

To install OpenVPN:

```bash
sudo apt install network-manager-openvpn network-manager-openvpn-gnome openvpn openvpn-systemd-resolved
```

Once installed you can add a new OpenVPN connection to NetworkManager.

Open NetworkManager, press the _Add new connection_ button,
then select _Other → Import VPN connection..._ and add the `ovpn` file that was
provided to you.

### OpenVPN3 - Terminal

In any case if the VPN config does not work correctly with NetworkManager, install `openvpn3`
The terminal-based `openvpn3` is an easy to use network manager for VPN configurations,
that does not need `sudo` execution permissions and can save configurations.

#### OpenVPN3 Installation

To install OpenVPN3:

```Shell
# Add, install and fix the openvpn3 repos
sudo apt install apt-transport-https
sudo wget https://swupdate.openvpn.net/repos/openvpn-repo-pkg-key.pub
sudo apt-key add openvpn-repo-pkg-key.pub

sudo wget -O /etc/apt/sources.list.d/openvpn3.list "https://swupdate.openvpn.net/community/openvpn3/repos/openvpn3-$(lsb_release -cs).list"

# Fix the openvpn3 repo to correctly retrieve amd64 arch versions
sudo vim /etc/apt/sources.list.d/openvpn3.list

# Replace line:
deb https://swupdate.openvpn.net/community/openvpn3/repos focal main
# With Line:
deb [arch=amd64] https://swupdate.openvpn.net/community/openvpn3/repos focal main

# Update & install
sudo apt update
sudo apt install openvpn3
```

#### OpenVPN3 Usage

Import tcp and udp config files for VPN. In this example the configuration files are extracted in folder: `~/.local/share/openvpn-configs`

```Shell
# Import the 2 config files with names
openvpn3 config-import --persistent --name example-udp --config ~/.local/share/openvpn-configs/openvpn-udp.conf
openvpn3 config-import --persistent --name example --config ~/.local/share/openvpn-configs/openvpn.conf

# List configs to show their canonical folders
Configuration path
Imported                        Last used                 Used
Name                                                      Owner
------------------------------------------------------------------------------
/net/openvpn/v3/configuration/7fcc32d9xb405x4f78xa72axcbe6a87dc532
Sat Oct 30 20:59:03 2021        Sat Oct 30 21:02:51 2021  2
example-udp                                                <your-user>

/net/openvpn/v3/configuration/ae3636c1xbdc4x45abxbd5fx241fd7814762
Sat Oct 30 21:04:50 2021                                  0
example                                                    <your-user>
------------------------------------------------------------------------------
```

Start a session in the background, e.g. the udp one

```Shell
# Start with named configuration
openvpn3 session-start --config example-udp

# Or, Start with config-path
openvpn3 session-start --config-path /net/openvpn/v3/configuration/7fcc32d9xb405x4f78xa72axcbe6a87dc532

# List running sessions
openvpn3 sessions-list
-----------------------------------------------------------------------------
        Path: /net/openvpn/v3/sessions/f911ff8es6482s4ed6sb6bbs0fb28c91fa04
     Created: Sat Oct 30 21:02:51 2021                  PID: 59210
       Owner: <your-user>                             Device: tun0
 Config name: /home/<your-user>/.local/share/openvpn-configs/openvpn-udp.conf  (Current name: example-udp)
Session name: boxes.yourdomain.com
      Status: Connection, Client connected
-----------------------------------------------------------------------------
```

Close running session when finished

```Shell
# Disconnect with named configuration
openvpn3 session-manage --disconnect --config example-udp

# Disconnect with session-path
openvpn3 session-manage --path /net/openvpn/v3/sessions/f911ff8es6482s4ed6sb6bbs0fb28c91fa04 --disconnect
```

### Screenrecorder

To record videos of your screen you can use _simplescreenrecorder_:

```bash
sudo apt install simplescreenrecorder
```

## Install Development Tools

### Common

These command line utilities can be used to improve your workflows or help you
debug:

```bash
sudo apt install curl mosh silversearcher-ag
```

- curl: the well known tool to perform requests to web servers
- mosh: the mobile shell can be used for persistent ssh sessions
- silversearcher-ag: better than grep for searching source code

Can be found on asdf:

- tmux: shell session manager, better than screen
- shellcheck: shell script analysis tool, required by the SRE chapter
- jq: manipulate JSON in the command line, useful for scripting and working with JSON APIs

## Developer Tweaks

### Bash completion

To add bash completion add this line to your `~/.bashrc`:

```Shell
source /etc/profile.d/bash_completion.sh
```

If you are not sure how to do it, here is an one liner:

```Shell
grep -wq '^source /etc/profile.d/bash_completion.sh' ~/.bashrc \
  || echo 'source /etc/profile.d/bash_completion.sh' >> ~/.bashrc
```

The completion will start working on new terminals.

### GPG Agent

The gpg-agent should be up and running by default.

### SSH Agent

The ssh-agent should be up and running by default. You can add keys via the
command line:

```bash
ssh-add -l ~/.ssh/id_rsa
```

### Verify Jenkinsfiles

The SRE and Testing chapters work excesively with Jenkins. Add this function to
your `.bashrc` file to be able to validate Jenkinsfile using our Jenkins
instance, substituing the `user` in curl:

```Shell
# Jenkins domain ci.jenkinsdomain.io is an example
jenkins-validate() {
    _file=${1:-Jenkinsfile}
    curl --user $(pass ci.jenkinsdomain.io/user) -X POST -F "jenkinsfile=<$_file" https://ci.jenkinsdomain.io/pipeline-model-converter/validate
}
```

In the example I use a program (`pass`) to store my credentials. Pass relies on
the gpg-agent to keep my password secure. The contents of the secret are my
Jenkins credentials, in the form `username:password`.

Do remember that script sections in Jenkinsfiles cannot be validated, so your
only way to test them is runtime.

### Terminal and Editor customization

#### Terminator Themes

- [Terminator Themes](https://github.com/EliverLara/terminator-themes)

```bash
# Terminator configs under
ll ~/.config/terminator/
```

#### Bash Git Prompt

- [Bash Git Prompt](https://github.com/magicmonty/bash-git-prompt)

#### Vim Colorschemes

- [Personal Repo](https://bitbucket.org/dreamPathsProjekt/vim_bash_profiles/src/master/)

#### K8s Prompt

- [Kube PS1](https://github.com/jonmosco/kube-ps1)
