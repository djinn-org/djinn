#!/bin/sh

cd $(dirname "$0")

for ip in $(./ips.sh); do
    ping -q -c1 -w1 $ip >/dev/null && echo $ip
done
