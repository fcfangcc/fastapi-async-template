## Config
Support reading configuration from environment variables, also support read from .env file.

## install dependencies

for developer

```shell
poetry install
```

for deployment
```shell
poetry install --without dev
```

## init DB
sync database struct to DB

```shell
alembic upgrade head
```

if you will regenerate the migrate file, do
```shell
rm -r alembic/versions/*
alembic revision -m "first create script"
alembic upgrade head
alembic revision --autogenerate -m 'init'
alembic upgrade head
```


## deployment with docker

todo
