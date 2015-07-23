django-djinn-backend
====================

Django library for Djinn backend

Install
-------

TODO

POC needed
----------

- GET /find-rooms?params
    - params:
        - start
        - minutes
        - capacity
        - equipment
    - show params in swagger
    - unit tests

- access to local REST from local Ionic
    - need to get CORS stuff working

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
