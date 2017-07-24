#!/usr/bin/python
import urllib2

import scraper_utils
from model.dto import SubjectDTO


def get_subject_dtos():
    # type: () -> list[SubjectDTO]
    """

    create records from hatz.squarespace.com

    :return: subject records
    """
    results = []
    url = 'https://hatz.squarespace.com/milb-dope'
    req = urllib2.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})
    page = urllib2.urlopen(req).read()
    soup = scraper_utils.get_soup(page)
    img_tags = soup.find_all('img', class_='loading')
    img_links = [img_tag['data-src'] for img_tag in img_tags]
    desc_tags = soup.find_all('div', class_='project-title')
    descriptions = [scraper_utils.get_soup_contents_by_tag(desc_tag) for desc_tag in desc_tags]
    assert len(img_links) == len(descriptions)
    for img_link, description in zip(img_links, descriptions):
        subject_dto = SubjectDTO(imgDesc=description, description=description, imgLink=img_link)
        results.append(subject_dto)
    return results
