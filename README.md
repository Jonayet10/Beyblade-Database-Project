# Beyblade-Database-Project

The GitHub repository establishes a project that constructs a Beyblade database, cataloging Beybalde parts, configurations, and battle outcomes. It features a dual command-line interface, one tailored for a Blader (client) and another for a BeyAdmin (administrator), enabling users to execute a wide variety of functions. These include account creatino, strategic Beyblade assembly based on accessible data, management of their personal Beyblade collection, as well as the analysis of battle statistics for various Beyblades and tournaments.

Before running this program, make sure to install Python MySQL Connector and tabulate with pip. Also, note that this program was tested on MySQL Version 8.2.0.

# Setup Instructions

In your computer's command line, do the following:

$ mysql --local-infile=1 -u root -p

and enter your password accordingly, assuming root is the username being used to log into the MySQL database server and 'mysql' is the command-line client.

Create and use database in the MySQL command-line interface:

mysql> CREATE DATABASE beybladedb;

mysql> USE beybladedb;

Run the following commands to establish the backend of the project:

mysql> SOURCE setup.sql;

mysql> SOURCE load.sql

mysql> SOURCE setup-passwords.sql;

mysql> SOURCE setup-routines.sql;

mysql> SOURCE grant-permissions.sql;

mysql> SOURCE queries.sql;

# Instructions for Running Python Program

Quit out of MySQL CLI:

mysql> quit

If you are a client, run

$ python app-client.py

If you are an admin, run

$ python app-admin.py

The registered admins are:

| USER       | PASSWORD      |
|------------|---------------|
| jlavin     | jlavinpw      |
| alinazhang | alinazhangpw  |
