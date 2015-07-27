django-djinn-backend
====================

Django library for Djinn backend

Install
-------

TODO

POC needed
----------

- GET /find/rooms?params
    - params:
        - start
        - minutes
        - capacity
        - equipment
    - show params in swagger
    - unit tests

- POST /rooms/:id/reservations?params
    - params:
        - start
        - minutes

x access to local REST from local Ionic
    x need to get CORS stuff working
    -> djinn-web will probably take care of this part

Memo
----

    # invalid date range:
    curl -X POST -d start=2015-07-27T12:00 -d room=1 -d end=2015-07-27T11:00 localhost:8000/api/v1/rooms/1/reservations/ | tee x.html

TODO
----

- Backend interface definition
    + example implementation using Django
    + example implementation using Parse

- Complete REST API

- Complete Engine API

- Engine implementation with unit tests

- CLI for backend

- CLI for engine

- /rooms/:id/status

- POST /rooms/:id/reserve?params
    - or: POST /rooms/:id/reservations
