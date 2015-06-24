#!/bin/bash

cd $(dirname "$0")

# params
service=$1
room_id=$2
await_seconds=$3

# constants
SwitchGPIO=24

# variables
presence=0
await_end=$(($(date +%s) + await_seconds))

waiting() {
    [[ $(date +%s) -le $await_end ]]
}

gpio -g mode $SwitchGPIO input

while waiting; do
    printf .
    TEST_VAR=$(gpio -g read $SwitchGPIO)

    if [ "$TEST_VAR" = 1 ]; then
        if [ $presence -eq 0 ]; then
            echo presence detected, making reservation ...
            presence=1
            update-leds.sh red
            ./run.sh mrgenie/cli.py $service make-reservation -r $room_id
            sleep 1
        else
            echo leaving room, canceling reservation ...
            presence=0
            update-leds.sh green
            ./run.sh mrgenie/cli.py $service cancel-reservation -r $room_id
            echo exit
            break
        fi
    fi
done
