# Domain Model

## Model

### Option 1: Rounds Model

* TEAM has name, ID, image link
* PARTICIPANT is a TEAM with a SEED
* SEED is a unique identifier (number)
* MATCHUP has two PARTICIPANTS, a WINNER, and a source MATCHUP
* WINNER is a PARTICIPANT
* ROUND is a list of MATCHUP
* BRACKET is a list of ROUNDS, has an ID, user, created timestamp, last modified timestamp, hash of FIELD, hash of SEEDING
* FIELD is a set of TEAMS
* SEEDING is a set of PARTICIPANTS

### Option 2: Matchup Model

* TEAM has name, ID, image link
* PARTICIPANT is a TEAM with a SEED
* SEED is a unique identifier (number)
* MATCHUP has two PARTICIPANTS, a WINNER, and a source MATCHUP
* WINNER is a PARTICIPANT
* BRACKET is the final MATCHUP, has an ID, user, created timestamp, last modified timestamp, hash of FIELD, hash of SEEDING
* FIELD is a set of TEAMS
* SEEDING is a set of PARTICIPANTS

## Collections

* BRACKETS


# Use Cases

## Creating a Bracket

1. Create a list of teams.
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

1. Get all BRACKET with FIELD hash=?

## Compare All Brackets For a Seeding

1. Get all BRACKET with SEEDING hash=?

## Get Finishing Position of a Participant

1. BFS for the team, where each level adds R^2, where R is the number of games from the final. 
  1. i.e. a team that loses in the Elite Eight finished in `1^2 + 2^2 = 5th place`, where `1 = final, 2 = final four, etc`