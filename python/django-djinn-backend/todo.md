essential
---------

! get CORS working, test

! fix sync related bugs

important: sort out timezone
----------------------------

Currently, production requires:

    USE_TZ = False

Otherwise reservations are created 2 hours behind or ahead, it's a confused mess.

However, unit tests fail like that:

> SQLite backend does not support timezone-aware datetimes when USE_TZ is False.

While at, force timezone warnings in unit tests.

later
-----

get filter tests working

/clients/:mac/presence -> update related client
- client: POST /status
- client: GET /status

/clients/:mac/empty -> update related client

cron script for client for heartbeats

disable deleting from rest api

remove Django logic from tests, make them use Python logic

generalize backend

separate mvc; especially remove logic from views
