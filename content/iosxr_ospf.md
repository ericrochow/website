Title: OSPF in IOS-XR
Date: 2019-09-06 14:34
Category: Network
Tags: ospf, routing, ios-xr, network, cli
Authors: Eric Rochow

# OSPF
****

OSPF configuration in IOS-XR is very similar to IOS.

   RP/0/0/CPU0:router(config)#router ospf 1
   RP/0/0/CPU0:router(config-ospf)#router-id 172.31.0.2
   RP/0/0/CPU0:router(config-ospf)#area 0
   RP/0/0/CPU0:router(config-ospf-ar)#interface Loopback0
   RP/0/0/CPU0:router(config-ospf-ar-if)#exit
   RP/0/0/CPU0:router(config-ospf-ar)#interface GigabitEthernet0/0/0/0
   RP/0/0/CPU0:router(config-ospf-ar-if)#network point-to-point
   RP/0/0/CPU0:router(config-ospf-ar-if)#exit
   RP/0/0/CPU0:router(config-ospf-ar)#interface GigabitEthernet0/0/0/1
   RP/0/0/CPU0:router(config-ospf-ar-if)#network point-to-point
   RP/0/0/CPU0:router(config-ospf-ar-if)#exit
   RP/0/0/CPU0:router(config-ospf-ar)#interface GigabitEthernet0/0/0/2
   RP/0/0/CPU0:router(config-ospf-ar-if)#network point-to-point
   RP/0/0/CPU0:router(config-ospf-ar-if)#exit
