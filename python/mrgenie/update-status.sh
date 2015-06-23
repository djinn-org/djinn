#!/bin/sh

cd $(dirname "$0")

room_id=$1
status=$(./run.sh mrgenie/status.py $room_id)

echo room=$room_id
echo status=$status

BlueLED=17
GreenLED=22
RedLED=4

gpio -g mode $BlueLED out
gpio -g mode $GreenLED out
gpio -g mode $RedLED out

StatusRed=0
StatusGreen=0
StatusBlue=0

case $status in
    RESERVED) StatusBlue=1 ;;
    MEETING) StatusRed=1 ;;
    FREE) StatusGreen=1 ;;
esac

gpio -g write $BlueLED $StatusBlue
gpio -g write $GreenLED $StatusGreen
gpio -g write $RedLED $StatusRed
