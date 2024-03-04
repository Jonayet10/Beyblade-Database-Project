-- Granting permission to admins and clients of beybladedb
DROP USER IF EXISTS 'jlavin'@'localhost';
DROP USER IF EXISTS 'alinazhang'@'localhost';
DROP USER IF EXISTS 'dpasha'@'localhost';
DROP USER IF EXISTS 'gokus'@'localhost';
DROP USER IF EXISTS 'midoriyai'@'localhost';

-- Create admins (BeyAdmin)
CREATE USER 'jlavin'@'localhost' IDENTIFIED BY 'jlavinpw';
CREATE USER 'alinazhang'@'localhost' IDENTIFIED BY 'alinazhangpw';
CREATE USER 'dpasha'@'localhost' IDENTIFIED BY 'dpashapw';

-- Create clients (Bladers)
CREATE USER 'gokus'@'localhost' IDENTIFIED BY 'gokuspw';
CREATE USER 'midoriyai'@'localhost' IDENTIFIED BY 'midoriyaipw';

-- Grant all priveleges to BeyAdmins

GRANT ALL PRIVILEGES ON beybladedb.* TO 'jlavin'@'localhost';
GRANT ALL PRIVILEGES ON beybladedb.* TO 'alinazhang'@'localhost';
GRANT ALL PRIVILEGES ON beybladedb.* TO 'dpasha'@'localhost';

-- Grant priveleges to Bladers

-- Grant SELECT permission on beyblades and parts tables to Bladers
GRANT SELECT ON beybladedb.beyblades TO 'gokus'@'localhost';
GRANT SELECT ON beybladedb.parts TO 'gokus'@'localhost';
GRANT SELECT ON beybladedb.userbeyblades TO 'gokus'@'localhost';
GRANT SELECT ON beybladedb.beyblades TO 'midoriyai'@'localhost';
GRANT SELECT ON beybladedb.parts TO 'midoriyai'@'localhost';
GRANT SELECT ON beybladedb.userbeyblades TO 'midoriyai'@'localhost';

-- Grand SELECT permission on users to all clients
GRANT SELECT ON beybladedb.users TO 'gokus'@'localhost';
GRANT SELECT ON beybladedb.users TO 'midoriyai'@'localhost';

-- Grant INSERT, UPDATE, and DELETE permissions on userbeyblades table to Bladers
GRANT INSERT, UPDATE, DELETE ON beybladedb.userbeyblades TO 'gokus'@'localhost';
GRANT INSERT, UPDATE, DELETE ON beybladedb.userbeyblades TO 'midoriyai'@'localhost';

-- Grant EXECUTE permission on the AddCustomBeyblade procedure to Bladers
-- This allows Bladers to perform actions encapsulated by the procedure, even
-- if they don't have direct permissions to perform those actions on the
-- underlying tables ('beyblades' table)
GRANT EXECUTE ON PROCEDURE beybladedb.AddCustomBeyblade TO 'gokus'@'localhost';
GRANT EXECUTE ON PROCEDURE beybladedb.AddCustomBeyblade TO 'midoriyai'@'localhost';
GRANT EXECUTE ON FUNCTION beybladedb.authenticate TO 'gokus'@'localhost';
GRANT EXECUTE ON FUNCTION beybladedb.authenticate TO 'midoriyai'@'localhost';

GRANT SELECT ON beybladedb.battles TO 'gokus'@'localhost';
GRANT SELECT ON beybladedb.battles TO 'midoriyai'@'localhost';

FLUSH PRIVILEGES;
