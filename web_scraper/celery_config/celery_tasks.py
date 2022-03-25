import datetime
import logging
import time
import traceback
from typing import Set, Text, List
from urllib.error import HTTPError
from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup

from web_scraper import celery_app
from web_scraper.common.constants import site_map_url_cnn, cnn_url
from web_scraper.scraper.cnn_scraper import scrape_year_cnn
from web_scraper.scraper.fox_scraper import scrape_fox, prepare_feed_url
from web_scraper.scraper.core import get_xml_soup

logger = logging.getLogger(__name__)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(datetime.timedelta(minutes=15), simple_task.s(), name='simple_task')


@celery_app.task(name='simple_task')
def simple_task():
    try:
        time.sleep(100)
    except Exception as e:
        logger.error(e)


@celery_app.task(name='scrape_cnn_articles')
def scrape_cnn_articles(selected_years: List[Text], metadata):
    selected_years = set(selected_years)
    page_soup = None
    article_num = 0

    try:
        client = uReq(site_map_url_cnn)
        site_map_html = client.read()
        client.close()
        # html parsing
        page_soup = soup(site_map_html, "html.parser")
    except HTTPError:
        error_msg_top = "".join(["HTTP Error in title in top site: ",
                                 site_map_url_cnn, "\n"])
        logger.error(error_msg_top)
        logger.error(traceback.format_exc())
        raise

    # gets each year
    years = page_soup.find("ul", {"class": "sitemap-year"}).findAll("li", {"class": "date"})

    # iterate over all years to find the selected_year and go to that year page
    for year in years:
        if year.text.strip() in selected_years:
            selected_year_url = cnn_url + year.a["href"]
            try:
                uYearClient = uReq(selected_year_url)
                selected_year_html = uYearClient.read()
                uYearClient.close()
                page_soup = soup(selected_year_html, "html.parser")
            except HTTPError:
                error_msg_year = "".join(["HTTP Error in year: ",
                                          selected_year_url, "\n"])
                logger.error(error_msg_year)
                logger.error(traceback.format_exc())
                continue

            try:
                article_num += scrape_year_cnn(cnn_url, page_soup, metadata)
            except AttributeError:
                error_msg_year = "".join(["Attribute Error in year: ",
                                          selected_year_url, "\n"])
                logger.error(error_msg_year)
                logger.error(traceback.format_exc())
                continue


@celery_app.task(name='scrape_fox_articles')
def scrape_fox_articles(metadata):
    prev_feed_url = ""
    feed_url = prepare_feed_url(None)
    num_articles = 0
    while prev_feed_url != feed_url:
        try:
            _ = get_xml_soup(feed_url)  # check if rss feed url is valid
            num_articles += scrape_fox(feed_url=feed_url, metadata=metadata)
            prev_feed_url = feed_url
            feed_url = prepare_feed_url(feed_url)
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return True
    return True

# @celery_app.task(task="send_aws_sms")
# def send_aws_sms(message, phone_number):
#     response = sms_client.publish(PhoneNumber=phone_number, Message=message)
#     return response
