## deliverect_task
Test task for Deliverect
I used python 3.7 and Django 3.2 + Django Rest Framework 3.12
Application uses an sqlite database.

### Aplication start steps:
1. Create virtual environment (I used virtualenv).
> virtualenv venv
2. Activate virtual environment
> source venv/bin/activate
3. install requirements
> pip install requirements.txt
4. run migrations
> python manage.py migrate
5. run application
> cd ./deliverect
> python manage.py runserver

### Run unit tests
> cd ./deliverect
> python manage.py test
