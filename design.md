# Domain Model

## Matchup Model

### Schema

* TEAM has name, ID, image link, abbreviation
* PARTICIPANT is a TEAM with a SEED
  * SEED is a unique identifier (number)
* MATCHUP has two PARTICIPANTS and two source MATCHUP
* BRACKET has a "final" REGION_MATCHUP , an ID, user, created timestamp, last modified timestamp, pickle of tuple of FIELD, pickle of tuple of SEEDING
  * FIELD is a set of TEAM IDs
  * SEEDING is a map of region ID to seed to TEAM ID
* REGION_MATCHUP has two REGION, and two source REGION_MATCHUP
* REGION has a name and size, and a "final" MATCHUP

### Collections

* BRACKETS
* TEAMS

### Sample Data

```
{
  "bracket": {
    "id": "XXX",
    "user": "mdsportz21@gmail.com",
    "created_timestamp": "2019-04-06 21:36:00Z",
    "last_modified_timestamp": "2019-04-06 21:36:00Z",
    "field": "",
    "seeding": "",
    "region_matchup": {
      "region_one": {
        "name": "final four",
        "size": 4,
        "matchup": {
          "participant_one": null,
          "participant_two": null,
          "source_matchup_one": {
            "participant_one": {
              "name": "Auburn",
              "id": "XXX",
              "img_link": "XXX",
              "seed": "5"
            },
            "participant_two": {
              "name": "Virginia",
              "id": "XXX",
              "img_link": "XXX",
              "seed": "1"
            },
            "source_matchup_one": null,
            "source_matchup_two": null
          },
          "source_matchup_two": {
            "participant_one": {
              "name": "Texas Tech",
              "id": "XXX",
              "img_link": "XXX",
              "seed": "3"
            },
            "participant_two": {
              "name": "Michigan State",
              "id": "XXX",
              "img_link": "XXX",
              "seed": "2"
            },
            "source_matchup_one": null,
            "source_matchup_two": null
          }
        }
      },
      "region_two": null,
      "source_region_matchup_one": null,
      "source_region_matchup_two": null
    }
  }
}
```

# Implementation Details

```
from bson.binary import Binary
from bson import ObjectId
import pickle

field = (ObjectId(), ObjectId(), ObjectId())
```
    >>> (ObjectId('5ca91d68a8d8062f3a24f436'), ObjectId('5ca91d68a8d8062f3a24f437'), ObjectId('5ca91d68a8d8062f3a24f438'))

```
saved_field = pickle.dumps(field)
binary_saved_field = Binary(saved_field)
pickle.loads(binary_saved_field)
```
    >>> (ObjectId('5ca91d68a8d8062f3a24f436'), ObjectId('5ca91d68a8d8062f3a24f437'), ObjectId('5ca91d68a8d8062f3a24f438'))
   

# Use Cases

## Creating a Bracket from Scratch

### Scenario

I want to create the 2019 NCAA Tournament Bracket

### Option 1: Spreadsheet

1. User uploads a spreadsheet of TEAMS, SEEDS and REGIONS
1. Backend validates, constructs, and saves BRACKET
1. Frontend displays the BRACKET
1. User fills out the BRACKET
1. Backend saves user's choices in BRACKET
1. User shares a link to User 2 to fill out the bracket
1. User 2 hits the URL
1. Backend creates and saves new BRACKET based on SEEDING
1. Frontend display BRACKET

### Option 2: UI

1. User creates a list of teams / selects from existing list of teams
1. Frontend constructs empty bracket
1. User drags and drops teams into the first round of the bracket
1. Backend validates and saves the bracket
1. User fills out the bracket
1. User shares the bracket

### Option 3: Use Pre-Existing Bracket

1. Tim creates brackets in backend
1. UI loads list of brackets to choose from
1. User selects bracket and optionally to randomize seedings
1. Backend creates and saves bracket from FIELD and/or SEEDING


## Managing a Set of Teams

1. 

## Creating a Bracket from a Set of Teams

1. Select a list of teams.
1. Assign each team a seed.
1. Create rounds of matchups based on the seeds.

## Filling Out a Bracket

1. Starting from the first round, assign a winner to each matchup.

## Two Users Fill Out Same Bracket

1. Deep copy of BRACKET.
1. Clear all winners.

## Randomize Seeding of an Existing Brackets

1. Get all unique TEAMS in a BRACKET.
1. Assign each TEAM a SEED.
1. Create ROUNDS of MATCHUPS based on the SEEDS.

## Fetch Most Recent Bracket

1. Get BRACKET with most recent edited timestamp.

## Compare All Brackets For a Field

1. Get all BRACKET with FIELD pickle=?

## Compare All Brackets For a Seeding

1. Get all BRACKET with SEEDING pickle=?

## Get Finishing Position of a Participant

1. BFS for the team, where each level adds R^2, where R is the number of games from the final. 
  1. i.e. a team that loses in the Elite Eight finished in `1^2 + 2^2 = 5th place`, where `1 = final, 2 = final four, etc`
  

# Archive

## Model

### Rounds Model (Old)

* TEAM has name, ID, image link
* PARTICIPANT is a TEAM with a REGION and SEED
* SEED is a unique identifier (number)
* MATCHUP has two PARTICIPANTS, a WINNER, and a source MATCHUP
* WINNER is a PARTICIPANT
* ROUND is a list of MATCHUP
* BRACKET is a list of ROUNDS, has an ID, user, created timestamp, last modified timestamp, pickle of FIELD, pickle of SEEDING, REGIONS
* FIELD is a set of TEAM IDs
* SEEDING is a set of PARTICIPANTS 