How to model a bracket?
A bracket has a list of rounds
A round has a list of matchups
A matchup has a pair of slots, a winner, a region, and 0-2 source matchups
A slot has a team, a seed
A team has a name and image

Notes:
The source should belong to the slot because otherwise, a different slot will have
to be used for each game a team plays in.
Giving a matchup source matchups should work, as long as we map the slot to the
source matchup it came from.

Testing the model

TeamRecords
    TeamRecord
        id: trw
        name: W
        img_link: image w
    TeamRecord
        id: trx
        name: X
        img_link: image x
    TeamRecord
        id: try
        name: Y
        img_link: image y
    TeamRecord
        id: trz
        name: Z
        img_link: image z
        
SlotRecords
    SlotRecord
        id: sr1
        team_id: trw
        seed: 1
    SlotRecord
        id: sr2
        team_id: trx
        seed: 2
    SlotRecord
        id: sr3
        team: team y
        seed: 3
    SlotRecord
        id: sr4
        team: team z
        seed: 4

BracketRecord
    name: Unfilled
    round_records:
        RoundRecord
            matchup_records:
                MatchupRecord
                    id: mr1_1
                    slot_one_id: sr1
                    slot_two_id: sr4
                    winner_slot_id: None
                    region: None
                    source_matchup_one_id: None
                    source_matchup_two_id: None
                MatchupRecord
                    id: mr1_2
                    slot_one_id: sr2
                    slot_two_id: sr3
                    winner_slot_id: None
                    region: None
                    source_matchup_one_id: None
                    source_matchup_two_id: None
        RoundRecord
            matchup_records:
                MatchupRecord
                    id: mr2_1
                    slot_one_id: None
                    slot_two_id: None
                    winner_slot_id: None
                    region: None
                    source_matchup_one_id: mr1_1
                    source_matchup_two_id: mr1_2

BracketRecord
    name: Filled
    round_records:
        RoundRecord
            matchup_records:
                MatchupRecord
                    id: mr1_1
                    slot_one_id: sr1
                    slot_two_id: sr4
                    winner_slot_id: sr1
                    region: None
                    source_matchup_one_id: None
                    source_matchup_two_id: None
                MatchupRecord
                    id: mr1_2
                    slot_one_id: sr2
                    slot_two_id: sr3
                    winner_slot_id: sr2
                    region: None
                    source_matchup_one_id: None
                    source_matchup_two_id: None
        RoundRecord
            matchup_records:
                MatchupRecord
                    id: mr2_1
                    slot_one_id: sr1
                    slot_two_id: sr2
                    winner_slot_id: sr1
                    region: None
                    source_matchup_one_id: mr1_1
                    source_matchup_two_id: mr1_2
        
        
                    
              
                    
        

How to update the bracket?
Send list of (matchup_id, winner_id)
    a. source matchup ids are fixed, so we only need to set winners
    b. difficulty here is validating there are no holes in the bracket
        i. i.e. slot a is winner of matchup 3, but matchup 2 has no winner
        ii. i think we have trace all of the winners through regardless


**TODO**  
1. REEEEEEEMIX: Create a bracket  
1. Create brackets collection and teams collection


1. Make subject metadata in rankings table editable  
a. Open text editor on click cell  
b. Save on click out   
1. Export to csv on demand in ranked order  
a. Create util for copying and appending to CSV  
b. Write subjects to csv using Squarespace product csv template  
c. Verify that CSV can be uploaded to Squarespace Commerce
1. Create class level normalizer (i.e. A, Class-A and Class A => Class A)
  
**Setup**  
_$ virtualenv flask_  
_$ flask/bin/pip install flask_  
_$ flask/bin/pip install flask-restful_  
_$ flask/bin/pip install flask_cors_  
_$ flask/bin/pip install Flask-PyMongo_  
_$ flask/bin/pip install pytest-mock_  
_$ flask/bin/pip install -U pytest_  

**Run**  
_$ ./app.py_  

**Unit Test**  
_$ flask/bin/python -m pytest test/_  

**Test**  
_$ mongo thisorthat_  
_$ db.subjects.find()_  

_$ curl http://localhost:5000/api/bracket/hatz | json_pp_
_$ curl http://localhost:5000/api/subjects | json_pp_
_$ curl http://localhost:5000/api/ranking | json_pp_  
_$ curl http://localhost:5000/api/scrape -X POST_   
_$ curl http://localhost:5000/api/import -X POST_  
_$ curl -H "Content-Type: application/json" -X POST -d '{"name": "final_four"}' http://localhost:5000/api/bracket_  
_$ curl http://localhost:5000/api/bracket/final_four | json_pp_  

  
  
**Sources**
1. https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
2. https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
3. https://flask-cors.readthedocs.io/en/latest/
4. https://flask-pymongo.readthedocs.io/en/latest/
