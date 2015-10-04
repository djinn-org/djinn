#!/bin/sh

iface=$1

/sbin/ifconfig $iface | tr A-Z a-z | sed -e 's/.*ether /x/' -e 's/.*hwaddr /x/' -e 's/ //g' -ne 's/^x//p'
