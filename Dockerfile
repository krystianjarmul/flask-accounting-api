FROM python:3.7-alpine
WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src /app/src
COPY ./manage.py /app/manage.py

RUN chmod +x manage.py
RUN python manage.py db init
RUN python manage.py db migrate
RUN python manage.py db upgrade
