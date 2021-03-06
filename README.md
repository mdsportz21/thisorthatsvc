**Run**
_$ source ./bin/activate
_$ python runserver.py

**Deploy to Server**
_$ cd thisorthatsvc_
_$ git push heroku master_
_$ heroku logs --tail_

**Setup**
_$ virtualenv flask_
_$ flask/bin/pip install flask_
_$ flask/bin/pip install flask-restful_
_$ flask/bin/pip install flask_cors_
_$ flask/bin/pip install Flask-PyMongo_
_$ flask/bin/pip install pytest-mock_
_$ flask/bin/pip install -U pytest_

**Setup 2**
_$pip install -r requirements.txt

**Unit Test**
_$ flask/bin/python -m pytest test/_

**Test**
_$ mongo thisorthat_
_$ db.subjects.find()_

_$ curl http://localhost:5000/api/bracket | json_pp_
_$ curl http://localhost:5000/api/subjects | json_pp_
_$ curl http://localhost:5000/api/ranking | json_pp_
_$ curl http://localhost:5000/api/scrape -X POST_
_$ curl http://localhost:5000/api/import -X POST_

Get a list of brackets
_$ curl http://localhost:5000/api/bracket | json_pp_

Create Bracket
_$ curl -H "Content-Type: application/json" -X POST -d '{"seedingStrategy": "random", "bracketSize":8}' http://localhost:5000/api/bracket/5b552322d6f45f189b117fbf/demo_
_$ curl -H "Content-Type: application/json" -X POST -d '{"name": "15"}' http://localhost:5000/api/bracket_
_$ curl -H "Content-Type: application/json" -X POST -d '{"user": "tim", "seedingStrategy": "random", "bracketFieldId":"5b552322d6f45f189b117fbf"}' http://localhost:5000/api/bracket > bracket.json_

Get Bracket
_$ curl http://localhost:5000/api/bracket/15 | json_pp > bracket_20180317.json_



**Sources**
1. https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
2. https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
3. https://flask-cors.readthedocs.io/en/latest/
4. https://flask-pymongo.readthedocs.io/en/latest/
5. https://www.codexpedia.com/devops/mongodb-authentication-setting/
6. https://devcenter.heroku.com/articles/config-vars
7. http://api.mongodb.com/python/current/examples/authentication.html - authenticating mlab queries
8. https://github.com/auth0/auth0-python - auth0 python (might need to use this)
9. https://auth0.com/docs/api-auth/tutorials/verify-access-token - verify token on backend
10. https://auth0.com/blog/navigating-rs256-and-jwks/ - verify token example
11. https://auth0.com/learn/json-web-tokens/ - front end token format

**Troubleshooting**
1. https://stackoverflow.com/questions/11150343/slow-requests-on-local-flask-server

Todo
----
10-11-18:
0. Install dropdown component

9-29-18:
0. Draw the page
1. show dropdown of bracket instances or login button at top
2. Show collapsible dropdown with bracket fields list below bracket instance / login section
3. Show (unauthenticated) demo bracket or selected  to home page below bracket fields dropdown
c. show demo below
2. Add label to existing bracket field list section.
3. Create bracket instance list section under existing bracket field list section.
a. "Create new bracket" should be permanent top item of the bracket instance list
b. Display created on / updated on in bracket instance list
4. Load existing bracket instance
5. Autogenerate name for new bracket instance
6. Display bracket instance name
7. Make bracket instance name editable
8. Implement bracket instance save on frontend
9. Implement bracket instance save validation on backend


9-14-18:
1. Restore mongo locally from data dump (/Users/mdsportz21/Documents/devel/mongodb/dumps/user_dumps/thisorthat.20180912)
2. Migrate bracket_fields to server
3. Test that bracket field fetch works on server

8-2-18: Turn all classes into modules
package: bracket
    init.py
        - imports the following modules (http://intermediate-and-advanced-software-carpentry.readthedocs.io/en/latest/structuring-python.html)
        - has the "controller" methods, which should take in and return dtos, and thus manage conversion
    models.py - both records and dtos, now featuring conversion
    storage.py - repository & storage methods


  
What's the difference between a bracket and a bracket entry?  
<br>Bracket:
1. Playin matchups
2. 1st round matchups
3. matchup map aka bracket skeleton

bracket: {
    name: 'elite_eight'
    rounds: [{
        matchups: [{
            team_one_id: '',
            team_two_id: '',
            source_matchup_one_id: '',
            source_matchup_two_id: ''
        }...]
    }...],
    teams: [{
        id: '',
        name: '',
        img_link: '',
        seed: 1
    }]
}

bracket_entry: {
    id: '',
    email: '',
    name: 'tims_1st_entry',
    bracket_id: '',
    winners: [{
        matchup_id: '',
        winner_team_id: ''
    }...]
}

bracket_dto: {
    name: '',
    bracket_entry_id: '',
    rounds: [{
        matchups: [{}]
    }],
    teams: [{}]
}

bracket_entry_request: {
    bracket_id: '',
    email: '',
    index: 0 (optional)
}

bracket_entry_response: {
    bracket_entry_id: ''
    winners: [{}]
}

should i fill in the winners on the frontend or backend?
* either way. we can do it on the backend since it'll be faster / less work for the frontend.
* backend definitely needs to validate the bracket now (i think we already are).



Todo:
~~1. Change MatchupDTO.*slotId to *teamId~~
~~2. Create a UI for de-duping hat links~~
3. Make server URL configurable and connect this thing to heroku
3. when creating brackets from teams, exclude where duplicate == true
    * for all teams, set grouping to milb_hats
    * create getAllTeamsByGroupingCall
    * create bracket from list of team ids
        * team ids = non-excluded teams with milb grouping
4. on ui/svc, create bracket_entry_request
    * bracket_id - ID of bracket
    * email - email address of user, so we can send them results
    * index - (optional) allows user to create multiple bracket entries
5. translate from BracketDTO to BracketEntryRecord
    * validate team IDs come from source matchup IDs
    * validate winnerId is one of the teamIds
    * for each MatchupDTO, if winnerTeamId exists, set winners[matchupId] to winnerTeamId
    * save to db
        * save initial bracket entry on request, that way we have somewhere to put it on first save
        * if the bracket entry id exists, update it with the winners
6. translate from BracketRecord & BracketEntryRecord to BracketDTO
    * create BracketDTO from BracketRecord
    * for each winner in BracketEntryRecord
        * find the matchupDTO and set its winner
    * send to frontend
11. return hybrid bracket & bracket entry
* reconstruct BracketDTO winners (on MatchupDTO) using bracket entry record


8. ~~on ui/svc, create bracket_entry_response~~
* ACTUALLY maybe we should keep the front end as is
* And the service should construct the BracketEntryRecord from the MatchupDTOs
* This would
a. make it easier to validate
b. make it consistent on the frontend. so...


6. add dropdown which shows list of available brackets

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