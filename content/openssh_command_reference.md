Title: OpenSSH Command Reference
Date: 2019-10-12 07:05
Category: Linux
Tags: linux, ssh, cli
Authors: Eric Rochow
Summary: A list of commands I need on a regular basis but infrequently enough not to commit to memory

# Create a key pair
```shell
ssh-keygen -t rsa -b 4096 -C "$(whoami)@$(hostname)-$(date -u +%Y-%m-%d-%H:%M:%S%z)"
```
# Copy the keys to the remote machine:
```shell
ssh-copy-id <linuxserver>
```
# Attempt to log into the remote machine:
```shell
ssh <linuxserver>
```