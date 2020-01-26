Title: LXD Networking
Date: 2019-09-06 14:34
Category: Containers
Tags: lxd, containers, linux, networking
Authors: Eric Rochow

# LXD Networking

Starting in LXD 2.3 there has been quite a bit of network functionality exposed to the operator. As before 2.3 there is the default `lxdbr0` bridge created when LXD is installed on the host system, but several other options exist.


## LXD Bridges

### Using the Default LXD Bridge

First things first, let's go over the default bidge and what it gives you. Out of the box, any new containers will be attached to this bridge and the host system will be configured to NAT oubound connections using the default IP address of the host system via iptables MASQUERADE rules. IP addresses will be assigned to new containers using a built-in DHCP server using the range provided during the LXD init process. If you're looking to keep things simple, just stick with the default bridge.


### Creating a Custom LXD Bridge

If for some reason the default bridge does not suffice (e.g. the network namespaces need to be segregated, differing requirements for addressing or NAT behavior, etc), it is possible to create a new bridge. There are a few different options for configuring a bridge.

To create an autoconfigured bridge named lxdbr1337:

    root@host# lxc network create lxdbr1337

To configure the bridge by hand:

    root@host# lxc network create lxdbr1337 ipv6.address=none ipv4.address=10.13.37.1/24 ipv4.nat=true

This will create a new bridge call `lxdbr1337` with IPv6 disabled and an IPv4 address of 10.13.31.1, will create MASQUERADE rules in iptables to NAT outbound traffic. The built-in DHCP server will hand out addresses to containers attached to the bridge from the range 10.13.37.0/24 (i.e. 10.13.31.2 - 254).

### Attach to a Bridge

So now we have an LXD bridge or two; how do we use it?

Let's attach the container `app1`'s eth0 to the host's bridge lxdbr1337:

    root@host# lxc network attach lxdbr1337 app1 eth0

Now let's restart the container to apply the new configuration and verify the bridge configuration on app1:

    root@host# lxc restart app1
    root@host# lxc info app1
    ... snip
    devices:
      eth0:
        ipv4.address: 10.13.37.224
        nictype: bridged
        parent: lxdbr1337
        type: nic
    ... snip

YAHTZEE

### Set Static IP

Now we have a new bridge and we have successfully attached a container to that bridge. The container successfully pulled an IP address from the DHCP pool and we should be able to NAT out to the Internet. What if we want to make 100% sure that the IP address never changes? This is where static IP addresses come in. One thing to note about static IP addresses on devices connected to an LXD bridge is that they are not actually static IP addresses; they are DHCP reservations. This has a few benefits:

* It avoids IP address conflicts as the DHCP server is aware the IP address is in use
* It allows the DHCP server to pass additional options to the container (e.g. gateway, DNS, NTP, etc values).


Let's add a "static" IP address to the container `app1`'s eth0 interface:

    root@host# lxc config device set app1 eth0 ipv4.address 10.13.37.66

Time to restart and verify the change:

    root@host# lxc restart app1
    root@host# lxc info app1
    ... snip
    devices:
      eth0:
        ipv4.address: 10.13.37.66
        nictype: bridged
        parent: lxdbr1337
        type: nic
    ... snip

This also works for IPv6 with the `ipv6.address` flag, but our bridge has IPv6 disabled.

### Port Security

There may be scenarios where there need to be security measures in place to avoid MAC address spoofing or to avoid forwarding traffic for other containers (e.g. nesting containers). The following will accomplish that:

    root@host# lxc config device set app1 eth0 security.mac_filtering true

### DNS

LXD runs a DNS server on the bridge, which allows the domain to be set via the `dns.domain` network property, and supports 3 different modes (via `dns.mode`):

* "managed" - one DNS record per container, matching its name and known IP addresses. This record cannot alter this record through DHCP.
* "dynamic" - containers can self-register through DHCP; the current hostname during DHCP negotiation is the domain name
* "none" - simple recursive DNS server with no local DNS records

The default mode is "managed"## External Briding

It's possible for the container to participate in the host's LAN as well using bridges outside the control of LXD, but at the expense of losing control of networking for the host through LXD itself. This means that things like DHCP, NAT, etc will also need to be handled external to LXD.

### Bridging with bridgeutils

Let's start with the most basic option using bridgeutils. Bridgeutils creates an internal switch on the host and attaches the configured hosted containers and the configured physical interface. There are a lot of other options, but they are not explicitly germain to the topic at hand. Let's start by crating a new bridge:

    root@host# brctl addbr lanbr

You've probably already deduced that we have created a new bridge named `lanbr`. Let's verify that:

    root@host# brctl show
    bridge name     bridge id               STP enabled     interfaces
    lanbr           8000.000000000000       no

Nice! There aren't any physical or logical interfaces attached to the bridge yet, so it's just chillin there waiting for some friends. Let's give him a physical friend:

    root@host# brctl addif lanbr enp4s0f0

