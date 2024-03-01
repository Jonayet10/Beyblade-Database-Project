-- Stored Procedure for adding a custom Beyblade configuration for a user. It
-- checks if the custom Beyblade configuration already exits in the database
-- based on its parts. If it does not exist, the procedure inserst the new
-- configuration into the 'beyblades' table. Then it links this Beyblade to
-- the users by inserting a record into the 'userbeyblades' table, associating
-- the customized Beyblade with the user's account. Notably, beyblade_ID of
-- stock Beyblades in 'beyblades' table are already known VARCHAR types, but
-- we want custom Beyblades in 'beyblades' table to have auto-generated IDs
-- (they can be anything, just to  make sure they are unique). Therefore, 
-- we use UUID() function to generate an ID for each custom Beyblade.

DELIMITER !

CREATE PROCEDURE `sp_add_custom_beyblade`(
    IN _user_id INT,
    IN _name VARCHAR(250),
    IN _type ENUM('Attack', 'Defense', 'Stamina', 'Balance'),
    IN _series ENUM('Metal Fusion', 'Metal Masters', 'Metal Fury'),
    IN _face_bolt_id VARCHAR(20),
    IN _energy_ring_id VARCHAR(20),
    IN _fusion_wheel_id VARCHAR(20),
    IN _spin_track_id VARCHAR(20),
    IN _performance_tip_id VARCHAR(20)
)
BEGIN
    DECLARE _beyblade_id VARCHAR(10);
    DECLARE _exists INT;

    -- Check if the Beyblade already exists based on its parts
    SELECT beyblade_ID INTO _beyblade_id FROM beyblades
    WHERE face_bolt_ID = _face_bolt_id 
    AND energy_ring_ID = _energy_ring_id 
    AND fusion_wheel_ID = _fusion_wheel_id 
    AND spin_track_ID = _spin_track_id 
    AND performance_tip_ID = _performance_tip_id
    LIMIT 1;

    IF _beyblade_id IS NULL THEN
        -- Generate a new beyblade_ID using MD5 and UUID, and take first 10 chars
        SET _beyblade_id = LEFT(MD5(UUID()), 10);

        -- Attempt to insert the new custom Beyblade with the generated ID
        INSERT INTO beyblades (beyblade_ID, name, type, is_custom, series, face_bolt_ID, energy_ring_ID, fusion_wheel_ID, spin_track_ID, performance_tip_ID)
        VALUES (_beyblade_id, _name, _type, TRUE, _series, _face_bolt_id, _energy_ring_id, _fusion_wheel_id, _spin_track_id, _performance_tip_id);
    END IF;

    -- Link the Beyblade (new or existing) to the user
    INSERT INTO userbeyblades (user_ID, beyblade_ID)
    VALUES (_user_id, _beyblade_id);
    -- Note that user_beyblade_ID attribute of 'userbeyblades' table is auto-incremented INT, so
    -- don't need to explicitly provide a value for this when inserting
END !

DELIMITER ;
