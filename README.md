# Terminology Service

Simple Terminology service with REST API. Operating with the reference book and terms in it.

# Installation

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

# Running

```bash
python manage.py runserver
```
