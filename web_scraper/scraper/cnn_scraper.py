import logging
import time
import traceback
from typing import List
from urllib.error import HTTPError
from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup

from web_scraper.common.constants import topics, PUBLISHER_CNN, CNN_bias
from web_scraper.scraper.core import get_article
from web_scraper.core.models import Article, save_cnn_articles_mongo
from web_scraper.elastic.elastic_write import save_articles_es

logger = logging.getLogger(__name__)


def parse_cnn_article(topic, article_url, article_soup, date_span, year, month):
    article = Article(url=article_url)
    # Article's title is present in heading 1
    try:
        article.title = article_soup.h1.text
    except AttributeError:
        error_msg_title = "".join(["Attribute Error in title in article: ",
                                   article_url, "\n"])
        logger.error(error_msg_title)
        raise

    article_date = date_span.text[-2:]
    article.day = article_date
    article.year = year
    article.month = month
    article.create_creation_date()

    try:
        images = article_soup.findAll("meta", {"property": "og:image"})
        article.url_image = images[0].get("content")
    except:
        error_msg_content = "".join([
            "Couldn't find image url in article: ", article_url, "\n"])
        logger.error(error_msg_content)

    # Finding all paragraphs of the article's contents
    article_paragraphs = article_soup.findAll("div", {"class": "zn-body__paragraph"})

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
    article.topic = topic
    return article


def scrape_month_cnn(topic, month_soup, month_url) -> List[Article]:
    start_time = time.time()
    article_entries_month = month_soup.findAll(
        "div", {"class": "sitemap-entry"})[1]

    articles_of_month = article_entries_month.findAll("span", {"class": "sitemap-link"})

    dates_of_articles = article_entries_month.findAll("span", {"class", "date"})

    if len(articles_of_month) != len(dates_of_articles):
        msg = ("Mismatch: No. articles != No. dates in this month at "
               + month_url)
        logger.error(msg)

    this_month = dates_of_articles[0].text[-5:-3]
    this_year = dates_of_articles[0].text[:4]

    num_articles_month = len(articles_of_month)

    article_objs = []
    num_articles = 0
    # Scrape all links of a topic for a month:
    for i in range(len(articles_of_month)):
        article_url = articles_of_month[i].a["href"]
        try:
            article_soup = get_article(article_url)
        except Exception as e:
            logger.error(e)
            continue

        try:
            date_span = dates_of_articles[i]
            article_obj = parse_cnn_article(topic=topic, article_url=article_url, article_soup=article_soup,
                                            date_span=date_span, year=this_year, month=this_month)
            article_obj.publisher = PUBLISHER_CNN
            article_obj.tags = [topic]
            article_obj.bias = CNN_bias
            article_objs.append(article_obj)
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            continue

        num_articles += 1

        if i % 10 == 0:
            logger.info("{} {} {} {}/{} {}".format(topic, this_month,
                                                   this_year, i,
                                                   num_articles_month,
                                                   time.time() - start_time))

    return article_objs


def scrape_year_cnn(cnn_url, year_soup, metadata):
    num_articles = 0
    # Find all topics
    sections_of_year = year_soup.findAll("li", {"class": "section"})

    # Finds entries of each month
    topics_of_year = []
    for section in sections_of_year:
        if section.text in topics:
            topics_of_year.append(section)

    # Scrapes all articles of each topic for each month
    for topic in topics_of_year:
        section_month_url = cnn_url + topic.a["href"]
        try:
            month_client = uReq(section_month_url)
            section_month_html = month_client.read()
            month_client.close()
            topic_soup = soup(section_month_html, "html.parser")
        except HTTPError:
            error_msg_title = "".join(["HTTP Error in title in topic: ",
                                       section_month_url, "\n"])
            logger.error(error_msg_title)
            logger.error(traceback.format_exc())
            continue

        # scrapes all articles of a month
        try:
            article_objs = scrape_month_cnn(topic.text, topic_soup,
                                            section_month_url)
            save_cnn_articles_mongo(article_objs=article_objs)
            save_articles_es(article_objs=article_objs, metadata=metadata)
            num_articles += len(article_objs)
        except AttributeError:
            error_msg_month = "".join(["Attribute Error in month: ",
                                       section_month_url, "\n"])
            logger.error(error_msg_month)
            logger.error(traceback.format_exc())
            continue
        except Exception as e:
            print(traceback.format_exc())
            logger.error(e)
            continue

    return num_articles
