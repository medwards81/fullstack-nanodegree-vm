#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    query = "DELETE FROM matches;"
    _delete(query)


def deletePlayers():
    """Remove all the player records from the database."""
    query = "DELETE FROM players;"
    _delete(query)


def countPlayers():
    """Returns the number of players currently registered."""
    query = "SELECT COUNT(player_id) AS player_count FROM players;"
    player_count = _count(query)
    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    query = "INSERT INTO players(name) VALUES(%s);"
    con = connect()
    cur = con.cursor()
    cur.execute(query, (name,))
    con.commit()
    con.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    standings = []
    con = connect()
    cur = con.cursor()

    query = "SELECT player_id, name FROM players;"
    cur.execute(query)
    con.commit()

    players = cur.fetchall()

    player_info = {}
    for player_data in players:
        player_id = player_data[0]
        player_name = player_data[1]
        player_matches = _get_total_matches(player_id)
        player_wins = _get_wins(player_id)

        player_info[player_id] = {}

        player_info[player_id]['id'] = player_id
        player_info[player_id]['name'] = player_name
        player_info[player_id]['matches'] = player_matches
        player_info[player_id]['wins'] = player_wins

    con.close()

    players_sorted = sorted(player_info.items(),
                            key=lambda x: (x[1]['wins']),
                            reverse=True)

    idx = 0
    for player_id, player_data in players_sorted:
        standings.insert(idx, (player_data['id'],
                                       player_data['name'],
                                       player_data['wins'],
                                       player_data['matches']
                                       )
                               )
        idx += 1

    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = "INSERT INTO matches(player_1_id, player_2_id, winner_id) "
    query += "VALUES(%s, %s, %s);"
    con = connect()
    cur = con.cursor()
    cur.execute(query, (winner, loser, winner,))
    con.commit()
    con.close()


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
    pairings = []
    standings = playerStandings()

    for i in range(0, len(standings), 2):
        (id1, name1, id2, name2) = (standings[i][0], standings[i][1],
                                    standings[i+1][0], standings[i+1][1])
        pairings.append((id1, name1, id2, name2))

    return pairings


def _delete(query):
    """Executes the provided delete query against the database"""
    con = connect()
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    con.close()


def _count(query):
    """Executes the provided count query against the database"""
    con = connect()
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    count = cur.fetchone()[0]
    con.close()
    return count


def _get_wins(player_id):
    query = "SELECT COUNT(winner_id) FROM matches"
    query += " WHERE winner_id = %s;" % player_id
    wins = _count(query)
    return wins


def _get_total_matches(player_id):
    query = "SELECT COUNT(match_id) FROM matches WHERE "
    query += "player_1_id = %s OR player_2_id = %s;" % (player_id, player_id)
    total_matches = _count(query)
    return total_matches