This adds the physical interface `enp4s0f0` to the bridge. Don't believe me? See for yourself:

    root@host# brctl show lanbr
    bridge name     bridge id               STP enabled     interfaces
    lanbr           8000.00e0814cbc1c       no              enp4s0f0

Now we're getting somewhere. We still don't have any containers attached though. The default profile to which the container was attached uses the lxdbr0 interface, so we will need to override that inherited bridge for the eth0 interface on the container. Let's do that now:

    root@host# lxc config device override app1 eth0 parent=lanbr

Let's see what we're looking at now:

    root@host# lxc config device show app1
    eth0:
      nictype: bridged
      parent: lanbr
      type: nic
    root@host# brctl show lanbr
    bridge name     bridge id               STP enabled     interfaces
    lanbr           8000.00e0814cbc1c       no              enp4s0f0
                                                        vethce92439e

Awesome! So to recap, we have now created our bridge `lanbr` using the brctl interface to bridgeutils, added a physical interface to the bridge, then added a container to the bridge. There are a ton of other options available through bridgeutils like VLAN tagging, loop avoidance through STP, and more, but that goes way outside the scope of this discussion. Poke around and see what you can do!

### Bridging with macvlan

Say you don't need all the fancy knobs associated with bridgeutils and just want your containers to be able to interact directly with the LAN without worry of a layer 2 loop. Enter macvlan. Macvlan creates a trivial bridge and attach subinterfaces to that bridge. Subinterfaces use the naming convention of subint@int: e.g. `updog@enp3s0`, where `updog` is an arbitrary interface name and `enp3s0` is the parent interface to which the bridge is bound.


    root@host# lxc config device set app1 eth0 nictype=macvlan
    root@host# lxc config device set app1 eth0 parent=enp4s0f0
    root@host# lxc config device show app1
    eth0:
      nictype: macvlan
      parent: enp4s0f0
      type: nic

Restart the container and you'll be in business. There are a points of clarification that need to be made about macvlan to avoid pulling your hair out:

* Containers will not be able to communicate directly with the host via the physical interface to which the macsubinterface is bound
This means that if a container is using the hosts physical enp3s0 as a macvlan parent, the container will be limited in the ways in which the container can interact with the host; you will need a second physical interface up and running.
* Containers attached to a physical interface using macvlan share the fate of that interface.
If there are 10 containers on a host all using the same parent interface and that interface goes down, the entire bridge goes down. You may expect that inter-container traffic to continue uninterupted, but that bridging is performed by hairpinning traffic through the physical interface. Kind of hard to do when the interface is down!

### Bridging with openvswitch

Another option to provide host bridging is openvswitch. openvswitch is a virtual switch that comes with a whole host of nerd knobs you can tweak to your heart's content. You can even go buck wild by attaching vswitches from multiple hosts to an SDN controller (read: openflow). For this sake of brevity we will stick to creating a bridge and adding our container to the bridge tagged for a specified vlan.

#### Configuration

    root@host# ovs-vsctl add-br ctr-bridge
    root@host# ovs-vsctl add-port ctr-bridge enp4s0f1
    root@host# ovs-vsctl add-br vlan409 ctr-bridge 409
    root@host# lxc config device override app1 eth0 parent=vlan409

#### Explanation

Here we've created a bridge called `ctr-bridge` and assigned host interface `enp4s0f1` to the bridge. Next we've created a dummy bridge called `vlan409` that is tied to the parent bridge `ctr-bridge` and is tagged for, you guessed it, vlan 409. By attaching `enp4s0f1` to the parent bridge, it will act as a VLAN trunk as 802.1q behavior is the default in ovs vsiwtches. Any other devices also connected to the `vlan409` bridge will also be tagged as vlan 409.

## Tunnelling

At this point we've configured bridging a few different ways. Let's say we have configured additional hosts and we containers on those hosts to be able to talk to each other without any bridging to the external network or NAT-ing using an LXD bridge. This is where tunelling comes into play. If you've worked with networking in any way int the past... oh, say 10 years... it's probably safe to assume you've heard of overlay networking. This is overlay networking. BUZZWORDS!

### GRE Tunnelling

Generic Routing Encapsulation (GRE) provides a method to allow two networks to talk to each other that would not be able to otherwise. GRE takes the packet to be transmitted and wraps it inside a new header (i.e. encapsulates it) specifying the local router (in this case our local LXD host) as the source and the remote router (i.e. our remote LXD host) as the destination. When the GRE packet is received, it is decapsulated and routed as usual. This is very similar to VPNs, but it should be noted that GRE does *NOT* encrypt the payload like true VPNs (ipsec, openvpn, sslvpn, etc). If multiple hosts are participating via GRE, each endpoint will need to be configured on every other host.

#### Configuration

On host1:

    root@host1# lxc network set br0 tunnel.host2.protocol gre
    root@host1# lxc network set br0 tunnel.host2.id 10
    root@host1# lxc network set br0 tunnel.local 11.11.11.11
    root@host1# lxc network set br0 tunnel.remote 99.99.99.99

