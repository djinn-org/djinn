#!/bin/bash

server_url=$1
retry_count=$2
manage=~/local/djinn/python/django-djinn-client/manage.sh
$manage server --set-server-url $server_url
$manage server --reset eth0

msg() {
    echo '[*]' $*
}

for ((i = 1; i <= $retry_count; ++i)); do
    msg connecting to server, attempt '#'$i
    $manage server --register && exit 0
done

msg Failed to connect to Djinn server
exit 1
