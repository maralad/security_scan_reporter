FROM python:3.7-alpine

RUN pip3 install --upgrade pip

WORKDIR /src

COPY . .

#package dependency needed for lxlm - python xml parser
RUN apk add --update --no-cache g++ gcc libxslt-dev 

RUN pip3 install -r ./requirements.txt
    

#ENTRYPOINT python manage.py migrate && \
 #          python manage.py runserver 0.0.0.0:8000
