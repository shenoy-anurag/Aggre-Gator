FROM python:latest

RUN mkdir /app
WORKDIR /app

ADD web_scraper /app/web_scraper

RUN apt-get update \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV CGO_ENABLED=0 

RUN apt-get -y install curl

RUN groupadd -g 799 scraper && \
    useradd -r -u 999 -g scraper scraper

ADD --chown=scraper:scraper web_scraper/requirements.txt /app

WORKDIR /app
RUN pip3 install Flask
RUN pip3 install -r /app/requirements.txt

USER scraper

COPY web_scraper/wsgi.py /app
COPY web_scraper/entrypoint.sh /app
COPY web_scraper/celery_entrypoint.sh /app
COPY rds-combined-ca-bundle.pem /app/

# RUN chmod +x ./entrypoint.sh
# RUN chmod +x ./celery_entrypoint.sh

CMD [ "python", "./wsgi.py" ]