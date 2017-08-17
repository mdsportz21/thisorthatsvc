#!/usr/bin/python

import csv
import re
from urllib2 import HTTPError

from bs4 import NavigableString
from nltk import tokenize

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
    soup = scraper_utils.get_soup(url)
    img_tags = soup.find_all('img', class_='loading')
    img_links = [img_tag['data-src'] for img_tag in img_tags]
    desc_tags = soup.find_all('div', class_='project-title')
    descriptions = [scraper_utils.get_soup_contents_by_tag(desc_tag) for desc_tag in desc_tags]
    assert len(img_links) == len(descriptions)
    for img_link, description in zip(img_links, descriptions):
        subject_dto = SubjectDTO(imgDesc=description, description=description, imgLink=img_link)
        results.append(subject_dto)
    return results


def get_teams_from_lids():
    # type: () -> list[str]
    """
    Input:
    <li class="facet-value-container">
        <a id="team-facet-148" class="facet-link" data-seoslug="/team_vermont-lake-monsters" href="/milb/fitted/men/team_vermont-lake-monsters" >
            <span class="facet-value facet-name">Vermont Lake Monsters</span>
            <span class="facet-value-count"> (4)</span>
        </a>
    </li>

    Selector:
    a with id="team-facet*"

    Output:
    Vermont Lake Monsters
    https://www.lids.com/milb/fitted/men/team_vermont-lake-monsters

    :return:
    """
    url_resource_name = 'https://www.lids.com'
    url = url_resource_name + '/milb/fitted/men'
    soup = scraper_utils.get_soup(url)
    team_link_elements = soup('a', id=re.compile('team-facet'))
    team_links = [url_resource_name + a.get('href') for a in team_link_elements]
    team_names = ['' + a.find('span', 'facet-name').string for a in team_link_elements]
    team_lines = []
    for team_name, team_link in zip(team_names, team_links):
        team_lines.append(team_name + ',' + team_link)
    return team_lines


def get_teams_from_milb():
    # type: () -> list[str]
    """
    <div id="MiLB1" class="collapse accordionWrapper">
        ...
        <li class="alt hidden  vermont_lake_monsters">
            <a class="" href="/MiLB_Vermont_Lake_Monsters_Fitted_Caps" title="Vermont Lake Monsters" data-talos="filter" data-filter-value="Vermont Lake Monsters" >Vermont Lake Monsters</a>
        </li>
        ...
    </div>
    :return:
    """
    url = 'http://www.mlbshop.com/MiLB_Fitted_Caps'
    soup = scraper_utils.get_soup(url)
    # get all <a data-talos> inside of <div id=MiLB1>
    # milb_div = soup.find(id='MiLB1')
    team_links = soup.select('#MiLB1 a[data-talos]')
    team_names = [team_link['title'] for team_link in team_links]
    return team_names


