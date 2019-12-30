Title: BGP in IOS-XR
Date: 2019-09-06 14:34
Category: Network
Tags: iox-xr, bgp, cli
Authors: Eric Rochow
Summary: A basic how-to to get up-and-running with BGP on IOS-XR

# BGP

* Configure a route policy (at least a pass-all RPL).
* Configure BGP with the ASN and networks to be advertised::

   RP/0/0/CPU0:router(config)# router bgp 65535
   RP/0/0/CPU0:router(config-bgp)# address-family ipv4 unicast
   RP/0/0/CPU0:router(config-bgp-af)# network 192.0.2.0/24

* Configure the neighbor::

   RP/0/0/CPU0:router(config-bgp)# neighbor 172.31.0.5
   RP/0/0/CPU0:router(config-bgp-nbr)# remote-as 65533
   RP/0/0/CPU0:router(config-bgp-nbr)# update-source Looback0
   RP/0/0/CPU0:router(config-bgp-nbr)# address-family ipv4 unicast
   RP/0/0/CPU0:router(config-bgp-nbr-af)# route-policy pass-all in
   RP/0/0/CPU0:router(config-bgp-nbr-af)# route-policy pass-all out

* Commit the configuration

Further customization is possible via route policies.

