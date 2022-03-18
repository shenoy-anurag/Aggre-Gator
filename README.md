# Aggre-Gator

Our project aggregates articles from a few news sites and shows them in one place for the convenience of the user.

## Demo

Articles saved in MongoDB and Elastic Search after scraping:
![Mongo DB Articles Stored](https://github.com/shenoy-anurag/temp-json/blob/master/static/images/mongo-db-articles-cnn.png?raw=true)
![Elastic Search Article P1](https://github.com/shenoy-anurag/temp-json/blob/master/static/images/elastic-search-articles-p1.png?raw=true)
![Elastic Search Article P2](https://github.com/shenoy-anurag/temp-json/blob/master/static/images/elastic-search-articles-p2.png?raw=true)

## Run

### Prerequisites

- [Docker Compose](https://docs.docker.com/compose/install/)

### Start containers

Run the command:

`sudo docker-compose -f docker-compose.yml up`

to start all the containers.

### Containers

- `web_scraper`: The main Flask web application which will scrape websites for articles, and return search results and feed.
- `celery_web_scraper`: The Celery application which run the async tasks.
- `es01`: The primary node of the ElasticSearch cluster.
- `rabbitmq`: Broker for Celery workers and queues.
- `mongo`: MongoDB instance, primary data store, for storing articles and other user and app information.

