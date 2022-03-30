FROM python:latest

RUN mkdir /app
WORKDIR /app

ADD web_aggregator /app/web_aggregator

RUN apt-get update \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get -y install curl

RUN groupadd -g 799 aggregator && \
    useradd -r -u 999 -g aggregator aggregator

ADD --chown=aggregator:aggregator web_aggregator/requirements.txt /app

WORKDIR /app
RUN pip3 install Flask
RUN pip3 install -r /app/requirements.txt

USER aggregator

COPY web_aggregator/wsgi.py /app
COPY web_aggregator/entrypoint.sh /app
COPY web_aggregator/celery_entrypoint.sh /app

# RUN chmod +x ./entrypoint.sh
# RUN chmod +x ./celery_entrypoint.sh

CMD [ "python", "./wsgi.py" ]