import datetime
import logging
import traceback
from datetime import datetime
from typing import Text

from pymongo import errors

from web_aggregator import mongo, app
from web_aggregator.common.constants import PUBLISHER_FOX, PUBLISHER_CNN, CATEGORY_MAPPINGS, SOURCES
from web_aggregator.core.utils import convert_categories, truncate_descriptions

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


def create_basic_settings():
    try:
        result = mongo.db.settings.insert_one(
            {
                'org': "aggregator",
                'name': "Aggre-Gator",
                'categories': ['US', 'World', 'Business', 'Technology', 'Science', 'Sport', 'Health', 'Entertainment'],
                'sources': ['CNN', 'FOX News']
            }
        )
        return result
    except errors.OperationFailure as e:
        logger.error(e)
        return None
    except Exception as e:
        logger.error(e)
        return None


def fetch_settings():
    try:
        settings = mongo.db.settings.find_one(
            {'org': "aggregator"})
        return settings
    except errors.OperationFailure as e:
        logger.error(e)
        return e.details.get("errmsg")
    except Exception as e:
        logger.error(e)
        return None


def fetch_mongo_articles(categories, sources, years, page, per_page):
    try:
        skip_count = (page - 1) * per_page

        if not years:
            years = [str(datetime.datetime.now().year)]
        # publishers = convert_sources(sources)
        publishers = sources
        if not sources:
            publishers = SOURCES
        converted_categories = categories
        if categories:
            converted_categories = convert_categories(categories, CATEGORY_MAPPINGS, publishers)
        articles = []
        if PUBLISHER_CNN in publishers:
            if not categories:
                cnn_articles = list(
                    mongo.db.articles_cnn.find(
                        {}, {'_id': 0, 'publisher': 1, 'title': 1, 'article': 1, 'author': 1, 'url_image': 1,
                             'creation_date': 1, 'url': 1, 'bias': 1, 'topic': 1}
                    ).skip(skip_count).limit(per_page)
                )
            else:
                cnn_articles = mongo.db.articles_cnn.aggregate([
                    {
                        '$match': {
                            'topic': {
                                '$in': converted_categories[PUBLISHER_CNN]
                            },
                            'year': {
                                '$in': years
                            }
                        }
                    },
                    {'$skip': skip_count},
                    {'$limit': per_page},
                    {'$project': {'_id': 0, 'publisher': 1, 'title': 1, 'article': 1, 'author': 1, 'url_image': 1,
                                  'creation_date': 1, 'url': 1, 'bias': 1, 'topic': 1}}
                ])
            articles.extend(cnn_articles)
        if PUBLISHER_FOX in publishers:
            if not categories:
                fox_articles = list(
                    mongo.db.articles_fox.find(
                        {}, {'_id': 0, 'publisher': 1, 'title': 1, 'article': 1, 'author': 1, 'url_image': 1,
                             'creation_date': 1, 'url': 1, 'bias': 1, 'topic': 1}
                    ).skip(skip_count).limit(per_page)
                )
            else:
                fox_articles = mongo.db.articles_fox.aggregate([
                    {
                        '$match': {
                            'topic': {
                                '$in': converted_categories[PUBLISHER_FOX]
                            },
                            'year': {
                                '$in': years
                            }
                        }
                    },
                    {'$skip': skip_count},
                    {'$limit': per_page},
                    {'$project': {'_id': 0, 'publisher': 1, 'title': 1, 'article': 1, 'author': 1, 'url_image': 1,
                                  'creation_date': 1, 'url': 1, 'bias': 1, 'topic': 1}}
                ])
            articles.extend(fox_articles)
        # sorting
        articles.sort(key=lambda x: x['creation_date'], reverse=True)
        articles = truncate_descriptions(articles)
        return articles
    except errors.OperationFailure as e:
        app.logger.error(e)
        app.logger.debug(traceback.format_exc())
        return e.details.get("errmsg")
    except Exception as e:
        print(traceback.format_exc())
        app.logger.error(e)
        app.logger.debug(traceback.format_exc())
        return None
