Title: Virtual Port-Channel
Date: 2017-02-24 12:11
Category: Network
Tags: network, nx-os, vpc
Authors: Eric Rochow
Summary: An overview of the Virtual Port-Channel protocol

# Virtual Port-Channel

## Overview

Virtual Port-Channels (vPCs) allow links from two separate Cisco Nexus switches to appear as a single Port Channel to a third device (regardless of the operating system of the third device as long as the device supports LACP). This can be useful for Top of Rack (ToR) switches that are connected via layer 2 to a redundant pair of Nexus switches as it eliminates STP blocked ports.

### Basic Concepts and Terms

**vPC Domain**:  Pair of Nexus switches cooperating to form the vPC

**vPC Peer Keepalive**:  Layer 3 link between the two Nexus switches used to send ICMP heartbeats

**vPC Peer Link**:  Layer 2 link between the two nexus switches used to synchronize ARP and ND tables

**vPC Member Port**:  One of a set of ports to form vPC

**vPC VLAN**: Any VLAN carried over the vPC Peer Link (all VLANs by default)

**Orphan Device**: A device on a vPC VLAN but only connected to a single vPC peer device

**Orphan Port**: An interface that connects to an Orphan device

**Cisco Fabric Services (CFS)**: The underlying protocol running across the vPC peer-link providing reliable sychnronization and consistency check mechanisms between the two peer devices

### Benefits

* vPC loop avoidance is performed at the data-plane layer, which means that it is handled in hardware vs. STP which is handled at the control plane layer which is performed in software. Since all ToR switches would use port channels, individual link failures would not result in TCN BPDUs and, thus, would reduce CPU load on all switches in the layer 2 domain.

### Limitations

* vPC domains are limited to two devices.

### Requirements

*  vPC was introduced in NX-OS 4.1.3 and is included in all later versions.

*  vPC, HSRP, VRRP, and LACP are all included with the base NX-OS software license.

## Basic Step-by-step Configuration

First, enable the vPC feature on both switches:

    switch1(config)# feature vpc
    switch1(config)# feature lacp
    switch2(config)# feature vpc
    switch2(config)# feature lacp

Now, create the peer-keepalive port. At this point, we have a decision - we can either use the management port on the supervisor or we can use a port-channel between the vPC switches. For more info, see "Important Design Considerations". For this example, we are going to use the management ports:

    switch1(config)# interface mgmt0
    switch1(config-if)# ip address 1.1.1.1/24

    switch2(config)# interface mgmt0
    switch2(config-if)# ip address 1.1.1.2/24

Next create the vPC domain each switch:

    switch1(config)# vpc domain 1
    switch1(config-vpc-domain)# ip arp synchronize
    switch1(config-vpc-domain)# ipv6 nd synchronize
    switch1(config-vpc-domain)# peer-keepalive destination 1.1.1.2 source 1.1.1.1

    switch2(config)# vpc domain 1
    switch2(config-vpc-domain)# ip arp synchronize
    switch2(config-vpc-domain)# ipv6 nd synchronize
    switch2(config-vpc-domain)# peer-keepalive destination 1.1.1.1 source 1.1.1.2

Note that the `peer-keepalive` configuration defaults to using the management VRF. If not using the management port, the VRF must be specified by appending `vrf default` after the source (or substituting the actual VRF name if you specified a vPC keepalive VRF).

Time to create the peer link:

    switch1(config)# interface po1
    switch1(config-if)# switchport
    switch1(config-if)# switchport mode trunk
    switch(config-if)# vpc peer-link

    switch2(config)# interface po1
    switch2(config-if)# switchport
    switch2(config-if)# switchport mode trunk
    switch2(config-if)# vpc peer-link

And now we can configure the switches as peer switches and peer gateways:

    switch1(config)# vpc domain 1
    switch1(config-vpc-domain)# peer-switch
    switch1(config-vpc-domain)# peer-gateway

    switch2(config)# vpc domain 1
    switch2(config-vpc-domain)# peer-switch
    switch2(config-vpc-domain)# peer-gateway

The `peer-gateway` feature will allow both switches to forward traffic without having it cross the the peer-link regardless of the switch's HSRP role (i.e. it creates "Active/Active" HSRP). The `peer-switch` feature ensures that all BPDUs sent by the switch to vPC members will be identical to the peer switch's BPDUs so the vPC member sees the upstream switches as a single switch. 

Last, create the port channel by adding the port(s) to it on each switch and specifying a vPC ID:

    switch1(config)# interface ethernet 1/1
    switch1(config-if)# switchport
    switch1(config-if)# switchport mode trunk
    switch1(config-if)# channel-group 100 mode active
    switch1(config-if)# exit
    switch1(config-if) interface po100
    switch1(config-if)# vpc 100

    switch2(config)# interface ethernet 1/1
    switch2(config-if)# switchport
    switch2(config-if)# switchport mode trunk
    switch2(config-if)# channel-group 100 mode active
    switch2(config-if)# exit
    switch2(config-if) interface po100
    switch2(config-if)# vpc 100

