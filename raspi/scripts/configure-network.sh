#!/bin/bash

iface=$1
subnet=$2
gw=$3
nameserver=$4

msg() {
    echo '[*]' $*
}

cd $(dirname "$0")

ip=$(./ip.sh)
if test "$ip"; then
    msg Detected IP: $ip
    exit 0
fi

addresses=../etc/addresses.txt
# in the format:
#b8:27:eb:4a:ca:47 192.168.1.10
#b8:27:eb:34:f8:f2 192.168.1.11
#b8:27:eb:ab:f9:98 192.168.1.12
#...

msg Could not detect IP, trying to find one in address list

mac=$(./mac.sh $iface)
ip=$(grep "$mac" "$addresses" | awk 'NR == 1 {print $2}')

if test "$ip"; then
    msg Found IP in address list: $ip
else
    msg No IP in address list, will pick one at random
    network=$(head -n1 $addresses | awk '{sub("\.[^.]*$", "", $2); print $2}')
    highest_ip=$(awk -F. '{ if ($NF > max) max = $NF } END { print max }' $addresses)
    ip=$network.$((highest_ip + 10 + $RANDOM % 10))
    msg Picked semi-random IP: $ip
fi

msg Configuring network: $iface $ip/$subnet $gw $nameserver

ifconfig $iface $ip/$subnet

route add default gw $gw

echo "nameserver $nameserver" > /etc/resolv.conf
