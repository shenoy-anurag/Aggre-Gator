import copy
import logging
import time
import traceback
from typing import Text
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen as uReq

import bs4
from bs4 import BeautifulSoup as soup
from dateutil.parser import parse

from web_scraper.common.constants import (
    PUBLISHER_FOX, FOX_bias, FOX_NEWS_QUERY_ARGS, site_map_url_fox
)
from web_scraper.core.models import Article, save_fox_articles_mongo
from web_scraper.elastic.elastic_write import save_articles_es

logger = logging.getLogger(__name__)


def get_article(article_url):
    try:
        article_client = uReq(article_url)
        html_content = article_client.read()
        article_client.close()
        article_soup = soup(html_content, "html.parser")
        return article_soup
    except HTTPError:
        error_msg_title = "".join(["HTTP Error in title in article: ",
                                   article_url, "\n"])
        logger.error(error_msg_title)
        raise HTTPError


def get_xml_soup(url):
    try:
        xml_client = uReq(url)
        xml_content = xml_client.read()
        xml_client.close()
        xml_soup = soup(xml_content, "lxml-xml")
        return xml_soup
    except HTTPError:
        error_msg_title = "".join(["HTTP Error in title in article: ",
                                   url, "\n"])
        logger.error(error_msg_title)
        return None


def prepare_feed_url(curr_feed_url: Text = None):
    q_str = urlencode(FOX_NEWS_QUERY_ARGS)
    base_feed_url = site_map_url_fox + "?" + q_str
    if not curr_feed_url:
        return base_feed_url

    feed_soup = get_xml_soup(curr_feed_url)

    if feed_soup:
        urls = feed_soup.find_all('url')
        last_article_modified = urls[-1].find_next("lastmod").get_text()
        last_article_modified = parse(last_article_modified)
        unix_ts = int(last_article_modified.timestamp() * 1000)
        new_args = copy.deepcopy(FOX_NEWS_QUERY_ARGS)
        new_args["from"] = unix_ts
        q_str = urlencode(new_args)
        new_feed_url = site_map_url_fox + "?" + q_str
        return new_feed_url
    else:
        return base_feed_url


def parse_fox_article(article_url, article_soup: bs4.BeautifulSoup, date_modified):
    article = Article(url=article_url)
    # Article's title is present in heading 1
    try:
        article.title = article_soup.h1.text
    except AttributeError:
        error_msg_title = "".join(["Attribute Error in title in article: ",
                                   article_url, "\n"])
        logger.error(error_msg_title)
        raise

    article_modified_date = parse(date_modified.text)
    article.modified_date = article_modified_date
    article_date = article_soup.find_all("div", {"class": "article-date"})
    if article_date:
        article_published_date = article_date[0].find("time").get_text()
        article_published_date = parse(article_published_date)
        article.day = article_published_date.day
        article.year = article_published_date.year
        article.month = article_published_date.month
        article.creation_date = article_published_date

    # div class ="author-byline" >
    author_details = article_soup.find_all("div", {"class": "author-byline"})
    if author_details:
        article.author = author_details[0].find("a").get_text()
        article.author_url = author_details[0].find("a").attrs.get("href")

    # Finding all paragraphs of the article's contents
    article_paragraphs = article_soup.findAll("p")

    # retrieve article's contents
    article_content = ""
    try:
        for a_paragraph in article_paragraphs:
            text = a_paragraph.text.strip()
            article_content = '\n'.join([article_content, text])
    except AttributeError:
        error_msg_content = "".join([
            "Attribute Error in content in article: ", article_url, "\n"])
        logger.error(error_msg_content)

    article.article = article_content

    # number of characters in article content
    article_length = len(article_content)
    article.character_length = article_length

    topic = article_soup.find("div", {"class": "eyebrow"}).find("a")
    topic_url = topic.get("href")
    category_url_base = "https://www.foxnews.com/category/"
    topics = topic_url.partition(category_url_base)
    topics = topics[-1].split("/")
    article.topic = topics[0]
    article.tags = topics

    article.publisher = PUBLISHER_FOX
    article.bias = FOX_bias
    return article


def scrape_fox(feed_url, metadata):
    page_soup = None
    start_time = time.time()
    num_articles = 0
    try:
        client = uReq(feed_url)
        site_map_xml = client.read()
        client.close()
        # xml parsing
        page_soup = soup(site_map_xml, "lxml-xml")
    except HTTPError:
        error_msg_top = "".join(["HTTP Error in title in top site: ",
                                 feed_url, "\n"])
        logger.error(error_msg_top)
        logger.error(traceback.format_exc())
        raise

    urls = page_soup.find_all('url')
    article_objs = []
    try:
        for url_block in urls:
            page_url = url_block.find_next("loc")
            try:
                modified = url_block.find_next("lastmod")
                # xml parsing
                article_soup = get_article(article_url=page_url.get_text())
                article_obj = parse_fox_article(article_url=page_url.get_text(), article_soup=article_soup,
                                                date_modified=modified)
                article_objs.append(article_obj)
                num_articles += 1
                if num_articles % 50 == 0:
                    save_fox_articles_mongo(article_objs=article_objs)
                    save_articles_es(article_objs=article_objs, metadata=metadata)
                    article_objs = []
                    logger.info(
                        "{} {} {} {}".format(feed_url.rsplit("/")[-1], modified, page_url, time.time() - start_time))
            except Exception as e:
                error_msg_top = "".join(["Error in parsing article: ",
                                         page_url, ", ", str(e), "\n"])
                logger.error(error_msg_top)
                logger.error(traceback.format_exc())
                continue
    except HTTPError:
        error_msg_top = "".join(["HTTP Error in title in top site: ",
                                 feed_url, "\n"])
        logger.error(error_msg_top)
        logger.error(traceback.format_exc())

    # save_fox_articles_mongo(article_objs=article_objs)
    # save_articles_es(article_objs=article_objs, metadata=metadata)

    return num_articles
