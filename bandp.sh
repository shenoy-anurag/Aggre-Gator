#!/bin/bash

docker build -t web-scraper . -f ./web_scraper/Dockerfile --no-cache
docker tag web-scraper:latest 413589174266.dkr.ecr.us-east-1.amazonaws.com/web-scraper:latest
aws lightsail push-container-image --region us-east-1 --service-name web-scraper --label web-scraper --image web-scraper:latest

docker build -t web-aggregator . -f ./web_aggregator/Dockerfile --no-cache
docker tag web-aggregator:latest 413589174266.dkr.ecr.us-east-1.amazonaws.com/web-aggregator:latest
aws lightsail push-container-image --region us-east-1 --service-name web-aggregator --label web-aggregator --image web-aggregator:latest