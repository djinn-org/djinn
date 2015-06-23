#!/bin/sh

cd $(dirname "$0")

room_id=$1
status=$(./run.sh mrgenie/status.py $room_id)

echo room=$room_id
echo status=$status

case $status in
    RESERVED) update-leds.sh blue ;;
    MEETING) update-leds.sh red ;;
    FREE) update-leds.sh green ;;
    *) update-leds.sh off ;;
esac