def get_wiki_info(input_filepath='../resources/Hatz import metadata.csv'):
    """
    Pseudocode:

    Read team names from csv
    For each team name
        construct wikipedia URL
        scrape page
        get state and description

    This needs to fail gracefully and return empty for both if the page is not found.

    Example: https://en.wikipedia.org/wiki/Albuquerque_Isotopes

    :return: list[object[state, description]]
    """

    # Get Teams From CSV
    with open(input_filepath, 'rb') as f:
        reader = csv.reader(f)
        team_data = list(reader)
    team_names = [team_line[0] for team_line in team_data][1:]
    team_lines = []
    url_to_first_sentences_cache = {}

    for team_name in team_names:
        # Construct wiki URL
        wiki_url = 'https://en.wikipedia.org/wiki/' + team_name.replace(' ', '_')

        if wiki_url in url_to_first_sentences_cache:
            print 'Retrieving ', wiki_url, 'from cache'
            [team_name, first_sentences, is_defunct, is_real, city, state, major_league_affiliate, class_level] = \
                url_to_first_sentences_cache[wiki_url]
        else:
            print 'Evaluating ', wiki_url
            first_sentences = ''
            is_defunct = False
            is_real = False
            city = ''
            state = ''
            major_league_affiliate = ''
            class_level = ''
            try:
                soup = scraper_utils.get_soup(wiki_url)

                # check if valid page
                if soup.find(string=re.compile(
                        'Wikipedia does not have an article with this exact name')) is None and soup.find(
                    string=re.compile(
                        'you may wish to change the link to point directly to the intended article')) is None:

                    # Get first two sentences of first paragraph
                    # get contents of <p> after <table class="infobox"
                    infobox_table = soup.find('table', 'infobox')
                    intro_paragraph = infobox_table.find_next_sibling('p')
                    intro_paragraph_contents = scraper_utils.get_contents(intro_paragraph)
                    first_sentences = ' '.join(
                        tokenize.sent_tokenize(re.sub('<[^<]+?>', '', intro_paragraph_contents))[:2])

                    # real teams should exist in Wikipedia
                    is_real = first_sentences is not ''

                    # Determine if team is current of defunct
                    mla_th = soup.find('th', string=re.compile('Major league affiliations'))
                    if mla_th is not None:
                        mla_tr = mla_th.parent
                        mla_tr_sibling = mla_tr.find_next_sibling('tr')
                        is_defunct = mla_tr_sibling.find('th', scope='row', string=re.compile('Current')) is None

                        # Major League Affiliate
                        mla_recent_team_link = mla_tr_sibling.td.a
                        major_league_affiliate = scraper_utils.get_contents(mla_recent_team_link)

                    # City & State
                    city_state_link = infobox_table.find('a', title=re.compile(', '), href=re.compile('/wiki/'))
                    if city_state_link is not None:
                        city_state = city_state_link['title']

                        # Not every page has a category link
                        # sports_category_link = soup.find('a', title=re.compile('Category:Sports in'))
                        # if sports_category_link is not None:
                        #     sports_category_link_title = sports_category_link['title']
                        #     city_state = sports_category_link_title.split('Category:Sports in ')[1]

                        if ',' in city_state:
                            [city, state] = city_state.split(', ')
                        else:
                            city = city_state

                    class_level_th = soup.find('th', string=re.compile('Class-level'))
                    if class_level_th is not None:
                        # class_level_th.parent.find_next_sibling('tr').find('td')
                        class_level_tr = class_level_th.parent.find_next_sibling('tr')
                        if class_level_tr is not None:
                            class_level_td = class_level_tr.find('td')
                            if class_level_td.a is not None and not bool(
                                    re.search(r'\d', scraper_utils.get_contents(
                                        class_level_td.a))):
                                class_level = scraper_utils.get_contents(class_level_td.a)
                            elif class_level_td.div is not None and len(class_level_td.div.contents) > 0 and type(
                                    class_level_td.div.contents[0]) is NavigableString and '\n' not in \
                                    class_level_td.div.contents[0]:
                                class_level = unicode(class_level_td.div.contents[0])
                            elif class_level_td is not None and len(class_level_td.contents) > 0 and type(
                                    class_level_td.contents[0]) is NavigableString and '\n' not in \
                                    class_level_td.contents[0]:
                                class_level = unicode(class_level_td.contents[0])
                            # Filter out " (1980 - present)"
                            if " (" in class_level:
                                class_level = class_level[:class_level.index(" (")]

            except HTTPError:
                print 'Error', wiki_url, 'not found'  # Invalid page
                pass

        team_line = '|'.join(
            [team_name, first_sentences, str(is_defunct), str(is_real), city, state, major_league_affiliate,
             class_level])
        # print team_line
        team_lines.append(team_line)
        if wiki_url not in url_to_first_sentences_cache:
            url_to_first_sentences_cache[wiki_url] = [team_name, first_sentences, is_defunct, is_real, city, state,
                                                      major_league_affiliate, class_level]

    return team_lines


if __name__ == '__main__':
    # teams = get_teams_from_milb()
    # team_lines = get_teams_from_lids()

    # team_lines = get_wiki_info('../resources/test_shit.csv')
    team_lines = get_wiki_info()
    print '\nPrinting team lines...\n'
    print 'team_name|first_sentences|is_defunct|is_real|city|state|major_league_affiliate|class_level'
    print '\n'.join(team_lines)
