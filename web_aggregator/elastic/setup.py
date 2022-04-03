import logging
import os
import traceback

import elasticsearch
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)

elasticsearch.logger.setLevel('ERROR')


# Use this url to connect to Elastic Search Docker Cluster outside the docker network named "agg_network".
# URL = 'http://localhost:9200/'


def connect_elasticsearch():
    try:
        _es = None
        _es = Elasticsearch(
            [{"scheme": "https",
              'host': os.environ.get('ES_HOST', 'es01'),
              'port': int(os.environ.get('ES_PORT', '9200'))}],
            basic_auth=(os.environ.get('ES_USER'), os.environ.get('ES_PASS'))
        )
        print(_es.__dict__)
        if _es.ping():
            print('Connected!')
        else:
            print('Connection Failed!')
        return _es
    except Exception as e:
        # print(e)
        return None

def connect_opensearch():
    try:
        awsauth = (os.environ.get('ES_USER'), os.environ.get('ES_PASS'))

        _es = None  
        _es = Elasticsearch(
            hosts=[{'host': os.environ.get('ES_HOST', 'es01'), 'port': 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )

        print(_es.__dict__)
        if _es.ping():
            print('Connected!')
        else:
            print('Connection Failed!')
        return _es
    except Exception as e:
        return None

try:
    elasticsearch_obj = '' 
    cloud_status = os.environ.get('CLOUD', 'disabled')
    if cloud_status == 'enabled':
        elasticsearch_obj = connect_opensearch()
    else:
        elasticsearch_obj = connect_elasticsearch()

    if elasticsearch_obj.ping():
        print("Elastic Search Connected!")
except Exception as e:
    print("Elastic Search couldn't be connected!", e)


def get_or_create_es_client():
    global elasticsearch_obj
    if elasticsearch_obj and elasticsearch_obj.ping():
        return elasticsearch_obj
    try:
        _es = ''
        cloud_status = os.environ.get('CLOUD', 'disabled')
        if cloud_status == 'enabled':
            _es = connect_opensearch()
        else:
            _es = connect_elasticsearch()

        if _es.ping():
            print('Connected!')
        else:
            print('Connection Failed!')
        return _es

    except Exception as e:
        logger.debug(str(e))
        logger.debug(traceback.format_exc())
        return None
