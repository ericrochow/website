Title: VRF on IOS
Date: 2019-09-06 14:34
Category: Network
Tags: network, ios, vrf, cli
Authors: Eric Rochow
Summary: Brief Summary of VRFs on IOS

# VRF

## Configure VRF

* Create the new VRF:

    ip vrf VRFNAME
     description This is your new vrf
     rd 65000:101

The `rd` is a route distinguisher in the form of an AS number and an arbitrary number (xxx:y) or an IP address and an arbitrary number ( x.x.x.x:y).

* Back up the interface config (not necessary if this is a new interface).
* Add interface to new VRF:

    interface Ethernet0/3
     ip vrf forwarding VRFNAME

* Re-add the interface configuration (ip address, etc.).
* Configure OSPF (or other IGP) to be VRF-aware:

    router ospf 101 vrf VRFNAME
     network 0.0.0.0 255.255.255.255 area 0

## Configure Inter-VRF Routing

* Create prefix list of routes to leak:

    ip prefix-list LEAK-TO-VRF seq 10 permit 172.16.0.0/20
    ip prefix-list LEAK-TO-VRF seq 20 permit 192.168.0.0/20
    ip prefix-list LEAK-TO-VRF seq 9001 deny 0.0.0.0/0 le 32

* Create a route-map to use the prefix list

    route-map IMPORT-FROM-GLOBAL permit 10
     match ip address prefix-list LEAK-TO-VRF

* Apply the route-map to the VRF:

    ip vrf scrubbed
     import ipv4 unicast map IMPORT-FROM-GLOBAL
