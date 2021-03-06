Title: IOS-XR Licensing
Date: 2019-09-06 14:34
Category: Network
Tags: network, ios-xr, cli
Authors: Eric Rochow
Summary: Basic information on installing and applying licenses

# Licenses

## 32-bit IOS-XR

### Add a Perpetual License

On the chassis, find the appropriate license info. NOTE: You must be in ``admin`` mode to run this command:

    RP/0/RSP0/CPU0:router#admin
    Thu Mar 23 09:30:21.857 UTC
    RP/0/RSP0/CPU0:router(admin)#show license udi
    Thu Mar 23 09:30:25.285 UTC

    Local Chassis UDI Information:
      PID         : ASR-9904-AC
      S/N         : FOXXXXXXXXX
      Operation ID: 0

The PID and SN are needed to redeem the PAK.

SCP the file to the router.

Add the license (still in admin mode):

    RP/0/RSP0/CPU0:router(admin)#license add disk0a:/usr/FOXXXXXXXXX_20170323113900442.lic
    Thu Mar 23 09:41:34.745 UTC

    Info: License add successful for feature(s): "A9K-200G-IVRF"

    License command "license add disk0a:/usr/FOXXXXXXXXX_20170323113900442.lic sdr  Owner " completed successfully.

### Apply a Perpetual License

Verify the license is available:

    RP/0/RSP0/CPU0:router#show license available
    Thu Mar 23 09:51:27.512 UTC

    FeatureID: A9K-200G-IVRF (Slot based, Permanent)
      Total licenses 1
      Status: Available    1
        Pool: Owner
          Total licenses in pool: 1
          Status: Available    1

If this license is slot-based (and it is in this case), find the slot number for the card:

    RP/0/RSP0/CPU0:router#show inventory
    Thu Mar 23 09:50:35.761 UTC
    ....
    NAME: "module 0/0/CPU0", DESCR: "200G Modular Linecard, Packet Transport Optimized"
    PID: A9K-MOD200-TR, VID: V01, SN: FOC2035NWJV
    ....

In this case we know that we need 0/0/CPU0.

Drop into admin mode and apply the license to the slot:

    RP/0/RSP0/CPU0:router(admin-config)#license A9K-200G-IVRF location 0/0/CPU0

Commit the change.

NOTE: The license will not show active until 5 interfaces have been configured in separate VRFs. If fewer than five VRFs will be used, configuring dummy VRFs and rolling the configuration back will suffice.

## 64-bit IOS-XR
