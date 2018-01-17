import csv

from bson import ObjectId

from model.record import TeamRecord

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


def get_team_records_from_csv(input_filepath):
    # type: (str) -> list[TeamRecord]
    with open(input_filepath, 'rb') as f:
        reader = csv.reader(f)
        team_lines = list(reader)

    return [to_team_record(team_line) for team_line in team_lines[1:]]


def to_team_record(team_line):
    # type: (str) -> TeamRecord
    return TeamRecord(_id=ObjectId(), name=team_line[NAME], img_link=team_line[IMG_LINK])
