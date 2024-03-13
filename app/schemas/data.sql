-- Active: 1695837029838@@127.0.0.1@3306@

DROP DATABASE IF EXISTS checador;

CREATE DATABASE checador DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE checador;

CREATE TABLE permissions (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY name (name)
);

INSERT INTO permissions (name) VALUES
    ('Admin'),
    ('Trabajador');

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
);

CREATE TABLE fingerprints (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL DEFAULT 2,
    fingerprint TEXT NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_fingerprint_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE user_perms (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    perm_id INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY user_perm (user_id, perm_id),
    CONSTRAINT fk_user_perm_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_user_perm_perm FOREIGN KEY (perm_id) REFERENCES permissions (id) ON DELETE CASCADE
);

