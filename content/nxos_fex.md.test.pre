Title: Fabric Extender (FEX)
Date: 2017-02-24 12:11
Category: Network
Tags: network, nx-os, fex
Authors: Eric Rochow
Summary: An overview of fabric extenders

# Fabric Extender (FEX)

## Overview

The Cisco Nexus 2000 line of switches are known as Fabic Extenders (or FEXes). Fabric extenders act as remote line cards that are controlled by aggregation switches. The FEX is assigned an ID betweeen 100 and 199 and the FEX shows up as being in that slot. As of writing the Nexus 5000-, 6000-, 7000-, and 9000-series switches are capable of aggregating FEXes.

It is possible to dual-home a FEX to a pair of aggregation switches and have the configuration of the FEX synchronized between the two aggregation switches.

## Base Configuration

On the aggregation switch, enter the following configuration:

    agg-sw01(config)# feature fex
    agg-sw01(config)# interface e1/1
    agg-sw01(config-if)# channel-group 101
    agg-sw01(config)# interface po101
    agg-sw01(config-if)# switchport mode fex-fabric
    agg-sw01(config-if)# fex associate 101

At this point the connected FEX should upgrade its software to match that of the aggregation switch and reboot. The interfaces on the FEX should show up on the aggregation switch as soon as the reboot completes.

## Dual-Homing Configuration

### Configure CFS for FEX Config Sync

Since we will be using multiple aggregation switches to manage a single device, we will need to configure CFS distribution to distribute the config changes to the sister device:

    agg-sw01(config)# cfs ipv4 distribute
    agg-sw01(config)# end
    agg-sw01# configure sync
    agg-sw01(config-sync)# switch-profile PROFILE
    agg-sw01(config-sync)# sync-peers destination 10.x.y.2
    agg-sw01(config-sync)# end

    agg-sw02(config)# cfs ipv4 distribute
    agg-sw02(config)# end
    agg-sw02# configure sync
    agg-sw02(config-sync)# switch-profile PROFILE
    agg-sw02(config-sync)# sync-peers destination 10.x.y.1
    agg-sw02(config-sync)# end

### Configure FEX Fabric Interfaces

Configuration of dual-homed FEXes is similar to single-homed FEXes with a few extra steps. Assuming the two aggregation switches have been configured as a vPC pair, the following configuration is required on the first aggregation switch:

    agg-sw01(config)# feature fex
    agg-sw01(config)# interface e1/1
    agg-sw01(config-if)# channel-group 101
    agg-sw01(config)# interface po101
    agg-sw01(config-if)# vpc 101
    agg-sw01(config-if)# switchport mode fex-fabric
    agg-sw01(config-if)# fex associate 101

Next, configure the following on the second aggregation switch:

    agg-sw02(config)# feature fex
    agg-sw02(config)# interface e1/1
    agg-sw02(config-if)# channel-group 101
    agg-sw02(config)# interface po101
    agg-sw02(config-if)# vpc 101
    agg-sw02(config-if)# switchport mode fex-fabric
    agg-sw02(config-if)# fex associate 101

Before connecting the FEX to either aggregation switch, we will want to pre-provision the slot as the FEX configuration cannot be synced to the other switch if the configuration does not already exist.

### Preprovisioning Fabric Extenders

    agg-sw01(config)# slot 101
    agg-sw01(config-slot)# provision model n2k-n2348tq

    agg-sw02(config)# slot 101
    agg-sw02(config-slot)# provision model n2k-n2348tq

### Distributing Config Changes

To keep changes consistent between the pair of aggregation switches, make sure that changes are configured using the CFS profile configured ealier rather than in standard config mode:

    agg-sw01# config sync
    agg-sw01(config-sync)# switch-profile PROFILE
    agg-sw01(config-sync-sp)# interface e101/1/1
    agg-sw01(config-sync-sp-if)# desc Server1
    agg-sw01(config-sync-sp-if)# switchport mode access
    agg-sw01(config-sync-sp-if)# switchport access vlan 55
    agg-sw01(config-sync-sp-if)# no shutdown
    agg-sw01(config-sync-sp-if)# exit

The configuration has not taken effect yet, but before the configuration is configured, it should be verified to make sure there are not inconsistencies:

    agg-sw01(config-sync-sp)# verify
    Verification Successful

If the verification is not successful, then some troubleshooting steps will need to be taken. Otherwise, it is time to commit the changes.

    agg-sw01(config-sync-sp)# commit
    Verification successful...
    Proceeding to apply configuration. This might take a while depending on amount of configuration in buffer.
    Please avoid other configuration changes during this time.
    Commit Successful

