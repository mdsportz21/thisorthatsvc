import csv

from bson import ObjectId

from model.record import TeamRecord

NAME = 0
IMG_LINK = 1


def write_team_records_to_csv(teams, output_filepath):
    # type: (list[TeamRecord], str) -> ()
    print('writing file to ' + output_filepath)
    with open(output_filepath, 'w+') as f:
        writer = csv.writer(f, delimiter='|')
        for team_record in teams:
            writer.writerow([team_record.name, team_record.img_link])
    print('file written to ' + output_filepath)


def get_team_records_from_csv(input_filepath):
    # type: (str) -> list[TeamRecord]
    with open(input_filepath, newline='') as f:
        reader = csv.reader(f, delimiter='|')
        return [TeamRecord(name=team_line[NAME], img_link=team_line[IMG_LINK], grouping=team_line[NAME]) for team_line in reader]
