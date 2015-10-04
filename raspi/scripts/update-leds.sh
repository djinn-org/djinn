#!/bin/sh

StatusRed=0
StatusGreen=0
StatusBlue=0

color=$1

case "$color" in
    red) StatusRed=1 ;;
    green) StatusGreen=1 ;;
    blue) StatusBlue=1 ;;
esac

BlueLED=17
GreenLED=22
RedLED=4

gpio -g mode $BlueLED out
gpio -g mode $GreenLED out
gpio -g mode $RedLED out

gpio -g write $BlueLED $StatusBlue
gpio -g write $GreenLED $StatusGreen
gpio -g write $RedLED $StatusRed
