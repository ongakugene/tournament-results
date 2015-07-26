# Tournament Results
### Repository: tournament-results
#### *Note : This repository contains the code for an educational project. No copyright infringement is intended.

The project uses a Psycopg Python module alongside a Postgresql database to keep track of players and matches in a game tournament.



## Quick start

To run the project, Python and Psycopg2 module needs to be installed on the system ::

- [Download the latest release](https://github.com/ongakugene/tournament-results/archive/master.zip)
    or
- Clone the repo: `git clone https://github.com/ongakugene/tournament-results.git`.
- On the shell, navigate into the project directory: `cd path/to/tournament-results`
- In psql run: `\i tournament.sql`
- This will create the empty database and the required schema for the tables. 
- Unit tests can be run using the command: `python tournament_tests.py`
- The project assumes an even number of players and no ties in the matches.