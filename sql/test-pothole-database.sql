DROP DATABASE IF EXISTS test_pothole_reporting;

CREATE DATABASE test_pothole_reporting;

USE test_pothole_reporting;

CREATE TABLE pothole (
    id INT NOT NULL AUTO_INCREMENT,
    lat DECIMAL(11, 8) NOT NULL,
    lon DECIMAL(11, 8) NOT NULL,
    create_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE site_user (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(32) NOT NULL UNIQUE,
    first_name VARCHAR(32) NOT NULL,
    last_name VARCHAR(32) NOT NULL,
    email VARCHAR(64) NOT NULL,
    pword VARCHAR(128) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY(id)
);

CREATE TABLE pothole_ledger (
    id INT NOT NULL AUTO_INCREMENT,
    fk_pothole_id INT NOT NULL,
    fk_user_id INT NOT NULL,
    state TINYINT NOT NULL,
    submit_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (fk_pothole_id) REFERENCES pothole(id),
    FOREIGN KEY (fk_user_id) REFERENCES site_user(id)
);