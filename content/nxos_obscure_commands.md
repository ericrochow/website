Title: Obscure NX-OS Commands
Date: 2017-04-28 13:05
Category: Network
Tags: network, nx-os, cli
Authors: Eric Rochow
Summary: Obscure commands for my future reference

# Obscure Commands

## STP

Find the total number of STP Virtual Ports currently in use:

    show spanning-tree internal info global | grep -a 3 "STP Port Count Summary"
    ------- STP Port Count Summary ---------------
    Total stp_ports*instances:      498
    Total ports*vlans        :    41799
    Total phy_ports*vlans    :    42051

## TCAM

### FIB Exception State

    show system internal forwarding route summary [module #]

## RAID

    lw-dc2-dist1-nexus# show system internal raid

This command does not tab complete nor question mark complete. It must also be typed out completely.
