#!/bin/sh
#cd ..
celery -A web_scraper.celery_app worker -P solo --loglevel=DEBUG --without-gossip --without-mingle --without-heartbeat
