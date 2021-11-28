## deliverect_task
Test task for Deliverect.
<br />
I used python 3.7 and Django 3.2 + Django Rest Framework 3.12.
<br />
Application uses an sqlite database.
<br />
You can find deliverect postman collection in root of the project. It has some HTTP calls I used for testing the application. Hopefully everything looks pretty self-explanatory if you look at urls.py and views.py under ./pos folder.

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
> cd ./deliverect; python manage.py runserver

### Running unit tests
> cd ./deliverect; python manage.py test
