#!/bin/bash

cd $(dirname "$0")

service=$1
room_id=$2
await_seconds=$3

# init : sanity test leds
for color in off red green blue off; do
    update-leds.sh $color
done

while :; do
    ./update-status.sh $service $room_id

    status=$(./status.sh $service $room_id)
    if test $status = FREE; then
        ./await-presence-and-reserve-once.sh $service $room_id $await_seconds
    fi
done
