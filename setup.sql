DROP TABLE IF EXISTS battles;
DROP TABLE IF EXISTS userbeyblades;
DROP TABLE IF EXISTS beyblades;
DROP TABLE IF EXISTS parts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_ID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(250) NOT NULL,
    email VARCHAR(250) NOT NULL UNIQUE,
    is_admin BOOLEAN NOT NULL,
    date_joined DATETIME NOT NULL
);

CREATE TABLE parts (
    part_ID VARCHAR(50) PRIMARY KEY,
    part_name VARCHAR(250) NOT NULL,
    part_type ENUM('Face Bolt', 'Energy Ring', 'Fusion Wheel', 'Spin Track', 'Performance Tip') NOT NULL,
    weight DECIMAL(4,2), -- in grams
    description TEXT
);

CREATE TABLE beyblades (
    beyblade_ID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    type ENUM('Attack', 'Defense', 'Stamina', 'Balance') NOT NULL,
    is_custom BOOLEAN NOT NULL,
    series ENUM('Metal Fusion', 'Metal Masters', 'Metal Fury') NOT NULL,
    face_bolt_ID VARCHAR(50),
    energy_ring_ID VARCHAR(50),
    fusion_wheel_ID VARCHAR(50),
    spin_track_ID VARCHAR(50),
    performance_tip_ID VARCHAR(50),
    FOREIGN KEY (face_bolt_ID) REFERENCES parts(part_ID),
    FOREIGN KEY (energy_ring_ID) REFERENCES parts(part_ID),
    FOREIGN KEY (fusion_wheel_ID) REFERENCES parts(part_ID),
    FOREIGN KEY (spin_track_ID) REFERENCES parts(part_ID),
    FOREIGN KEY (performance_tip_ID) REFERENCES parts(part_ID)
);

CREATE TABLE userbeyblades (
    user_beyblade_ID INT AUTO_INCREMENT PRIMARY KEY,
    user_ID INT NOT NULL,
    beyblade_ID INT NOT NULL,
    FOREIGN KEY (user_ID) REFERENCES users(user_ID)
        ON DELETE CASCADE, -- if user is deleted in users table, their Beyblades are also deleted from userbeyblades table
    FOREIGN KEY (beyblade_ID) REFERENCES beyblades(beyblade_ID)
);

CREATE TABLE battles (
    battle_ID INT AUTO_INCREMENT PRIMARY KEY,
    tournament_name VARCHAR(250),
    date DATETIME NOT NULL,
    location VARCHAR(250) NOT NULL,
    player1_ID INT NOT NULL,
    player2_ID INT NOT NULL,
    player1_beyblade_ID INT NOT NULL,
    player2_beyblade_ID INT NOT NULL,
    winner_ID INT, -- Can be NULL if the battle was a draw or the winner is not recorded
    FOREIGN KEY (player1_ID) REFERENCES users(user_ID)
        ON DELETE CASCADE, -- delete player1's battle history if player1's user_ID is deleted in users table
    FOREIGN KEY (player2_ID) REFERENCES users(user_ID)
        ON DELETE CASCADE, -- delete player2's battle history if player2's user_ID is deleted in users table
    FOREIGN KEY (player1_beyblade_ID) REFERENCES userbeyblades(user_beyblade_ID),
    FOREIGN KEY (player2_beyblade_ID) REFERENCES userbeyblades(user_beyblade_ID),
    FOREIGN KEY (winner_ID) REFERENCES userbeyblades(user_beyblade_ID)
);
