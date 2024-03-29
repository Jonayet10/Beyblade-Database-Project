-- Remove existing tables to prevent errors on creation
DROP TABLE IF EXISTS battles;
DROP TABLE IF EXISTS userbeyblades;
DROP TABLE IF EXISTS beyblades;
DROP TABLE IF EXISTS parts;
DROP TABLE IF EXISTS users;

-- Table for storing user informaiton
CREATE TABLE users (
    -- Unique identifier for each user
    user_ID INT AUTO_INCREMENT PRIMARY KEY,
    -- Username of user
    username VARCHAR(250) NOT NULL,
    -- Email address of user
    email VARCHAR(250) NOT NULL UNIQUE,
    -- Flag to indicate whether the user has administrative priveleges
    is_admin BOOLEAN NOT NULL,
    -- The date and time the user joined
    date_joined DATETIME NOT NULL
);

-- Table for storing compilation of beyblade parts
CREATE TABLE parts (
    -- Unique identifier for each part
    part_ID VARCHAR(20) PRIMARY KEY,
    -- Type of the part 
    part_type ENUM('Face Bolt', 'Energy Ring', 'Fusion Wheel', 'Spin Track', 'Performance Tip') NOT NULL,
    -- Weight of the part in grams
    weight DECIMAL(4,2),
    -- Brief description of the part
    description TEXT
);

-- Table for storing parts and aspects that make up a single beyblade
CREATE TABLE beyblades (
    -- Unique identifier for each Beyblade
    beyblade_ID VARCHAR(10) PRIMARY KEY,
    -- Name of the Beyblade
    name VARCHAR(250) NOT NULL,
    -- Type of the Beyblade
    type ENUM('Attack', 'Defense', 'Stamina', 'Balance') NOT NULL,
    -- Flag to indicate whether the Beyblade is custom-made
    is_custom BOOLEAN NOT NULL,
    -- Series the Beyblade is from
    series ENUM('Metal Fusion', 'Metal Masters', 'Metal Fury') NOT NULL,
    -- Foreign keys linking to the parts table
    face_bolt_ID VARCHAR(20),
    energy_ring_ID VARCHAR(20),
    fusion_wheel_ID VARCHAR(20),
    spin_track_ID VARCHAR(20),
    performance_tip_ID VARCHAR(20),
    FOREIGN KEY (face_bolt_ID) REFERENCES parts(part_ID),
    FOREIGN KEY (energy_ring_ID) REFERENCES parts(part_ID),
    FOREIGN KEY (fusion_wheel_ID) REFERENCES parts(part_ID),
    FOREIGN KEY (spin_track_ID) REFERENCES parts(part_ID),
    FOREIGN KEY (performance_tip_ID) REFERENCES parts(part_ID)
);

-- Table for linking users with their Beyblades
CREATE TABLE userbeyblades (
    -- Unique identifier for user-owned Beyblades
    user_beyblade_ID INT AUTO_INCREMENT PRIMARY KEY,
    -- References the owner of the Beyblade
    user_ID INT NOT NULL,
    -- Reference the Beyblade owned by the user
    beyblade_ID VARCHAR(10) NOT NULL,
    FOREIGN KEY (user_ID) REFERENCES users(user_ID)
        ON DELETE CASCADE, -- if user is deleted in users table, their Beyblades are also deleted from userbeyblades table
    FOREIGN KEY (beyblade_ID) REFERENCES beyblades(beyblade_ID)
);

-- Table for storing battle results
CREATE TABLE battles (
    -- Unique identifier for each Battle
    battle_ID INT AUTO_INCREMENT PRIMARY KEY,
    -- Name of the tournament the battle is from
    tournament_name VARCHAR(250),
    -- Date of the battle
    date DATETIME NOT NULL,
    -- Lovation of the battle
    location VARCHAR(250) NOT NULL,
    -- References to the players and their Beyblades invovles in the battle
    player1_ID INT NOT NULL,
    player2_ID INT NOT NULL,
    player1_beyblade_ID INT NOT NULL,
    player2_beyblade_ID INT NOT NULL,
    winner_ID INT, -- Can be NULL if battle was draw
    -- delete player1's battle history if player1's user_ID is deleted in users table
    FOREIGN KEY (player1_ID) REFERENCES users(user_ID)
        ON DELETE CASCADE, 
    -- delete player2's battle history if player2's user_ID is deleted in users table
    FOREIGN KEY (player2_ID) REFERENCES users(user_ID)
        ON DELETE CASCADE, 
    FOREIGN KEY (player1_beyblade_ID) REFERENCES userbeyblades(user_beyblade_ID),
    FOREIGN KEY (player2_beyblade_ID) REFERENCES userbeyblades(user_beyblade_ID),
    FOREIGN KEY (winner_ID) REFERENCES userbeyblades(user_beyblade_ID)
);
