# Aggre-Gator

Our project aggregates articles from a few news sites and shows them in one place for the convenience of the user.

## Amazon Lightsail Challenge by Agorize

### Application Status 
We are presenting our submission for the 3rd round of the lightsail challenge. Currently, we are done with creation of backend services and working on integrating AWS services
and developing frontend application as well as bug fixes.

### Team members:
1. Anuj Koli
2. Anurag Shenoy
3. Aman pathak
4. Ruchika Upadhyay
5. Naveen Kumar

## Demo
Articles saved in MongoDB and Elastic Search after scraping:
![Mongo DB Articles Stored](https://github.com/shenoy-anurag/temp-json/blob/master/static/images/mongo-db-articles-cnn.png?raw=true)
![Elastic Search Article P1](https://github.com/shenoy-anurag/temp-json/blob/master/static/images/elastic-search-articles-p1.png?raw=true)
![Elastic Search Article P2](https://github.com/shenoy-anurag/temp-json/blob/master/static/images/elastic-search-articles-p2.png?raw=true)

## Documentation & Presentations
`docs` folder contains presentations, architecture and postman collection.

### Files
- Round 1 Presentation
- Final Presentation
- Architecture (drawio file, jpg image)
- Postman Collection to call APIs

## Run

### Prerequisites

- [Docker Compose](https://docs.docker.com/compose/install/)

### Start containers

Run the command:

`sudo docker-compose -f docker-compose.yml up`

to start all the containers.

### Build & Run Containers

`sudo docker-compose -f docker-compose.yml up --build`

### Containers

- `web_aggregator`: The main Flask web application which will return search results and feed.
- `web_scraper`: A Flask web application which will scrape websites for articles.
- `celery_web_scraper`: The Celery application which run the async tasks.
- `es01`: The primary node of the ElasticSearch cluster.
- `rabbitmq`: Broker for Celery workers and queues.
- `mongo`: MongoDB instance, primary data store, for storing articles and other user and app information.
