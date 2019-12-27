Title: FabricPath
Date: 2019-09-06 14:34
Category: Network
Tags: network, nx-os, fabricpath, reference
Authors: Eric Rochow
Summary: Overview of the FabricPath protocol

# FabricPath

## FabricPath Principles

### What is FabricPath?

FabricPath is a Cisco-proprietary, TRILL-based layer 2 [^osi] technology that allows VLANs to span across multiple pods/sections within a datacenter utilizing a Clos (spine-and-leaf) architecture that would have traditionally been routed previously (in a traditional campus architecture). 

### How does FabricPath Work?

FabricPath creates a "routing table" of switch IDs using IS-IS as a control plane distributed among all switches in the FabricPath domain. FabricPath then creates a Multi-Destination Tree (MDT) which determines how traffic flows across the fabric without involving Spanning Tree but still allowing for layer 2 multipathing (ECMP). Use of the layer 2 TCAM is minimized by the use of conversational MAC learning wherever possible (basically all switches involved that are not routing the VLANs due to ARP/ND) which only stores the MAC address during active flows.

### FabricPath Requirements

As mentioned previously, FabricPath is Cisco-proprietary which means that it will not work in a mixed-vendor environment. [^proprietary] Also worth noting is that it is only available on the Nexus 5k/6k/7k platform. It is supported on the Nexus 2k platform as well via Fabric Extenders (FEX) as long as the aggregation switch supports FabricPath. When using the Nexus 7k, only F-series modules are supported. F2 and F2e allow for M-series modules to be in the same VDC; however F3 modules will not allow M-series modules in the same VDC when utilizing FabricPath. [^hardware]

FabricPath requires the Enhanced Layer 2 license on the chassis. Free trials 120 trials are possible via the "grace period" feature. The list price on this license is about $20k, and do not expect a deeper discount than your organization's standard discount off list unless ordering with hardware. Cisco makes it very difficult to discount licenses, but a deeper discount is possible on hardware when ordering licensing so plan ahead when making and order for a FabricPath network.

### FabricPath, Spanning-Tree, and YOU!

While FabricPath helps get around the limitations imposed by spanning-tree, the FabricPath proecess has to be running in order to not be sending regular STP BPDUs between the switches. This means that in the event of a switch reload or some other operation that causes the FabricPath feature to break in some way, the switch will flood BPDUs like a traditional spanning-tree device with a bridge ID being its own system MAC address rather than the common FabricPath bridge ID until the switch becomes active in FabricPath. When vPC+ is not being utilized, this opens the door to superior BPDUs being transmitted which can generate `*L2GW_Inc` state on Classical Ethernet switches. For this reason, it is important to configure spanning-tree root priority on all FabricPath edge switches with `spanning-tree pseudo-information` when not utilizing vPC+.

## FabricPath Configuration

### Easy Mode

The base FabricPath configuration is actually pretty basic. First, install and add the the feature-set:

    switch(config)# install feature-set fabricpath
    switch(config)# feature-set fabricpath

Next, configure the FabricPath switch-id and basic domain settings:

    switch(config)# fabricpath switch-id 101
    switch(config)# fabricpath domain default
    switch(config-fabricpath-isis)# root-priority 64

