BACKEND_URL = ""

class Config:
    NEWS_BASE_URL_SOURCES = 'https://newsapi.org/v2/top-headlines/sources?apiKey={}'
    NEWS_BASE_EVERYTHING_URL = 'https://newsapi.org/v2/everything?domains={}&apiKey={}'
    NEWS_BASE_HEADLINES_URL = 'https://newsapi.org/v2/top-headlines?country=us&apiKey={}'
    NEWS_BASE_SOURCE = 'https://newsapi.org/v2/top-headlines?sources={}&apiKey={}'
    API_KEY = "f1a683b7df544ace8de3d9ce54790eb1"

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
