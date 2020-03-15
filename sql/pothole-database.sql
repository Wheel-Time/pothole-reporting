DROP DATABASE IF EXISTS pothole_reporting;

CREATE DATABASE pothole_reporting CHARACTER SET utf8;

USE pothole_reporting;

CREATE TABLE pothole (
	id INT NOT NULL AUTO_INCREMENT,
    pothole_point POINT NOT NULL,
    create_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    effective_date DATETIME,
    fixed_date DATETIME,
    PRIMARY KEY (id)
);

CREATE TABLE site_user (
	id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(32) NOT NULL UNIQUE,
    first_name VARCHAR(32) NOT NULL,
    last_name VARCHAR(32) NOT NULL,
    email VARCHAR(64) NOT NULL,
    pass VARCHAR(128) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY(id)
);

CREATE TABLE pothole_ledger (
	id INT NOT NULL AUTO_INCREMENT,
    pothole__id INT NOT NULL,
    user__id INT NOT NULL,
    state TINYINT NOT NULL,
    submit_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (pothole__id) REFERENCES pothole(id),
    FOREIGN KEY (user__id) REFERENCES site_user(id)
);