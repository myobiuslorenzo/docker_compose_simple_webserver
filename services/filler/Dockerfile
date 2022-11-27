FROM ubuntu:latest
MAINTAINER Olga Shpuntenko 'oshpuntenko@yandex.ru'
RUN apt-get update -y
RUN apt-get install -y python3-pip python3 build-essential
RUN pip install mysql-connector-python pandas
COPY /services/filler/app /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
# RUN python3 app.py -- only for debug
CMD ["python3", "app.py"]