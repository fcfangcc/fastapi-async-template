From fcfangcc/uvicorn-gunicorn-fastapi-poetry:3.9

COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install -E mysql --no-root; else poetry install -E mysql --no-root --no-dev ; fi"

COPY ./app/ /app/app
COPY ./gunicorn_conf.py /app/gunicorn_conf.py
ENV PYTHONPATH=/app

# Don't forget to change the default values
# Injection via environment variables
ENV SECRET_KEY="secret_key"
ENV FIRST_SUPERUSER="superuser@xxx.com"
ENV FIRST_SUPERUSER_PASSWORD="password"
ENV SQLALCHEMY_DATABASE_URI="mysql+aiomysql://user:password@mysql-host/dbname?charset=utf8mb4"
