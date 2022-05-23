#!/bin/sh
# alembic revision -m "first create script"
# alembic upgrade head
# alembic revision --autogenerate -m 'add create date in user table'
alembic upgrade head
