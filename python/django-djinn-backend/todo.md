essential
---------

+ /clients/:mac/presence
    - ext: sync related room
    - if available:
        - calculate end = min(next start, start + 1 hour)
        - ext: create booking -> log
        - ext: sync related room
    - update related client

/clients/:mac/empty
    - ext: sync related room
    - if booked:
        - ext: cancel booking -> log
        - ext: sync related room
    - update related client

client: POST /status

client: GET /status

/clients/:mac/register  # TODO POST /clients

/clients/:mac/heartbeat

install on sandbox server

client command: presence

client command: empty

client command: heartbeat

later
-----

get CORS working, test

get filter tests working

disable deleting from rest api

remove Django logic from tests, make them use Python logic
