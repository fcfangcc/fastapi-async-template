From tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY ./requirements.txt /app/requirements.txt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir --upgrade -r /app/requirements.txt
# RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app/ /app/app
COPY ./gunicorn_conf.py /app/gunicorn_conf.py
ENV PYTHONPATH=/app

# Don't forget to change the default values
# Injection via environment variables
ENV SECRET_KEY="secret_key"
ENV FIRST_SUPERUSER="superuser@xxx.com"
ENV FIRST_SUPERUSER_PASSWORD="password"
ENV SQLALCHEMY_DATABASE_URI="mysql+aiomysql://user:password@mysql-host/dbname?charset=utf8mb4"