FROM ubuntu:20.04
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ADD web_aggregator /app/web_aggregator

RUN apt-get update && apt-get -y install curl
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

ADD web_aggregator/requirements.txt /app
RUN pip3 install -r /app/requirements.txt

RUN ls
RUN locale -a

# RUN locale-gen en_US en_US.UTF-8
# RUN dpkg-reconfigure locales

# RUN update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

COPY web_aggregator/wsgi.py /app
COPY web_aggregator/entrypoint.sh /app
COPY web_aggregator/celery_entrypoint.sh /app

RUN chmod +x ./entrypoint.sh
RUN chmod +x ./celery_entrypoint.sh
