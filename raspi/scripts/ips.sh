#!/bin/sh

cd $(dirname "$0")

awk '{print $2}' ../etc/addresses.txt
