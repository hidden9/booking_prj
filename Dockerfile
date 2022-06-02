FROM python:3.7-slim

RUN pip install django
RUN pip install djangorestframework
RUN pip install django-cors-headers
RUN pip install requests
RUN pip install djongo
RUN pip install mongoengine==0.20.0
RUN pip install pylint-mongoengine==0.4.0
RUN pip install pylint-mongoengine==0.4.0
RUN pip install django-throttle-requests


EXPOSE 8000
COPY src /var/opt/room-slot-booking/

ENTRYPOINT cd /var/opt/room-slot-booking/ ; python manage.py makemigrations ; python manage.py migrate; python manage.py runserver 