Title: NX-OS Upgrades
Date: 2017-03-24 12:26
Category: Network
Tags: network, nx-os, upgrade
Authors: Eric Rochow
Summary: Upgrade Procedures for Nexus devices

# Nexus 3k/9k Upgrades

Upgrades from NX-OS 6 to 7 require an incremental upgrade due to BIOS incompatibilities. First install a compatible version of 6 that allows standalone BIOS upgrades:

    copy scp://user@server/root/n3000-uk9.6.0.2.U6.9.bin bootflash: vrf default
    copy scp://user@server/root/n3000-uk9-kickstart.6.0.2.U6.9.bin bootflash: vrf default
    install all kickstart bootflash:///n3000-uk9-kickstart.6.0.2.U6.9.bin system bootflash:n3000-uk9.6.0.2.U6.9.bin

This will take a long time and require a reboot. After the reboot, delete the old image to make room for the new images:

    delete bootflash:///n3000-uk9-kickstart.6.0.2.U3.1.bin
    delete bootflash:///n3000-uk9.6.0.2.U3.1.bin

Now it's time to install the BIOS upgrade to enable the upgrade to 7:

    copy scp://user@server/root/nxos-n3kbios.bin bootflash: vrf default
    install all nxos bootflash:///nxos-n3kbios.bin bios

It will say that a reboot is required, but it's not. Delete the BIOS bin file and do the final upgrade:

    delete bootflash:///nxos-n3kbios.bin
    copy scp://user@server/root/nxos.7.0.3.I4.4.bin bootflash: vrf default
    install all nxos bootflash:///nxos.7.0.3.I4.4.bin

After the reboot, you will be on 7. You will not need to jump through all these hoops for future upgrades.


# Nexus 7k Upgrades
