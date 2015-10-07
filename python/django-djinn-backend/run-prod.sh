#!/bin/sh

cd $(dirname "$0")
. ./virtualenv.sh

./manage.sh runserver --settings django_djinn_backend.prod_settings 0.0.0.0:8000 $*
