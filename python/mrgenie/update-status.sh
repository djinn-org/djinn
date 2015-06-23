#!/bin/sh

cd $(dirname "$0")

room_id=eU9npkV8mZ
status=$(./run.sh mrgenie/status.py)

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
