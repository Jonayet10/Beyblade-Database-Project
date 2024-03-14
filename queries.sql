USE beybladedb;
-- app queries :

-- Retrieves the IDs, usernames, emails, is_admin statuses, and date joined
-- of users. 
SELECT user_ID, username, email, is_admin, date_joined
FROM users;

-- Retrieves the beyblade_IDs, names, and custom statuses of beyblades of a 
-- user. 
-- change %s to something else. 
SELECT b.beyblade_ID, b.name, b.is_custom
FROM beyblades b
JOIN beycollection ub ON b.beyblade_ID = ub.beyblade_ID
JOIN users u ON ub.user_ID = u.user_ID
WHERE u.username = 'gokus';

-- Retrieves all beyblades for the user. 
SELECT * FROM beyblades;

-- Retrieves all battle results related to the current user from the 
-- battles table. 
SELECT b.battle_ID, b.tournament_name, b.date, b.location, 
        u1.username AS Player1_Username, u2.username AS Player2_Username, 
        bb1.name AS Player1_Beyblade_Name, bb2.name AS Player2_Beyblade_Name, 
        b.player1_beyblade_ID, b.player2_beyblade_ID, b.winner_ID
FROM battles b
JOIN users u1 ON b.player1_ID = u1.user_ID
JOIN users u2 ON b.player2_ID = u2.user_ID
JOIN beycollection ub1 ON b.player1_beyblade_ID = ub1.user_beyblade_ID
JOIN beyblades bb1 ON ub1.beyblade_ID = bb1.beyblade_ID
JOIN beycollection ub2 ON b.player2_beyblade_ID = ub2.user_beyblade_ID
JOIN beyblades bb2 ON ub2.beyblade_ID = bb2.beyblade_ID
WHERE u1.username = 'gokus' OR u2.username = 'gokus';

-- Retrieves all battle results related to a specified tournament from the
-- battles table. 
SELECT b.battle_ID, b.date, b.location, 
        u1.username AS Player1_Username, u2.username AS Player2_Username, 
        bb1.name AS Player1_Beyblade_Name, bb2.name AS Player2_Beyblade_Name, 
        b.player1_beyblade_ID, b.player2_beyblade_ID, b.winner_ID
FROM battles b
JOIN users u1 ON b.player1_ID = u1.user_ID
JOIN users u2 ON b.player2_ID = u2.user_ID
JOIN beycollection ub1 ON b.player1_beyblade_ID = ub1.user_beyblade_ID
JOIN beyblades bb1 ON ub1.beyblade_ID = bb1.beyblade_ID
JOIN beycollection ub2 ON b.player2_beyblade_ID = ub2.user_beyblade_ID
JOIN beyblades bb2 ON ub2.beyblade_ID = bb2.beyblade_ID
WHERE b.tournament_name = 'WBBA Prelim';

-- Retrieves all battle results related to a specified tournament from the
-- given location. 
SELECT b.battle_ID, b.tournament_name, b.date, 
        u1.username AS Player1_Username, u2.username AS Player2_Username, 
        bb1.name AS Player1_Beyblade_Name, bb2.name AS Player2_Beyblade_Name, 
        b.player1_beyblade_ID, b.player2_beyblade_ID, b.winner_ID
FROM battles b
JOIN users u1 ON b.player1_ID = u1.user_ID
JOIN users u2 ON b.player2_ID = u2.user_ID
JOIN beycollection ub1 ON b.player1_beyblade_ID = ub1.user_beyblade_ID
JOIN beyblades bb1 ON ub1.beyblade_ID = bb1.beyblade_ID
JOIN beycollection ub2 ON b.player2_beyblade_ID = ub2.user_beyblade_ID
JOIN beyblades bb2 ON ub2.beyblade_ID = bb2.beyblade_ID
WHERE b.location = 'NYC';

-- Retrives the information for a specific part given a part_id. 
SELECT part_ID, part_type, weight, description
FROM parts
WHERE part_ID = 'L-Drago II FB';

-- Retrieves the names and weights of all parts that make up a specific 
-- Beyblade.
SELECT p.part_ID, p.part_type, p.weight, p.description
FROM parts p
JOIN beyblades b ON p.part_ID IN (b.face_bolt_ID, b.energy_ring_ID, 
                                  b.fusion_wheel_ID, b.spin_track_ID, 
                                  b.performance_tip_ID)
WHERE b.beyblade_ID = 'BB-60';

-- Gets the ID of the heaviest Beyblade of a specific type. 
SELECT udf_heaviest_beyblade_for_type('Attack') 
    AS heaviest_beyblade_id;

-- Gets the name of a Beyblade for a specified Beyblade ID.
SELECT name 
FROM beyblades 
WHERE beyblade_id = 'BB-60';

-- Selects all parts of Beyblades.
SELECT part_ID, part_type, weight, description 
FROM parts 
ORDER BY part_type, part_ID;

-- Select all tournament names.
SELECT DISTINCT tournament_name 
FROM battles 
ORDER BY tournament_name;

-- Select all locations of battles.
SELECT DISTINCT location 
FROM battles 
ORDER BY location;

-- Select and order all beyblades based off battle wins. 
SELECT bb.beyblade_ID, bb.name, bb.type, COUNT(*) as wins
FROM battles b
INNER JOIN beycollection ub ON b.winner_ID = ub.user_beyblade_ID
INNER JOIN beyblades bb ON ub.beyblade_ID = bb.beyblade_ID
GROUP BY bb.beyblade_ID, bb.name, bb.type
ORDER BY wins DESC, bb.name;
