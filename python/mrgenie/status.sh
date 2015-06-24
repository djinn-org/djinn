#!/bin/sh

cd $(dirname "$0")

service=$1
room_id=$2
./run.sh mrgenie/cli.py $service status -r $room_id
