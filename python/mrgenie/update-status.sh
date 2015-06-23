#!/bin/sh

cd $(dirname "$0")

service=$1
room_id=$2
status=$(./run.sh mrgenie/cli.py $service status -r $room_id)

echo room=$room_id
echo status=$status

case $status in
    RESERVED) update-leds.sh blue ;;
    MEETING) update-leds.sh red ;;
    FREE) update-leds.sh green ;;
    *) update-leds.sh off ;;
esac
