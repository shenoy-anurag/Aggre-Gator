from app import app
from flask import render_template
from .config import category_mapper
from .request import *


@app.route('/test/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h1>'


@app.route('/')
def home():
    article = get_articles_for_home()
    return render_template('home.html', articles=article)


@app.route('/sources/fox')
def fox():
    fox_news_articles = get_articles_from_source("FOX_NEWS")
    return render_template('news.html', sources=fox_news_articles)


@app.route('/sources/cnn')
def cnn():
    cnn_news_articles = get_articles_from_source("CNN")
    return render_template('news.html', sources=cnn_news_articles)


@app.route('/category/business')
def business():
    source = get_categorical_articles(category_mapper["CATEGORY_BUSINESS"])
    return render_template('news.html', sources=source)


@app.route('/category/tech')
def tech():
    source = get_categorical_articles(category_mapper["CATEGORY_TECHNOLOGY"])
    return render_template('news.html', sources=source)


@app.route('/category/entertainment')
def entertainment():
    source = get_categorical_articles(category_mapper["CATEGORY_ENTERTAINMENT"])
    return render_template('news.html', sources=source)


@app.route('/category/science')
def science():
    source = get_categorical_articles(category_mapper["CATEGORY_SCIENCE"])
    return render_template('news.html', sources=source)


@app.route('/category/sports')
def sports():
    source = get_categorical_articles(category_mapper["CATEGORY_SPORTS"])
    return render_template('news.html', sources=source)


@app.route('/category/health')
def health():
    source = get_categorical_articles(category_mapper["CATEGORY_HEALTH"])
    return render_template('news.html', sources=source)


# @app.route('/year/2021')
# def year_2021():
#     source = get_yearly_articles(2021)
#     return render_template('news.html', sources=source)


# @app.route('/year/2022')
# def year_2022():
#     source = get_yearly_articles(2022)
#     return render_template('news.html', sources=source)
