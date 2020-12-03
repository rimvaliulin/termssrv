# Terminology Service

Simple Terminology service with REST API. Operating with the reference book and terms in it.

## Installation

```bash
git clone https://github.com/rimvaliulin/termssrv.git
cd termsrv
python3 -m venv env
source env/bin/activate
pip install django djangorestframework
python manage.py migrate
python manage.py createsuperuser --email admin@example.com --username admin
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata termssrv/terms/fixtures/terms.json
```

## Running

```bash
python manage.py runserver
```

## Deinstallation

```bash
Ctrl+c
deactivate
cd ..
rm -rf termssrv
```

## API

### Getting the list of reference books.
```
GET /books/

HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 11,
    "next": "http://127.0.0.1:8000/books/?page=2",
    "previous": null,
    "results": [
        {
            "name": "Book A",
            "short_name": "a",
            "description": "",
            "version": "1",
            "pub_date": "2020-12-01"
        },
        {
            "name": "Book A",
            "short_name": "a",
            "description": "",
            "version": "2",
            "pub_date": "2020-12-02"
        },
        ...
        {
            "name": "Book D",
            "short_name": "d",
            "description": "",
            "version": "4",
            "pub_date": "2020-12-05"
        }
    ]
}
```

### Getting the list of reference books actual as of the specified date.
### Getting the terms of a specified reference books of the current version
### Validation of elements of a given reference books of the current version
### Getting the terms of a given reference books of the specified version
### Validation of an element of a given reference book according to a specified version
