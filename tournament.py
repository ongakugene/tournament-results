import psycopg2
import psycopg2.extras

__author__ = 'ali786'

# !/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#


def connect():
    """Connects to the PostgreSQL database.
       Returns a database connection or error."""
    try:
        conn = psycopg2.connect("dbname=db_tournament")
        return conn
    except:
        print "Unable to connect to the database"


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""DELETE FROM tbl_matches""")
    except:
        print "Deleting matches was not successful"
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""DELETE FROM tbl_players""")
    except:
        print "Deleting matches was not successful"
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT COUNT(*) FROM tbl_players""")
    except:
        print "Counting players was not successful"
    results = cur.fetchone()
    conn.close()
    count = int(results[0])  # Typecasting String to Int
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""INSERT INTO tbl_players(name) VALUES(%s)""", (name,))
    except:
        print "Registering the player was not successful"
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    playerCount = countPlayers()

    # Empty list for standings. This will contain tuples later
    playerStandings = []
    try:
        cur.execute("""SELECT id, name, COUNT(winner_id) AS wins FROM
            tbl_players LEFT JOIN tbl_matches ON
            tbl_players.id = tbl_matches.winner_id GROUP BY
            id ORDER BY wins DESC""")
    except:
        print "Retrieving player standings was not successful"

    results = cur.fetchall()
    for result in results:
        # Now finding number of matches played by the current player
        try:
            cur.execute("""SELECT COUNT(*) AS matches FROM
                tbl_players JOIN tbl_matches ON
                tbl_players.id = tbl_matches.p1_id OR
                tbl_players.id = tbl_matches.p2_id WHERE
                id = %s""", (result['id'],))
        except:
            print "Counting matches played was not successful"
        matchesPlayedResults = cur.fetchone()
        # Typecasting String to Int
        matchesPlayed = int(matchesPlayedResults['matches'])
        # Appending the tuples to the playerStandings list
        playerStandings.append((result['id'],
                                result['name'],
                                result['wins'],
                                matchesPlayed))

    conn.close()
    return playerStandings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""INSERT INTO tbl_matches(p1_id, p2_id, winner_id)
            VALUES(%s, %s, %s)""", (winner, loser, winner))
    except:
        print "Saving the match report was not successful"
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    playerStandingsList = playerStandings()
    # empty list which will contain
    # the players who will play in the next round
    pairings = []
    i = 0
    while i < len(playerStandingsList):
        pairings.append(
            (playerStandingsList[i][0], playerStandingsList[i][1],
             playerStandingsList[i + 1][0], playerStandingsList[i + 1][1]))
        i = i + 2
    return pairings
