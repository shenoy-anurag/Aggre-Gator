import datetime
import logging
from datetime import datetime
from typing import Text, List

from pymongo import errors

from web_scraper import mongo

logger = logging.getLogger(__name__)


class Article:
    TYPE = 'article'

    def __init__(self, url: Text, title: Text = None, article: Text = None, publisher: Text = None,
                 image_url: Text = None, bias=None, topic=None, tags=None, year: int = 0, month: int = 0, day: int = 0,
                 author: Text = "", author_url: Text = "", character_length: int = None, comments=None):
        self.url = url
        self.title = title
        self.article = article
        self.publisher = publisher
        self.url_image = image_url
        self.bias = bias
        self.topic = topic
        self.tags = [] if not tags else tags
        self.year = year
        self.month = month
        self.day = day
        self.creation_date = None
        self.modified_date = None
        self.author = author
        self.author_url = author_url
        self.character_length = character_length
        self.comments = comments

    def create_creation_date(self):
        self.creation_date = datetime(
            year=int(self.year), month=int(self.month), day=int(self.day)
        ).replace(microsecond=0, second=0, minute=0, hour=0)

    def create_mongo_document(self):
        return {
            'type': self.TYPE, 'publisher': self.publisher, 'url': self.url, 'title': self.title, 'author': self.author,
            'author_url': self.author_url, 'article': self.article, 'url_image': self.url_image, 'bias': self.bias,
            'topic': self.topic, 'tags': self.tags, 'year': self.year, 'month': self.month, 'day': self.day,
            'creation_date': self.creation_date, 'modified_date': self.modified_date,
            'character_length': self.character_length, 'comments': self.comments
        }


def save_cnn_articles_mongo(article_objs: List[Article]):
    try:
        article_documents = [article.create_mongo_document() for article in article_objs]
        mongo.db.articles_cnn.insert_many(article_documents)
    except errors.OperationFailure as e:
        logger.debug(e)
        return e.details.get("errmsg")
    except:
        raise


def save_fox_articles_mongo(article_objs: List[Article]):
    try:
        article_documents = [article.create_mongo_document() for article in article_objs]
        mongo.db.articles_fox.insert_many(article_documents)
    except errors.OperationFailure as e:
        logger.debug(e)
        return e.details.get("errmsg")
    except:
        raise
