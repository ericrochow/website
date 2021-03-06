Title: IOS-XR ACLs
Date: 2019-09-06 14:34
Category: Network
Tags: network, acl, ios-xr, network
Authors: Eric Rochow

# ACLs

## Configure

### IPv4

#### Create ACL

IPv4 ACL configuration in IOS XR is pretty similar to IOS::

    RP/0/0/CPU0:router(config)#ipv4 access-list TEST
    RP/0/0/CPU0:router(config-ipv4-acl)#remark FIRST
    RP/0/0/CPU0:router(config-ipv4-acl)#permit icmp any any echo
    RP/0/0/CPU0:router(config-ipv4-acl)#permit icmp any any echo-reply 
    RP/0/0/CPU0:router(config-ipv4-acl)#permit icmp any any ttl-exceeded 
    RP/0/0/CPU0:router(config-ipv4-acl)#permit icmp any any unreachable  
    RP/0/0/CPU0:router(config-ipv4-acl)#permit icmp any any packet-too-big 
    RP/0/0/CPU0:router(config-ipv4-acl)#deny icmp any any 
    RP/0/0/CPU0:router(config-ipv4-acl)#exit
    RP/0/0/CPU0:router(config)#commit 

#### Apply ACL

The ACL can then be applied to an interface with the following::

    RP/0/0/CPU0:router(config)#interface g0/0/0/0
    RP/0/0/CPU0:router(config-if)#ipv4 access-group TEST ingress

#### Implicit Entries

Every IPv4  ACL in IOS XR has the following implicit statement as its last match entry::

    deny ipv4 any any

The ACL must have at least one (1) explicit entry for the implicit ``deny ipv4 any any`` statement to take effect.

### IPv6

#### Create ACL

IPv6 ACL configuration in IOS XR is pretty similar to IOS::

    RP/0/0/CPU0:router(config)#ipv6 access-list TEST6
    RP/0/0/CPU0:router(config-ipv6-acl)#remark FIRST!
    RP/0/0/CPU0:router(config-ipv6-acl)#permit icmp any any echo
    RP/0/0/CPU0:router(config-ipv6-acl)#permit icmp any any echo-reply 
    RP/0/0/CPU0:router(config-ipv6-acl)#permit icmp any any ttl        
    RP/0/0/CPU0:router(config-ipv6-acl)#permit icmp any any ttl-exceeded 
    RP/0/0/CPU0:router(config-ipv6-acl)#permit icmp any any unreachable  
    RP/0/0/CPU0:router(config-ipv6-acl)#permit icmp any any packet-too-big 
    RP/0/0/CPU0:router(config-ipv6-acl)#deny icmp any any 
 
#### Apply ACL

The ACL can then be applied to an interface with the following::

    RP/0/0/CPU0:router(config)#interface g0/0/0/0
    RP/0/0/CPU0:router(config-if)#ipv4 access-group TEST6 egress

#### Implicit Entries

Every IPv6 ACL in IOS XR has the folling implicit statements as its last match entries::

    permit icmp any any nd-na
    permit icmp any any nd-ns
    deny ipv6 any any

The first two entries allow for ICMPv6 neighbor discovery by default. The ACL must have at least one (1) explicit entry for the implicit ``deny ipv6 any any`` statement to take effect.

## Hardware Counters

Hardware counters are disabled by default for IPv4. They can be enabled per-interface and per-ACL using the following::

    RP/0/0/CPU0:router(config)#interface *interface-name*
    RP/0/0/CPU0:router(config-if)#ipv4 access-group *acl-name* { ingress | egress } hardware-count 

