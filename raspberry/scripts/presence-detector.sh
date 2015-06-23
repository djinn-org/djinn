#!/bin/bash
#

update-leds.sh off

#constants
SwitchGPIO=24

#variables
presence=0

gpio -g mode $SwitchGPIO input

while true
do
    printf .
    TEST_VAR=$(gpio -g read $SwitchGPIO)

    if [ $TEST_VAR -eq 1 ]; then
        if [ $presence -eq 0 ]; then
            echo presence detected, making reservation ...
            presence=1
            update-leds.sh red
            sleep 1
        else
            echo leaving room, cancel reservation ...
            presence=0
            update-leds.sh green
            sleep 1
        fi
    fi
done
