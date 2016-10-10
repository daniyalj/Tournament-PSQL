-- Table definitions for the tournament project.

-- Drop database if it already exists
DROP DATABASE IF EXISTS tournament;

-- creates database called tournament
CREATE DATABASE tournament;

\c tournament;

-- Creates table for players
CREATE TABLE players(
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL
);

-- Creates tables for the round of games
CREATE TABLE matches(
	id SERIAL PRIMARY KEY,
	winner INT REFERENCES players(id),
	loser INT REFERENCES players(id)

);
-- Create view for standings of players
CREATE OR REPLACE View positions_players AS
-- Query to view player positions
	SELECT  players.id AS player_id, name, SUM(CASE WHEN players.id = matches.winner THEN 1 ELSE 0 END) AS victory_count,
	COUNT(matches) AS number_of_rounds
	FROM players
-- Create LEFT OUTER JOIN
	LEFT OUTER JOIN matches
	ON players.id = matches.winner OR players.id = matches.loser
-- GROUPING
	GROUP BY player_id
	ORDER BY victory_count DESC, number_of_rounds ASC;