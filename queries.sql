-- NEED TO FIX ERRORS FOR THIS

-- Retrieves the ID of the heaviest Beyblade of a given type by summing the weights of its parts
SELECT b.beyblade_id INTO heaviest_beyblade_id
FROM beyblades AS b
JOIN parts AS fb ON b.face_bolt_id = fb.part_id
JOIN parts AS er ON b.energy_ring_id = er.part_id
JOIN parts AS fw ON b.fusion_wheel_id = fw.part_id
JOIN parts AS st ON b.spin_track_id = st.part_id
JOIN parts AS pt ON b.performance_tip_id = pt.part_id
WHERE b.type = beyblade_type
GROUP BY b.beyblade_id
ORDER BY SUM(fb.weight + er.weight + fw.weight + st.weight + pt.weight) DESC
LIMIT 1;

-- Retrieves battle details for a specific tournament, including IDs, dates, locations, usernames, Beyblade names, and the winner ID
SELECT b.battle_ID, b.date, b.location, 
           u1.username AS Player1_Username, u2.username AS Player2_Username, 
           bb1.name AS Player1_Beyblade_Name, bb2.name AS Player2_Beyblade_Name, 
           b.player1_beyblade_ID, b.player2_beyblade_ID, b.winner_ID
FROM battles b
JOIN users u1 ON b.player1_ID = u1.user_ID
JOIN users u2 ON b.player2_ID = u2.user_ID
JOIN userbeyblades ub1 ON b.player1_beyblade_ID = ub1.user_beyblade_ID
JOIN beyblades bb1 ON ub1.beyblade_ID = bb1.beyblade_ID
JOIN userbeyblades ub2 ON b.player2_beyblade_ID = ub2.user_beyblade_ID
JOIN beyblades bb2 ON ub2.beyblade_ID = bb2.beyblade_ID
WHERE b.tournament_name = WBBA;

-------------------------- USE THE ABOVE FOR RELATIONAL ALGEBRA SECTION -------------------------------
