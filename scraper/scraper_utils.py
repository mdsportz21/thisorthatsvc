#!/usr/bin/python

import urllib2

from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag
from ratelimiter import RateLimiter
import re


def get_soup_contents_by_tag(tag, tag_name=None, prop_name=None, prop_value=None):
    # type: (BeautifulSoup, str, str, str) -> Tag | NavigableString
    """

    Example Usage:
        scraper_utils.get_soup_contents_by_tag(soup, 'strong', 'class', 'test')
        Input: '<li><strong>Redeemable </strong><strong class="test">Miles: </strong>1,950 miles</li>'
        Output: <strong class="test">Miles: </strong>

    :param tag:
    :param tag_name:
    :param prop_name:
    :param prop_value:
    :return:
    """
    contents = tag.contents
    for content in contents:
        if tag_name is None:
            if isinstance(content, NavigableString):
                return strip(content)
        else:
            if isinstance(content, Tag) and content.name == tag_name:
                if prop_name is None or tag_contains(content, prop_name, prop_value):
                    return content
    return None


def tag_contains(tag, prop_name, prop_value=None):
    return prop_name in tag.attrs and (prop_value is None or prop_value in tag.attrs[prop_name])


def strip(word, remove_newlines=True, remove_commas=False, encode_contents=True, strip_html_tags=False):
    # type: (str, bool, bool) -> str
    """
    :param word: word to strip
    :param remove_newlines:
    :param remove_commas:
    :return: stripped word
    """
    if word is not None:
        if strip_html_tags:
            word = re.sub('<[^<]+?>', '', word)
        if remove_newlines:
            word = word.replace('\n', '').replace('\r', '')
        if remove_commas:
            word = word.replace(',', '')
        if encode_contents:
            word = word.encode('ascii', 'ignore')
    return word.strip()


@RateLimiter(max_calls=1, period=1)
def get_soup(url):
    # type: (str) -> BeautifulSoup
    req = urllib2.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})
    page = urllib2.urlopen(req).read()
    return BeautifulSoup(page, "lxml")


def get_contents(tag):
    # type: (Tag) -> str
    return ''.join([unicode(content_el) for content_el in tag.contents])