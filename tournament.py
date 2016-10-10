import psycopg2
from contextlib import contextmanager

def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")

def deleteMatches():
	"""Remove all the match records from the database."""
	with position_db() as position:
		position.execute("DELETE FROM matches")


def deletePlayers():
	"""Remove all the player records from the database."""
	with position_db() as position:
		position.execute("DELETE FROM players")


def countPlayers():
	"""Returns the number of players currently registered."""
	with position_db() as position:
		position.execute("SELECT COUNT(id) FROM players")
		final_count = position.fetchone()[0]
		return final_count


def registerPlayer(name):
	"""Adds a player to the tournament database.
	The database assigns a unique serial id number for the player.  (This
	should be handled by your SQL database schema, not in your Python code.)
	Args:
	  name: the player's full name (need not be unique).
	"""
	with position_db() as position:
		position.execute("INSERT INTO players (name) VALUES (%s)", (name, ))


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
	with position_db() as position:
		position.execute("SELECT * FROM positions_players")
		positions_players = position.fetchall()
		return positions_players


def reportMatch(winner, loser):
	"""Records the outcome of a single match between two players.
	Args:
	  winner:  the id number of the player who won
	  loser:  the id number of the player who lost
	"""
	with position_db() as position:
		position.execute("INSERT INTO matches(loser, winner) VALUES(%s, %s);",(loser, winner))


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
	with position_db() as position:
		position.execute("SELECT player_id, name FROM positions_players")
		standings = position.fetchall()
		pairings = []
		for i in range(0, len(standings), 2):
			pairings.append(standings[i] + standings[i + 1])
		return pairings
		
		
@contextmanager
def position_db():
	"""
	Executes queries using position in DB
	"""
	DB = connect()
	position = DB.cursor()
	yield position
	DB.commit()
	position.close()
	DB.close()