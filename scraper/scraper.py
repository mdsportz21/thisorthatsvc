#!/usr/bin/python

import scraper_utils
import re
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


def get_wiki_info(teams):
    """
    Pseudocode:

    For each team name
        construct wikipedia URL
        scrape page
        get state and description

    This needs to fail gracefully and return empty for both if the page is not found.

    :return: list[object[state, description]]
    """
    pass


if __name__ == '__main__':
    # teams = get_teams_from_milb()
    team_lines = get_teams_from_lids()
    print '\n'.join(team_lines)
