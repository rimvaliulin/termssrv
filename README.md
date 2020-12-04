# Terminology Service

Simple Terminology service with REST API. Operating with the reference book and terms in it.

## Installation

```bash
git clone https://github.com/rimvaliulin/termssrv.git
cd termsrv
python3 -m venv env
source env/bin/activate
pip install django djangorestframework httpie
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --email admin@example.com --username admin
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

```bash
http http://127.0.0.1:8000/books/
```

```
GET /books/
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json

{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "description": "Справочник диагнозов",
            "id": 1,
            "name": "Диагнозы",
            "pub_date": "2020-12-01",
            "short_name": "diagnozy",
            "version": "1.0"
        },
        {
            "description": "Справочник диагнозов",
            "id": 2,
            "name": "Диагнозы",
            "pub_date": "2020-12-02",
            "short_name": "diagnozy",
            "version": "2.0"
        },
        ...
        {
            "description": "",
            "id": 5,
            "name": "Специальности",
            "pub_date": "2020-12-02",
            "short_name": "specialnosti",
            "version": "2.0"
        }
    ]
}

```

### Getting the list of reference books actual as of the specified date.

```bash
http http://127.0.0.1:8000/books/2020-12-02/
```

```
GET /books/2020-12-05/
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json

{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "description": "Справочник диагнозов",
            "id": 2,
            "name": "Диагнозы",
            "pub_date": "2020-12-02",
            "short_name": "diagnozy",
            "version": "2.0"
        },
        {
            "description": "",
            "id": 5,
            "name": "Специальности",
            "pub_date": "2020-12-02",
            "short_name": "specialnosti",
            "version": "2.0"
        },
        {
            "description": "Справочник диагнозов",
            "id": 1,
            "name": "Диагнозы",
            "pub_date": "2020-12-01",
            "short_name": "diagnozy",
            "version": "1.0"
        },
        {
            "description": "asdasd",
            "id": 4,
            "name": "Специальности",
            "pub_date": "2020-12-01",
            "short_name": "specialnosti",
            "version": "1.0"
        }
    ]
}

```

### Getting the terms of a specified reference books of the current version

```bash
http http://127.0.0.1:8000/books/1/
```

```
GET /books/a/
HTTP 200 OK
Allow: GET, PUT, HEAD, OPTIONS
Content-Type: application/json

{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "code": "bar",
            "value": "green"
        },
        {
            "code": "baz",
            "value": "blue"
        },
        {
            "code": "foo",
            "value": "red"
        }
    ]
}

```

### Validation of elements of a given reference books of the current version

```bash
echo '[{"code": "foo", "value": "red"}, {"code": "bar", "value": "black"}]' | http PUT http://127.0.0.1:8000/books/1/
```

````
PUT /books/a/1/
HTTP 400 Bad Request
Allow: GET, PUT, HEAD, OPTIONS
Content-Type: application/json

[
    {
        "code": "foo",
        "value": "white"
    }
]

````


### Getting the terms of a given reference books of the specified version

```bash
http http://127.0.0.1:8000/books/1/1.0/
```

```
GET /books/a/1/
HTTP 200 OK
Allow: GET, PUT, HEAD, OPTIONS
Content-Type: application/json

{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "code": "bar",
            "value": "green"
        },
        {
            "code": "baz",
            "value": "blue"
        },
        {
            "code": "foo",
            "value": "red"
        }
    ]
}
```

### Validation of an element of a given reference book according to a specified version

```bash
echo '{"code": "foo", "value": "red"}' | http PUT http://127.0.0.1:8000/books/1/1.0/
```
```
GET /books/a/1/
HTTP 200 OK
Allow: GET, PUT, HEAD, OPTIONS
Content-Type: application/json

{
    "status": "validated"
}
```

```bash
echo '{"code": "foo", "value": "brown"}' | http PUT http://127.0.0.1:8000/books/a/1/
```

```
PUT /books/a/1/
HTTP 400 Bad Request
Allow: GET, PUT, HEAD, OPTIONS
Content-Type: application/json

{
    "status": "not valid"
}
```