Even though FabricPath is a layer 2 technology, higher priority wins [^priority]. (If I had to venture a guess, I would say it's because FabricPath is using IS-IS, which is a layer 3 routing protocol.) You will want to make sure that your leafs have a lower priority than your spines.

After doing the same on the other leafs and the spines, configure your links as `switchport mode fabricpath` and allow them to come up and form IS-IS adjacencies:

    switch(config)# interface ethernet1/1
    switch(config-if)# switchport mode fabricpath

After the adjancies have formed, convert the VLAN(s) that will be utilizing FabricPath to be FabricPath-enabled:

    switch(config)# vlan 15-17 , 20 , 22 - 27
    switch(config-vlan)# mode fabricpath

### Advanced

It is possible to go beyond the base configuration to customize FabricPath to your network or needs. 

#### Spanning-Tree

I know, "eww". The fact remains that FabricPath is not the first protocol to come up and form adjacencies, so to avoid problems it is best to configure all edge switches as the spanning-tree root. 

If using MSTP:

    switch(config)# spanning-tree mst 1 priority 8192
    switch(config)# spanning-tree pseudo-information
    switch(config-pseudo)# mst 1 root priority 4096

If using PVST (or any varient thereof):

    switch(config)# spanning-tree vlan 15-17 , 20 , 22 - 27 priority 8192
    switch(config)# spanning-tree pseudo-information
    switch(config-pseudo)# vlan 15-17 , 20 , 22 - 27 root priority 4096

In either case, make sure that the "pseudo" root priority is lower than the value in the traditional spanning-tree configuration to avoid superior BPDUs from being sent by devices that have not started the FabricPath process.

#### vPC+

If you were already running vPC, it is possible to migrate to vPC+ (vPC with extensions to use along with FabricPath). All this migration requires is to specify a virtual switch id to be shared between the vPC pair and to change the port-channel that is being used as the vPC peer-link from `switchport mode trunk` to `switchport mode fabricpath`:

    switch(config)# vpc domain 1
    switch(config-)# fabricpath switch-id 1001
    switch(config)# interface po1
    switch(config-if)# vpc peer-link
    switch(config-if)# switchport mode fabricpath

**Important caveats**: It is not possible to run both vPC and vPC+ on the same VDC. This means that if you are planning to utilize FabricPath for only certain VLANs and have the rest remain Classical Ethernet VLANs, traffic will not work as expected or intended - especially when utilizing a first-hop redundancy protocol. Also important to note is that this will cause the link to flap, so any FHRP adjacencies will need to reform.

#### Anycast HSRP

One of the design considerations of a FabricPath network is where to place the layer 3 gateways. In smaller networks, SVIs can be placed on the spines, in others a dedicated pair of leafs can be used to connect the FabricPath network to the rest of the network (i.e. border leafs), or the SVIs can be placed on the leafs. The first option can lead to scalability issues as the spines would need to learn the MAC addresses of every device on the FabircPath network due to ARP (IPv4) and ND (IPv6) In addition, to gain access to the dual-active HSRP functionality, vPC+ will need to be enabled *regarless of whether there are any vPC ports on the spines* (which there almost certainly would not be if designed properly). In the last option, once of the concerns could be traffic tromboning due to the SVIs only being Active in HSRP on one pair of leafs. Enter Anycast HSRP!

Anycast HSRP will allow you to run essentially dual-dual-active HSRP on two sets of leafs. Like with vPC+, an emulated switch ID (known as an Ancast Switch ID or ASID) is specified to be shared by all switches participating in Anycast HSRP. The ASID will be advertised like a normal switch ID and IS-IS calculates the shortest path to the gateway. The configuration looks something like this:

    hsrp anycast 4 ipv4
    switch-id 2001
    vlan 15 - 17 , 20 , 22 - 27
    priority 110
    no shutdown
    !
    hsrp anycast 6 ipv6
    switch-id 2001
    vlan 15 - 17 , 20 , 22 - 27
    priority 110
    no shutdown

In the above example, the `4` and `6` are the names of the HSRP bundles. They are arbitrary, but give them names that make sense. In this case 4 is used for IPv4 and 6 is used for IPv6.

The rest of the HSRP configuration is a bit more stripped down as part of the configuration is already done and because of the dual-active nature which does not necessitate things like preemption:

    interface Vlan 15
    hsrp version 2
    hsrp 4
    ip 10.1.2.3/24
    hsrp 6
    ipv6 2601::1/64

Notice that HSRP version 2 is speicified - Anycast HSRP is only compatible with version 2.

**Important caveats**: In order to run Anycast HSRP, all switches participating in the FabricPath network must be running Anycast HSRP-capable software - on the Nexus 7k platform this would mean 6.2(2)+. For this reason, it is important to keep NX-OS images consistent. In NX-OS the limit of forwarders is 4 switches [^ahsrp], though this limit may be raised with future NS-OS releases. Prior to NX-OS 6.2(8), the ASID will be advertised even if the overload bit is set, which could incur a longer convergence times.

#### Overload Bit

As FabricPath rides on top of IS-IS, it can use the the `overload bit` feature of IS-IS [^overload_add], which allows the router (or switch in this case) to alert other routers that it has run out of system resources (i.e. memory and/or CPU) and therefore route transit traffic around this switch but still send route traffic to networks directly connected to the switch [^overload_traffic]. It is possible to configure this manually in an emergency like so:

    fabricpath domain default
    set-overload-bit always

This is not a feature you would want to leave set. To delay convergence after the switch boots, a delay timer can be set as follows:

    fabricpatch domain default
    set-overload-bit on-startup 20

In the previous example, configuring `20` sets the delay to 20 seconds after boot time. IS-IS allows 5-86400 seconds for this field.

#### Authentication

As with most routing protocols, it is possible to require authentication on FabricPath links. To do this, first configure a key-chain like you would with EIGRP:

    key chain fabricpathkeys
    key 1
    key-string iamatotallysecurekey
    accept-lifetime 01:00:00 April 1 2014 01:00:00 May 2 2014
    send-lifetime 01:00:00 April 1 2014 01:00:00 May 2 2014
    key 2
    key-string lastkeynotsosecureheresanewkey
    accept-lifetime 01:00:00 May 1 2014 infinite
    send-lifetime 01:00:00 May 1 2014 infinite

Next configure FabricPath to use the keychain:

    fabricpath domain default
    authentication-check
    authenticaiton key-chain fabricpathkeys
    authentication type md5

### Best Practices

* Assign a switch IDs manually. This will avoid any switch ID overlap (a BAD THING) and will allow you to set a switch ID scheme that makes sense for your network. Cisco suggests 2-digit IDs for the spines, 3-digit IDs for the leafs, and 4-digit IDs for virtual switches (anycast HSRP, vPC+, etc).

* Configure the multidestination tree root and (if applicable) use the multitopology feature. 

* Use a consistent VLAN configuration throughout your network.

* Use port channels between your spines and leafs (especially when using multiple physical links between each spine and leaf). This will allow for resilincy between each spine and leaf without the additional load of the added IS-IS calculations.

* Configure Active-Active default gateways using vPC+.

* Use caution when configuring fast convergence options. As with other routing protocols, it is possible to lower hello and SPF timers to speed up convergence; however doing so can increase the load on the hardware. Cisco recommends leaving IS-IS timers at their default values as by default FabricPath exponential LSP and SPF timers will react within a few milliseconds during times of stability and will lengthen during times of instability (e.g. when links are flapping).

* Configure the overload bit for graceful restarts. This can also be done automatically at boot to allow IS-IS adjacencies to form prior to advertising transit routes to other nodes.

* Use BFD for fast failover if a layer 1 device lies between your spine and leaf (as long as it is supported by your platform and version of NX-OS). 

### FabricPath Troubleshooting

Verify that your FabricPath interfaces are up:

    switch# show fabricpath topology interface 
    Interface           Topo-Description                 Topo-ID    Topo-IF-State
    ------------------- -------------------------------- ---------- -------------
    port-channel1       0                                0               Up   
    port-channel2       0                                0               Up   
    port-channel3       0                                0               Up   

Verify that the switch-ids are viewable:

    switch# show fabricpath isis route 
    Fabricpath IS-IS domain: default MT-0
    Topology 0, Tree 0, Swid routing table
    11, L1
     via port-channel2, metric 5
    12, L1
     via port-channel3, metric 5
    101, L1
     via port-channel2, metric 10
     via port-channel3, metric 10
    1001, L1
     via port-channel2, metric 10
     via port-channel3, metric 10


## Moar Infoz

* http://www.cisco.com/c/dam/en/us/products/collateral/switches/nexus-7000-series-switches/white_paper_c07-728188.pdf

### Footnotes

[^osi]: As with MPLS, there are arguments as to what layer on the OSI model FabricPath operates on. As IS-IS is used to "route" layer 2, the argument can be made that FabricPath is a layer 2.5 protocol. Really, it comes down to semantics.
[^proprietary]: At least at the spine and leaf layers. It is possible to hang other vendors' switches off of the leaf layer.
[^priority]: Default priority is 100.
[^overload_add]: As of 6.2(2)

[^hardware]: <https://supportforums.cisco.com/sites/default/files/attachments/discussion/2014-usa-pdf-brkdct-3407_0.pdf>
[^ahsrp]: <http://www.cisco.com/c/en/us/td/docs/switches/datacenter/sw/6_x/nx-os/fabricpath/configuration/guide/b-Cisco-Nexus-7000-Series-NX-OS-FP-Configuration-Guide-6x.pdf>
[^overload_traffic]: <http://www.cisco.com/c/en/us/support/docs/ip/integrated-intermediate-system-to-intermediate-system-is-is/24509-set-overload-bit.html>
