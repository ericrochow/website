Title: Mounting Devices in LXD
Date: 2020-01-25 11:19
Category: Containers
Tags: containers, lxd, linux
Authors: Eric Rochow


Some use cases for containers depend on passing devices through from the host system into the container. This can allow you to do anything from mount you home directory to passing through a USB device.

## Adding Devices in LXD

### NIC

Mounting a NIC device on the container allows a host system network interface (physical or logical) to the container. [See here for more detail](/lxd-networking.html). **NOTE!** Mounting the NIC to the container will cause the interface to disappear from the host system as it now "belongs" to the container. Make sure before you do this that nothing on your host system is utilizing the device intended to be mounted!

#### Command

    lxc config device add $ctr_name $dev_name nic parent=$parent_iface_name

#### Example

    lxc config device add app1 eth99 nic parent=enp3s0

The above will take the network interface `enp3s0` from the host system and attach it to the container `app1` as network interface `eth99`.

[Apply the configuration to the container](#markdown-header-apply-configuration-changes-to-container)

### Disk

The `disk` device type is probably the most straightforward of the device types and the one I most often use. This allows a directory on the host system to also be mounted in the container itself to either share between containers or to maintain state in the example of an ephemeral container.

#### Command

    lxc config device add $ctr_name $dev_name disk source=/path/to/host/dir path=/path/to/ctr/mount/point

[Apply the configuration to the container](#markdown-header-apply-configuration-changes-to-container)

#### Example

To mount a home drive from the host system to the container named app1:

    lxc config device add app1 home_directory disk source=/home/eric path=/home/ubuntu

This creates a `disk` device named `home_directory` and attaches it to the container `app1`. The host system directory `/home/eric` is now available within `app1` as `/home/ubuntu`.

[Apply the configuration to the container](#markdown-header-apply-configuration-changes-to-container)

### UNIX Char

The `unix-char` device type allows a "character" device to be attached to the container. Character devices are devices that convey data character-by-character rather than block-by-block. Examples of these types of devices are printers, keyboards, terminals, sound cards, etc. I can't think of a use case for any of these, but that doesn't mean there isn't one.

#### Command

    lxc config device add $ctr_name $dev_name unix-char source=/path/to/host/device path=/path/to/container/device

#### Example

    lxc config device add app1 tty42 source=/dev/tty42 path=/dev/tty1

The above will take `tty42` from the host system and pass it through to the container `app1` as `/dev/tty1`. Does it make sense to do that? Probably not, but you do you. It's your life. LIVE IT TO THE MAX!

[Apply the configuration to the container](#markdown-header-apply-configuration-changes-to-container)

### UNIX Block

The `unix-block` device type is similar to `disk`, but rather than sharing a directory, this is passing a block device to the container. The important distinction here is that the device is a volume rather than a directory within the volume. The device is added to the `/dev` directory on the container to be mounted within the container as appropriate.

#### Command

    lxc config device add $ctr_name $dev_name unix-block source=/path/to/host/device path=/path/to/container/device

#### Example

    lxc config device add app1 sdc5 unix-block source=/dev/sdc5 path=/dev/sda1

The above will take the unmounted volume `/dev/sdc5` on the host system and add to the `app1` container as `/dev/sda1`.

[Apply the configuration to the container](#markdown-header-apply-configuration-changes-to-container)

### USB

The `usb` device type is pretty self-explanitory: it takes a physical USB device and passes it through to the container rather than using it locally on the host system. The neat thing about `usb` devices is that they support hotplugging by default; if the device is removed and reattached at a later point, the device will automatically be attached to the container. Neat! **NOTE!** If the USB device uses a kernel driver, it will be more efficient to locate the device added in `/dev` and attach it as a [unix-block](#markdown-header-unix-block) or [unix-char](#markdown-header-unix-char) device as appropriate.

#### Commmand

    lxc config device add $ctr_name $dev_name usb vendor_id=$vendorid product_id=$productid

#### Example

Before looking at an example command, we're going to have to do some homework to look up values to pass to the command. To find the appropriate values, let's take a look at what USB devices I have plugged in at the moment:

    host# lsusb
    Bus 007 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
    Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    Bus 006 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
    Bus 005 Device 003: ID 046d:c52b Logitech, Inc. Unifying Receiver
    Bus 005 Device 002: ID 045e:028e Microsoft Corp. Xbox360 Controller
    Bus 005 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    Bus 004 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
    Bus 003 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub

Not a lot that would make sense to pass through to a container, but let's say for some reason I want to pass my XBOX controller through to the container. The command would look something like this:

    lxc config device add app1 xbox usb vendor_id=045e product_id=028e

This creates a device called `xbox` and attaches to the container `app1` if the product has the vendor_id `045e` and the product_id `028e`. These vaules are pulled from the ID in the above `lsusb` output where the number before the colon is the vendor and the number following the colon is the product.

[Apply the configuration to the container](#markdown-header-apply-configuration-changes-to-container)

### GPU

The `gpu` device type passes a graphic card through to the container in the event that some heavy computation is required (think cryptocurrency mining or participating in SETI or folding@home).

#### Command

    lxc config device add $ctr_name $dev_name gpu vendorid=$vendorid productid=$productid

#### Example

Let's start by finding the vendor and product IDs of the GPU we want to pass through:

    root@host# lspci -nn | grep -i vga
    0f:00.0 VGA compatible controller [0300]: NVIDIA Corporation GF100GL [Quadro 4000] [10de:06dd] (rev a3)

Now let's configure attach the physical device to the container:

    root@host# lxc config device add app1 quadro gpu vendorid=10de productid=06dd

This creates a device called `quadro` and attaches to the container `app1`. I identifies the physical device via the vendor ID `10de` (NVIDIA) and the productid `06dd`.

[Apply the configuration to the container](#markdown-header-apply-configuration-changes-to-container)

### Infiniband

If you have a use-case for connecting infiniband devices to containers, you're probably smarter than me so I won't bother trying to mansplain.

### Proxy

Proxy devices are a neat option to allow the container to bind to a port on the host systems. For example, if a container is running NGINX but the LXD server is using the built-in bridge, the container can bind the host system's port 80/443 directly to 80/443 on the container itself. Prior to the addition of the proxy device type, this type of setup required manually configuring iptables to perform a destination NAT to re-write the IP header; this feature will actually bind to the IP and port rather than mangle the incoming packet. This is a feature that has been available in Docker for a long time and is a welcome addition.

#### Command

    lxc config device add $ctr_name $devname proxy connect=$host_ip:$host_port listen=$ctr_ip:$ctr_port

#### Example

    lxc config device add nxing1 tcp_443 proxy connect=0.0.0.0:443 listen=0.0.0.0:443

The above example adds a proxy device named `tcp_443` to the container `nginx1`. The container is listening on all ports to TCP port 443, and binds to all IP addresses on the host system.

This can be verified with the following:

    host# sudo ss state listening sport = :443
    Netid              Recv-Q               Send-Q                               Local Address:Port                                Peer Address:Port
    tcp                0                    128                                               *:443                                           *:*

[Apply the configuration to the container](#markdown-header-apply-configuration-changes-to-container)


## Removing Devices from a Container

    lxc config device remove $ctr_name $devname

[Apply the configuration to the container](#markdown-header-apply-configuration-changes-to-container)

## Verifying Device Configuration for a Container

    lxc config device show $ctr_name

## Apply Configuration Changes to Container

    lxc restart $ctr_name
