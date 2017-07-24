from scraper import scraper
from scraper.scraper_utils import get_soup


def test_scrape_page():
    with open('resources/hatz.html') as fp:
        soup = get_soup(fp)
        img_tags = soup.find_all('img', class_='loading')
        desc_tags = soup.find_all('div', class_='project-title')
        assert len(img_tags) == 2
        assert len(desc_tags) == 2


def test_get_subject_dtos():
    scraper.get_subject_dtos()


if __name__ == '__main__':
    test_get_subject_dtos()
