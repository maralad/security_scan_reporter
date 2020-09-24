FROM python:3.7-alpine

RUN pip3 install --upgrade pip

COPY /src/backend /srv

WORKDIR /srv

RUN pip3 install -r requirements.txt

ENTRYPOINT python manage.py migrate && \
           python manage.py runserver 0.0.0.0:8000
