#!/bin/sh

cd $(dirname "$0")
. ./virtualenv.sh

ip=$(./scripts/ip.sh)
./manage.sh runserver $ip:8000 $*
