#!/bin/sh

/sbin/ifconfig | grep 'inet ' | grep -v 127.0.0.1 | awk '{print $2}' | sed -e 's/^[^0-9]*//g'