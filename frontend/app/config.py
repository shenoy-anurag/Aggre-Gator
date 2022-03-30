import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
BACKEND_URL = os.environ.get("BACKEND_URL")
BACKEND_PORT = os.environ.get("BACKEND_PORT")


class Config:
    DEBUG = False


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}

category_mapper = {
    "CATEGORY_BUSINESS": "business",
    "CATEGORY_TECHNOLOGY": "technology",
    "CATEGORY_ENTERTAINMENT": 'entertainment',
    "CATEGORY_SCIENCE": "science",
    "CATEGORY_SPORTS": "sports",
    "CATEGORY_HEALTH": "health",
}

api_url_mapper = {
    "URL_HOME": "",
    "URL_YEAR": "",
    "URL_SOURCE": "",
    "URL_CATEGORIES": "",
}
