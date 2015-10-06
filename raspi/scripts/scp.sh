#!/bin/sh

cd $(dirname "$0")

for ip in $(./alive-ips.sh); do
    raspi=pi@$ip
    echo '*' scp $1 $raspi:$2 ...
    scp $1 $raspi:$2
done
