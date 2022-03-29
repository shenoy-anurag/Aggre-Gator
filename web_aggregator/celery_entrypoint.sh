#!/bin/sh
#cd ..
celery -A web_aggregator.celery_app worker --loglevel=DEBUG
