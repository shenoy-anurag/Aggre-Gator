import requests

from .config import api_url_mapper
from .models import Articles

api_key = None
base_url = None
base_url_for_everything = None
base_url_top_headlines = None
base_source_list = None


def create_contents_from_all_articles(all_articles):

    all_articles_results = []
    source = []
    title = []
    desc = []
    author = []
    img = []
    p_date = []
    url = []

    for i in range(len(all_articles)):
        article = all_articles[i]
        source.append(article['source'])
        title.append(article['title'])
        desc.append(article['description'])
        author.append(article['author'])
        img.append(article['urlToImage'])
        p_date.append(article['publishedAt'])
        url.append(article['url'])
        article_object = Articles(source, title, desc, author, img, p_date, url)
        all_articles_results.append(article_object)
        contents = zip(source, title, desc, author, img, p_date, url)

    return contents

def publishedArticles():
    # TODO: ADD API CALL
    get_articles = requests.get(api_url_mapper["URL_HOME"])
    all_articles = get_articles['articles']
    return create_contents_from_all_articles(all_articles)


def get_categorical_articles(category):
    # TODO: ADD API CALL
    params = {"category": category}
    get_articles = requests.post(api_url_mapper["URL_CATEGORY"], data=params)
    all_articles = get_articles['articles']
    return create_contents_from_all_articles(all_articles)


def get_yearly_articles(year):
    # TODO: Add API CALL
    params = {'year': year}
    get_articles = requests.post(api_url_mapper["URL_YEAR"], data=params)
    all_articles = get_articles['articles']
    return create_contents_from_all_articles(all_articles)


def get_articles_from_source(source):
    # TODO: Add API CALL
    params = {'source': source}
    get_articles = requests.post(api_url_mapper["URL_SOURCE"], data=params)
    all_articles = get_articles['articles']
    return create_contents_from_all_articles(all_articles)