## All Together Now

    switch1(config)# feature vpc
    feature lacp
    interface mgmt0
    ip address 1.1.1.1/24
    vpc domain 1
    ip arp synchronize
    ipv6 nd synchronize
    peer-keepalive destination 1.1.1.2 source 1.1.1.1
    interface po1
    switchport
    switchport mode trunk
    vpc peer-link
    vpc domain 1
    peer-switch
    peer-gateway

    switch2(config)# feature vpc
    feature lacp
    interface mgmt0
    ip address 1.1.1.2/24
    vpc domain 1
    ip arp synchronize
    ipv6 nd synchronize
    peer-keepalive destination 1.1.1.1 source 1.1.1.2
    interface po1
    switchport
    switchport mode trunk
    vpc peer-link
    vpc domain 1
    peer-switch
    peer-gateway

## Advanced vPC Configuration

### Peer Keepalive on Port Channel

If you decide to use a non-management port, the vPC peer-keepalive can be configured on a port-channel like so:

    switch1(config)# interface po1
    switch1(config-if)# vrf member peer-keepalive
    switch1(config-if)# ip address 1.1.1.1/24
    switch1(config-if)# exit
    switch1(config)# vpc domain 1
    switch1(config-vpc-domain)# peer-keepalive destination 1.1.1.2 source 1.1.1.1 vrf peer-keepalive

    switch2(config)# interface po1
    switch2(config-if)# vrf member peer-keepalive
    switch2(config-if)# ip address 1.1.1.1/24
    switch2(config-if)# exit
    switch2(config)# vpc domain 1
    switch2(config-vpc-domain)# peer-keepalive destination 1.1.1.1 source 1.1.1.2 vrf peer-keepalive

### vPC Role Priorities

It is possible to define a primary and secondary role for vPC by applying a (non-preemptive) priority value. Since vPC is a layer 2 technology, the lower priority wins. 

    switch1(config)# vpc domain 1
    switch1(config-vpc-domain)# role priority 100

    switch2(config)# vpc domain 1
    switch2(config-vpc-domain)# role priority 120

It is a good idea to configure the vPC primary device to be the same as the STP root unless the `peer-switch` command is used, in which case both devices will use the same spanning-tree priority and this recommendation does not apply.

### vPC System Priorities

When configuring a vPC using LACP, the vPC system priority can be confgured to ensure that the vPC devices act as the primary devices in LACP:

    switch1(config)# vpc domain 1
    switch1(config-vpc-domain)# system-priority 4000

    switch2(config)# vpc domain 1
    switch2(config-vpc-domain)# system-priority 4000

When manually configuring the system priority, make sure to set both devices are set to the exact same priority.

## Important Design Considerations

1.  vPC domains need to specific within a layer 2 domain. This is less important when all north-bound connections from the vPC pair are layer 3 connections, but when using FabircPath, it is important to have non-overlapping vPC domain names.
2.  The decision over whether to use the management interface on the supervisor or a port-channel for the peer-keepalive link depends on a few variables. Obviously, if the management port on the supervisor is already in use for out-of-band management, it will not be available to use as a keepalive port. Additionally, if vPC is being configured between a pair of 7k chassis with redundant supervisors, using the management port (at least while directly connected from management port to management port), a supervisor failover can cause a split-brain scenario as each switch will think it is the only active switch. In these cases, the preferred configuration would be to use a port-channel between the vPC switches. If desired, it is possible to create a VRF specifically for vPC keepalive purposes. With this type of configuration, the VRF needs to be specified on the keepalive port-channel and in the peer-keepalive statement in the `vpc domain` stanza (even if the VRF is the default VRF).
3.  vPC peer-links need to be specified on a port-channel (regardless of the number of links bundled in the port-channel).

## Best Practices



## vPC Troubleshooting

If vPC issues are suspected, first try issuing the `show vpc brief` command. This will give your a summary whether an adjacency is formed, whether the peer-link is up, and whether there are any consistency issues.

Check the vPC role with `show vpc role`.

If the previous commands looks OK, try `show vpc consistency-parameters interface <interface-name>`, where `<interface-name>` is the name of the interface that is experiencing issues. The values under `Local Value` and `Peer Value` should match. If they do not, it indicates an interface-level configuration issue.

## 4 Moar Infoz

* http://www.cisco.com/c/dam/en/us/td/docs/switches/datacenter/sw/design/vpc_design/vpc_best_practices_design_guide.pdf
