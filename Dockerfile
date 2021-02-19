FROM python:3.7-alpine
WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers postgresql-client postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src /app/src
COPY ./manage.py /app/manage.py
