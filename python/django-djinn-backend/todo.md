essential
---------

! cleaning
+ create package, move and rename ext commands
x make it easy to work with or without exchange
    + reserve and cancel are void methods (at least for now)
    ! sync gets a list of bookings
    + if any of these are broken, simply nothing happens; but: tests are slow
    x make tests fast

+ /clients/:mac/presence
    - ext: sync related room
    + if available:
        + calculate end = min(next start, start + 1 hour)
        + ext: create booking -> +log
        - ext: sync related room
    - update related client

/clients/:mac/empty
    - ext: sync related room
    + if booked:
        + ext: cancel booking -> +log
        - ext: sync related room
    - update related client

client: POST /status

client: GET /status

install on sandbox server

cron script for client

full test with zwave
- copy scripts from image
- fix raspi network
- setup hosts service
- install djinn client
- simple test of zwave: call to presence, empty

later
-----

get CORS working, test

get filter tests working

disable deleting from rest api

remove Django logic from tests, make them use Python logic
