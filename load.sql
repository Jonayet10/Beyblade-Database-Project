-- Instructions:
-- This script will load the 4 CSV files you broke down from playlist_data.csv
-- into the tables you created in setup-spotify.sql.
-- Intended for use with the command-line MySQL, otherwise unnecessary for
-- phpMyAdmin (just import each CSV file in the GUI).

-- Make sure this file is in the same directory as your 5 CSV files and
-- setup.sql. Then run the following in the mysql> prompt (assuming
-- you have a spotifydb created with CREATE DATABASE spotifydb;):
-- USE DATABASE beybladedb; 
-- source setup.sql; (make sure no warnings appear)
-- source load-beyblade.sql; (make sure there are 0 skipped/warnings)

-- Load the data for users table
LOAD DATA LOCAL INFILE 'users.csv' INTO TABLE users
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

-- Load the data for parts table
LOAD DATA LOCAL INFILE 'parts.csv' INTO TABLE parts
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

-- Load the data for beyblades table
LOAD DATA LOCAL INFILE 'beyblades.csv' INTO TABLE beyblades
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

-- Load the data for userbeyblades table
LOAD DATA LOCAL INFILE 'userbeyblades.csv' INTO TABLE userbeyblades
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

-- Load the data for battles table
LOAD DATA LOCAL INFILE 'battles.csv' INTO TABLE battles
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;
