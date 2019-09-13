Title: Cisco Fabric Services
Date: 2017-02-24 12:11
Category: Network
Tags: network, nx-os
Authors: Eric Rochow
Summary: Overview of Cisco Fabric Services

# Cisco Fabric Services (CFS)

## Overview

Cisco Fabric Services (CFS) is used to distribute information such as configuration changes to Cisco Nexus devices.

### CFS-Supported Applications

| Application      | Default State |
| :--------------- | ------------: |
| Call Home        |  Disabled     |
| Device Alias     |  Enabled      |
| DPVM             |  Enabled      |
| FC domain        |  Disabled     |
| FC port security |  Disabled     |
| FC timer         |  Disabled     |
| IVR              |  Disabled     |
| NTP              |  Disabled     |
| RADIUS           |  Disabled     |
| RSCN             |  Disabled     |
| TACACS+          |  Disabled     |
| User roles       |  Disabled     |



### CFS Distribution Methods

- CFS over Ethernet (CFSoE) - Distributes over an Ethernet network
- CFS over IP (CFSoIP) - Distributes over an IPv4 network
- CFS over Fibre Channel (CFSoFC) - Distributes over a Fibre Channel, such as a virtual storage area network (VSAN). This is the default method if the device has been provisioned with Fibre Channel interfaces.


### CFS Distribution Modes

CFS supports three distribution modes; however only one mode can be configured at any given time. The following modes are supported:

- Uncoordinated distributions
 
 - Distribute information that is not expected to conflict with that from a peer
 - Parallel uncoordinated distributions are allowed for an application

- Coordinated distributions

 - Distribute information that can be manipulated and distributed from multiple devices (e.g. port security configuration)
 - Only one application distribution allowed at any given time
 - Consists of three stages:

  1. Network lock is acquired
  2. Configuration is distributed and committed
  3. Network lock is released

- Unrestricted uncoordinated distributions

 - Allow multiple parallel distributions in the network in the presence of an existing coordinated distribution

### CFS In a Mixed Fabric

CFS is available on the Nexus 5000, Nexus 7000, and MDS 9000 platforms. A mixed fabric can interact with each other using CFSoIP or CFSoFC (assuming the approriate FC of FCoE plugins installed and configured). It is worth noting that not all applications are compatible with the version of the same application running on a different platform.

### CFS Merge Support



### CFS Network Locks

When an application is configured for coordinated distributions using the CFS infrastructure, the application starts a CFS session and locks the network. While the network is locked, the software allows configuration only from the device holding the lock. An error message will occur if a change is attempted from another device; however the changes will be held in a pending database by the application.

If a CFS session that requires a network lock is opened but never closed, it is possible to clear the session. Network locks and the associated username are persistent across reboots and supervisor switchovers. Configuration attempts from other users will be rejected during a network lock.

### CFS Regions

CFS regions are user-defined subsets of devices for a given feature or application. Regions allow for localization or restriction of distribution based on devices that are close to one another. CFS regions are identified by numbers ranging from 0 to 200. Region 0 is reserved as the default region that contains every device in the network.

### High-availability CFS

CFS supports stateless restarts. The running configuration is applied after a reboot or supervisor switchover.

### CFS Virtualization Support

CFS is configured per-VDC; therefor it is important to make sure to `switchto` the appropriate VDC prior to configuration.

## Configuring CFS Distribution

### Enabling CFS By Application

Callhome:

    switch1(config)# callhome
    switch1(config-callhome)# distribute

Device Alias:

    switch1(config)# device-alias distribute

DPVM:

    switch1(config)# dpvm distribute

Fibre Channel Domain:

    switch1(config)# fcdomain distribute

Fibre Channel Port Security:

    switch1(config)# fc-port-security distribute

Fibre Channel Timers:

    switch1(config)# fctimer distribute

Inter-VSAN Routing:

    switch1(config)# ivr distribute

NTP:

    switch1(config)# ntp distribute

RADIUS:

    switch1(config)# radius distribute

RSCN:

    switch1(config)# rscn distribute

TACACS+:

    switch1(config)# tacacs+ distribute

User Roles:

    switch1(config)# role distribute

### Specify CFS Distribution Mode

CFSoE:

    switch1(config)# cfs eth distribute

CFSoIP:

    switch1(config)# cfs ipv4 distribute


### Configure an IP Multicast Address (CFSoIP)

The default multicast address for CFSoIP is 239.255.70.83. To change user another multicast address (e.g. 225.0.1.1):

    switch1(config)# no cfs ipvr distribute
    switch1(config)# cfs ipv4 mcast-address 225.0.1.1
    Distribution over this IP type will be affected
    Change multicast address for CFS-IP ?
    Are you sure? (y/n) [n] y
    cfs ipv4 distribute

Note that CFSoIP must be disabled globally before the multicast address can be changed.

### Configuring CFS Regions

#### Creating a CFS Region

To configure the switch for Call Home in region 4:

    switch1(config)# cfs region 4
    switch1(config-cfs-region)# callhome

#### Moving an Application to a Different Region

To move the previously configured Call Home application to region 2:

    switch1(config)# cfs region 2
    switch1(config-cfs-region)# callhome

#### Removing an Application from a Region

To remove Call Home from region 2:

    switch1(config)# cfs region 2
    switch1(config-cfs-region)# no callhome

#### Deleting a CFS Region

To delete CFS region 2:

    switch1(config)# no cfs region 2

### Creating and Distributing a CFS Configuration



### Clearing a Locked Session

To clear an open session for NTP:

    switch1(config)# clear ntp session

### Discarding a Configuration

To discard any configuration changes and release the lock for ntp:

    switch1(config)# ntp abort
    This will prevent CFS from distributing the 
    configuration to other switches.
    Are you sure? (y/n)  [n] y

### Disabling CFS Globally

    switch1(config)# no cfs distribute

## Troubleshooting CFS Distribution

Display status of CFS distribution on the device and IP distribution information:

    switch1# show cfs status

Display all applications that are currently CFS-enabled:

    switch1# show cfs application

Display CFS distribution status for a specified application (e.g. NTP):

    switch1# show ntp status

Display active locks:

    switch1# show cfs lock

Display all CFS peers in the physical fabric:

    switch1# show cfs peers

Display all applications with peers and region information:

    switch1# show cfs regions

Display merge status for a given application (e.g. NTP):

    switch1# show cfs merge status name ntp
