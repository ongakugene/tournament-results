-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS db_tournament;

CREATE DATABASE db_tournament;

-- Connecting to the database
\c db_tournament;

CREATE TABLE tbl_players(
	id SERIAL PRIMARY KEY NOT NULL,
	name TEXT NOT NULL
);

CREATE TABLE tbl_matches(
	p1_id INT REFERENCES tbl_players(id),
	p2_id INT REFERENCES tbl_players(id),
	winner_id INT REFERENCES tbl_players(id)
);
