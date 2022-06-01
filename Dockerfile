FROM python:3.9.10

COPY ./project /app/project
COPY ./project/requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENV DATABASE_HOSTNAME=localhost \
DATABASE_PORT=5432 \
DATABASE_PASSWORD=silash \
DATABASE_NAME=project \
DATABASE_USERNAME=postgres \
SECRET_KEY=5d643c4b89cdc16c73080b442b2c32ba \
ALGORITHM=HS256 \
ACCESS_TOKEN_EXPIRE_MINUTES=30

EXPOSE 8000



CMD ["uvicorn", "project.main:app", "--host=0.0.0.0", "--reload"]

