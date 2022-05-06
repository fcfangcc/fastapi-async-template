fastapi-async-template
============================
A Python Async Project Template With FastAPI and SQLAlchemy (reference `full-stack-fastapi-postgresql <https://github.com/tiangolo/full-stack-fastapi-postgresql>`_)



How to use
============================

.. code:: shell

    # git clone https://github.com/fcfangcc/fastapi-async-template.git

Create a env configuration

.. code:: shell

    # touch .env

    SECRET_KEY = "secret_key"
    FIRST_SUPERUSER = "superuser@xxx.com"
    FIRST_SUPERUSER_PASSWORD = "password"
    SQLALCHEMY_DATABASE_URI = "mysql+aiomysql://user:password@mysql-host/dbname?charset=utf8mb4"


Initialize database

.. code:: shell

    # bash ./scripts/init_db.sh

Start develop web service

.. code:: shell

    # poetry install -E mysql --no-dev
    # poetry run python manager.py db init
    # poetry run python manager.py runserver --port 8000

Deploy with dockert

.. code:: shell

    # docker build -f dockerfiles/Dockerfile  -t my-app .
    # docker run --name mycontainer -p 80:80 my-app



Dependencies
===========================
* `FastAPI <https://fastapi.tiangolo.com/>`_
* `SQLAlchemy <https://www.sqlalchemy.org/>`_  version > 1.4
