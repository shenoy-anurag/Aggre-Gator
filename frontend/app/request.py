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
        source.append(article['publisher'])
        title.append(article['title'])
        desc.append(article['description'])
        author.append(article.get('author', ''))
        img.append(article.get('url_image', ''))
        p_date.append(article['creation_date'])
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
    get_articles = requests.post(url_to_hit, json=params)
    articles_json = get_articles.json()
    all_articles = articles_json['articles']
    return create_contents_from_all_articles(all_articles)


def get_categorical_articles(category):
    print(category)
    params = {
        "years": ["2022"],
        "categories": [category],
        "sources": None,
        "page": 1,
        "per_page": 100
    }
    get_articles = requests.post(url_to_hit, json=params)
    articles_json = get_articles.json()
    all_articles = articles_json['articles']
    return create_contents_from_all_articles(all_articles)


# def get_yearly_articles(year):
#     # TODO: Add API CALL
#     params = {'year': year}
#     get_articles = requests.post(api_url_mapper["URL_YEAR"], data=params)
#     all_articles = get_articles['articles']
#     return create_contents_from_all_articles(all_articles)


def get_articles_from_source(source):
    params = {
        "years": ["2022"],
        "categories": None,
        "sources": source,
        "page": 1,
        "per_page": 100
    }

    get_articles = requests.post(url_to_hit, json=params)
    articles_json = get_articles.json()
    all_articles = articles_json['articles']
    return create_contents_from_all_articles(all_articles)
