# Common Lisp Basic

## Doom-Emacs Recipe

- [https://github.com/hlissner/doom-emacs/blob/develop/docs/getting_started.org#ubuntu](https://github.com/hlissner/doom-emacs/blob/develop/docs/getting_started.org#ubuntu)

```Shell
## Ubuntu Bionic - 18.04 ##
ll /root/
add-apt-repository ppa:kelleyk/emacs -y
apt-get update
apt install bash-completion
source /etc/bash_completion
apt-cache madison emacs
apt-cache madison emacs27
apt install emacs27
cd /root/
ll
type emacs
emacs
ll
ll .emacs.d/
apt install git
find
git --version
apt-get install ripgrep
$ curl -LO https://github.com/BurntSushi/ripgrep/releases/download/13.0.0/ripgrep_13.0.0_amd64.deb
curl -LO https://github.com/BurntSushi/ripgrep/releases/download/13.0.0/ripgrep_13.0.0_amd64.deb
apt install curl
curl -LO https://github.com/BurntSushi/ripgrep/releases/download/13.0.0/ripgrep_13.0.0_amd64.deb
dpkg -i ripgrep_13.0.0_amd64.deb
git clone --depth 1 https://github.com/hlissner/doom-emacs ~/.emacs.d
~/.emacs.d/bin/doom install
apt-get update
apt list --upgradable | grep git
add-apt-repository ppa:git-core/ppa
add-apt-repository ppa:git-core/ppa -y
apt update
apt list --upgradable
apt list --upgradable | grep git
apt upgrade git git-man
~/.emacs.d/bin/doom install
~/.emacs.d/bin/doom doctor

# Recipe for doom install
git clone --depth 1 https://github.com/hlissner/doom-emacs ~/.emacs.d
yes | ~/.emacs.d/bin/doom install
yes | ~/.emacs.d/bin/doom sync
echo >> ~/.doom.d/init.el
yes | ~/.emacs.d/bin/doom sync

## Ubuntu latest - Focal - 20.04 ##
apt-cache  madison git # Versions needed
       git | 1:2.25.1-1ubuntu3.2 | http://archive.ubuntu.com/ubuntu focal-updates/main amd64 Packages
       git | 1:2.25.1-1ubuntu3.2 | http://security.ubuntu.com/ubuntu focal-security/main amd64 Packages
       git | 1:2.25.1-1ubuntu3 | http://archive.ubuntu.com/ubuntu focal/main amd64 Packages
apt-cache  madison emacs
     emacs | 1:26.3+1-1ubuntu2 | http://archive.ubuntu.com/ubuntu focal/universe amd64 Packages
apt-cache  madison ripgrep
   ripgrep | 11.0.2-1build1 | http://archive.ubuntu.com/ubuntu focal/universe amd64 Packages
apt-cache  madison fd-find
   fd-find | 7.4.0-2build1 | http://archive.ubuntu.com/ubuntu focal/universe amd64 Packages

apt-get install git curl ripgrep fd-find software-properties-common # needs tz_data

add-apt-repository ppa:kelleyk/emacs -y
apt-get update
apt-cache madison emacs27
   emacs27 | 27.1~1.git86d8d76aa3-kk2+20.04 | http://ppa.launchpad.net/kelleyk/emacs/ubuntu focal/main amd64 Packages

# Install emacs 27.1
apt-get install -y emacs27
# Without creation of ~/.emacs.d/
git clone --depth 1 https://github.com/hlissner/doom-emacs ~/.emacs.d
yes | ~/.emacs.d/bin/doom install
yes | ~/.emacs.d/bin/doom sync

## Debian 11.1-slim ##
apt-get install -y ripgrep fd-find emacs
git clone --depth 1 https://github.com/hlissner/doom-emacs ~/.emacs.d
yes | ~/.emacs.d/bin/doom install
yes | ~/.emacs.d/bin/doom sync

# Install docker-ce-cli only
sudo apt-get update
sudo apt-get install  -y   apt-transport-https     ca-certificates     curl     gnupg     lsb-release
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get -y install docker-ce-cli docker-compose
docker version

# Run docker commands as dockeruser, do this on entrypoint, dynamically find gid
sudo groupadd -g 998 docker
sudo adduser dockeruser docker
```

- [Container-dind user run docker without sudo](https://stackoverflow.com/questions/47517128/how-do-i-give-a-non-root-user-access-to-docker-when-using-docker-dind)
