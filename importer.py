import csv

from model.dto import SubjectDTO

NAME = 0
IMG_LINK = 2
DESC = 4
DEFUNCT = 5
REAL = 6
CITY = 7
STATE = 8
MLB_AFFILIATE = 9
CLASS_LEVEL = 10

DEFUNCT_TAG = 'DEFUNCT'
DECIDUOUS_TAG = 'DECIDUOUS'


def get_subject_dtos_from_csv(input_filepath):
    with open(input_filepath, 'rb') as f:
        reader = csv.reader(f)
        team_lines = list(reader)

    subject_dtos = []
    for team_line in team_lines[1:]:
        subject_dto = to_subject_dto(team_line)
        subject_dtos.append(subject_dto)
    return subject_dtos


def to_subject_dto(team_line):
    # Headers:
    # name	Shop Link	img_link	Image	first_sentences	is_defunct	is_real	city	state	major_league_affiliate	class_level
    tags = []
    if team_line[DEFUNCT]:
        tags.append(DEFUNCT_TAG)
    if not team_line[REAL]:
        tags.append(DECIDUOUS_TAG)

    subject_dto = SubjectDTO(name=team_line[NAME],
                             imgLink=team_line[IMG_LINK],
                             description=team_line[DESC],
                             tags=tags,
                             address={
                                 'city': team_line[CITY],
                                 'state': team_line[STATE]
                             },
                             affiliate=team_line[MLB_AFFILIATE],
                             level=team_line[CLASS_LEVEL])
    return subject_dto
