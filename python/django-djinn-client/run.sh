#!/bin/sh

cd $(dirname "$0")
. ./virtualenv.sh

./manage.sh runserver 8001 $*
