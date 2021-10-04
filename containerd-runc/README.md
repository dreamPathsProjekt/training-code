# Containerd - runC Container runtime

## Requirements - Container

`runC` needs 3 thing to start container:

- `rootfs` dir with the whole filesystem (of a container filesystem)
- `config.json`
- `runtime.json`

### Export container to tar using docker

```Shell
docker create --name cont1 alpine:latest sh
# Shows only created status, not running
docker ps --all
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
ec8a97772f1c        alpine:latest       "sh"                12 seconds ago      Created                                 cont1

# Export to tar & remove created container
docker export cont1 > alpine.tar
docker rm -f cont1

# Create rootfs dir and untar tar into directory called rootfs:
mkdir -vp rootfs
# mkdir: created directory 'rootfs'
tar -xf alpine.tar -C rootfs/
ls -la rootfs/

total 72
drwxr-xr-x 18 root root 4096 Oct  4 13:46 .
drwxr-x---  5 root root 4096 Oct  4 13:46 ..
-rwxr-xr-x  1 root root    0 Oct  4 13:43 .dockerenv
drwxr-xr-x  2 root root 4096 Jan  9  2018 bin
drwxr-xr-x  4 root root 4096 Oct  4 13:43 dev
drwxr-xr-x 15 root root 4096 Oct  4 13:43 etc
drwxr-xr-x  2 root root 4096 Jan  9  2018 home
drwxr-xr-x  5 root root 4096 Jan  9  2018 lib
drwxr-xr-x  5 root root 4096 Jan  9  2018 media
drwxr-xr-x  2 root root 4096 Jan  9  2018 mnt
dr-xr-xr-x  2 root root 4096 Jan  9  2018 proc
drwx------  2 root root 4096 Jan  9  2018 root
drwxr-xr-x  2 root root 4096 Jan  9  2018 run
drwxr-xr-x  2 root root 4096 Jan  9  2018 sbin
drwxr-xr-x  2 root root 4096 Jan  9  2018 srv
drwxr-xr-x  2 root root 4096 Jan  9  2018 sys
drwxrwxrwt  2 root root 4096 Jan  9  2018 tmp
drwxr-xr-x  7 root root 4096 Jan  9  2018 usr
drwxr-xr-x 11 root root 4096 Jan  9  2018 var
```

### Create spec files

```Shell
# unC can create default spec files based on the rootfs directory using:
runc spec # uses default name rootfs

# Start the container
sudo runc start
# Now inside alpine sh shell
```
