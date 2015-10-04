#!/bin/bash

iface=$1
ip=$2
subnet=$3
gw=$4
nameserver=$5

# if we have ip, skip
test "$ip" && exit 0

cd $(dirname "$0")

msg() {
    echo '[*]' $*
}

msg No IP received, will try to pick from address list

addresses=../etc/addresses.txt
# in the format:
#b8:27:eb:4a:ca:47 192.168.1.10
#b8:27:eb:34:f8:f2 192.168.1.11
#b8:27:eb:ab:f9:98 192.168.1.12
#...

mac=$(./mac.sh $iface)
ip=$(grep "$mac" "$addresses" | awk '{print $2}')

if ! test "$ip"; then
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