On host2:

    root@host2# lxc network set br0 tunnel.host1.protocol gre
    root@host2# lxc network set br0 tunnel.host1.id 10
    root@host2# lxc network set br0 tunnel.local 99.99.99.99
    root@host2# lxc network set br0 tunnel.remote 11.11.11.11

#### Explanation

On each host we're configuring the parameters for the other side along with the local IP address. This will allow the two hosts to understand the routing and be able to properly return the traffic.

### VXLAN Overlays

While GRE allows two networks to communicate where end-to-end communication wouldn't otherwise be possible, VXLAN instead allows those two networks to act as a single network. This means that a container on one host could use the other host as a gateway, or containers could be moved between the hosts without needing to change their IP addresses. This is a huge win when it comes to trying to cluster LXD hosts. There are two options when it comes to VXLAN networking in LXD: unicast and multicast. Unicast is going to look a lot like the GRE configuration above - we will explicitly define each endpoint. There is also an option to use multicast. The benefit of using multicast is that it will work without specifying each individual endpoint with one major caveat: they ALL have to be on the same layer 2 network. If you have a host in one datacenter and a host in another datacenter, multicast is not going to work (unless there are some major layer 2 shenanigans going on between datacenters).

#### Unicast

If the hosts do not have L2 connectivity between them, it is possible to create the tunnel in unicast mode.

On host1:

    root@host1# lxc network set br0 tunnel.host2.protocol vxlan
    root@host1# lxc network set br0 tunnel.host2.id 10
    root@host1# lxc network set br0 tunnel.local 11.11.11.11
    root@host1# lxc network set br0 tunnel.remote 99.99.99.99

On host2:

    root@host2# lxc network set br0 tunnel.host1.protocol=vxlan tunnel.host1.id=10 tunnel.host1.local=99.99.99.99 tunnel.host2.remote=11.11.11.11
    root@host2# lxc network attach-profile br0 default eth0

#### Multicast

In this example, we can configure host1 to route all of the traffic and allow containers to communicate between hosts, then configure host2 to tunnel all traffic to host1. Since this is multicast, it is dependent on L2 connectivity between the hosts.

First create the bridge on host1:

    root@host1# lxc network create br0 tunnel.lan.protocol=vxlan

Now attach the bridge to eth0 in the default profile:

    root@host1# lxc network attach-profile br0 default eth0

Then create the bridge on host2:

    root@host2# lxc network create br0 tunnel.lan.protocol=vxlan ipv4.address=none ipv4.address=none tunnel.lan.protocol=vxlan

Attach the bridge to eth0 in the default profile:

    root@host2# lxc network attach-profile br0 default eth0


### Fan Networking

Fan networking is another overly option. Without going into too much detail, a fan consists of an underlay network with a /16. The hosts in the underlay network pull IP addresss from the /16 and each provide a /24 from the same /8 network. For example, the fan may use an underlay network `172.21.0.0/15` and the overlay network `10.0.0.0/8`. The hosts are assigned addresses from the /16, so lets say host1 has the address 172.21.3.15 and host2 has the address 172.21.5.20. `host1` will then assign containers addresses from the range `10.3.15.0/24` and `host2` will assign containers the range from `10.5.20.0/24`. Notice the lower two octets of the underlay address are used as the second and third octets for the hosts range. Containers can move around to different hosts, but traffic will always route out through the original host. There's a lot to unpack when it comes to fan networking and we're only going to cover the basics, so if you're interested in learning more about fan networking, I would suggest giving [the fan networking docs](https://wiki.ubuntu.com/FanNetworking) a read.

#### Configuration

First we need to create the fan on our hosts:

    root@host1# fanctl up -o 10.0.0.0/8 -u 172.21.3.5/16

    root@host2# fanctl up -o 10.0.0.0/8 -u 172.21.5.20/16

Now lets verify the fans are configured:

    root@host1# fanctl show
    Bridge           Underlay             Overlay              Flags
    fan-10           172.21.3.5/16        10.0.0.0/8


    root@host2
    Bridge           Underlay             Overlay              Flags
    fan-10           17.21.5.20/16        10.0.0.0/8

Now that we have the fan interfaces defined we can update our default bridge to use the fans to overlay:

    root@host1# lxc profile device set default eth0 parent=fan-10
    root@host1# lxc profile device set default eth0 mtu=1498

    root@host2# lxc profile device set default eth0 parent=fan-10
    root@host2# lxc profile device set default eth0 mtu=1498

#### Explanation

On each host we have created a fan bridge with `10.0.0.0/8` as the overlay network and `172.21.0.0/16` as the underlay network. This makes the asusmption that both hosts have interfaces configured with addresses from the same /16 and that they are on the same layer 2 network segment. Once the fan has been verified, the parent device for the containers `eth0` can be set to the newly-created fan bridge and lower the MTU to account for encapsulation overhead (to prevent unnecessary fragmentation).


## vSwitches and controlers


### openvswitch




#### Configuration




#### Explanation
