#!/bin/sh

cd $(dirname "$0")

for ip in $(./alive-ips.sh); do
    raspi=pi@$ip
    echo '*' sending to $raspi command "$@" ...
    ssh $raspi "$@"
done
