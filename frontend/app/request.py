import requests
from .config import BACKEND_URL, BACKEND_PORT
from .config import api_url_mapper
from .models import Articles

url_to_hit = BACKEND_URL + ":" + BACKEND_PORT + "/articles"
print(url_to_hit)

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


def get_articles_for_home():
    # TODO: ADD API CALL
    params = {
        "years": ["2022"],
        "categories": None,
        "sources": None,
        "page": 1,
        "per_page": 100
    }
    get_articles = requests.post(url_to_hit, data=params)
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
