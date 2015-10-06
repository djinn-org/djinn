essential
---------

! periodic job to merge reservations

! periodic job to cancel reservations
    
/clients/:mac/presence -> update related client
- client: POST /status
- client: GET /status

/clients/:mac/empty -> update related client

important: sort out timezone
----------------------------

Currently, production requires:

    USE_TZ = False

Otherwise reservations are created 2 hours behind or ahead, it's a confused mess.

However, unit tests fail like that:

> SQLite backend does not support timezone-aware datetimes when USE_TZ is False.

later
-----

get CORS working, test

get filter tests working

cron script for client for heartbeats

replace datetime in tests with timezone

disable deleting from rest api

remove Django logic from tests, make them use Python logic

generalize backend

separate mvc; especially remove logic from views
