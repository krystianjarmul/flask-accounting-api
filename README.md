# Short description

Accounting REST API for cleaning service made in Python3, using classic Flask aproach

# Requirements
* Docker

# Usage

Clone repo to your local:
```
git clone https://github.com/krystianjarmul/flask-accounting-api.git
```

Build docker-compose:
```
docker-compose build
```
Run docker-compose:
```
docker-compose up
```

Init database(only once):
```
docker-compose exec api sh -c "python manage.py db init && python manage.py db migrate && python manage.py db upgrade"
```

Open browser at 127.0.0.1:5000 and enjoy the api.
