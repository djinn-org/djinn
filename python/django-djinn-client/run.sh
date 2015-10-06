#!/bin/sh

cd $(dirname "$0")
. ./virtualenv.sh

./manage.sh runserver 0.0.0.0:8001 $*
