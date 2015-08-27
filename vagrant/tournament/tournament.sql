-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Delete the database and its contents
DROP DATABASE IF EXISTS tournament;
DROP TABLE IF EXISTS player CASCADE;
DROP TABLE IF EXISTS tournament_details CASCADE;
DROP TABLE IF EXISTS match CASCADE;
DROP TYPE IF EXISTS result_of_match;


-- Begin database and table creation
CREATE DATABASE tournament;

CREATE TABLE player (
	player_id		serial			primary key	not null,
	name			text			not null,
	date_added		timestamp without time zone default (now() at time zone 'utc')
);

CREATE TABLE tournament_details (
	tournament_id	serial primary key not null,
	num_rounds		smallint,
	start_date		timestamp without time zone,
	end_date		timestamp without time zone
);

CREATE TYPE result_of_match AS ENUM('win', 'lose', 'draw');

CREATE TABLE match (
	tournament_id	int						references tournament_details(tournament_id)	not null,
	player_1_id		int						references player(player_id),
	player_2_id		int						references player(player_id),
	start_date		timestamp without time zone,
	end_date		timestamp without time zone,
	round_num		smallint,
	is_completed	boolean	default false,
	match_result	result_of_match
);

-- connect to the db so we can interact with it
\c tournament;

