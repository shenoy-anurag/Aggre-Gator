import logging
from urllib.error import HTTPError
from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup

logger = logging.getLogger(__name__)


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
        raise HTTPError


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
