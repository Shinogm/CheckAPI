-- Active: 1696921476499@@127.0.0.1@3306@checador_db
DROP DATABASE IF EXISTS checador_db;

CREATE DATABASE checador_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE checador_db;

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
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(255) NOT NULL,
    domicilio VARCHAR(255) NOT NULL,
    telefono VARCHAR(255) NOT NULL,
    empresa VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    horario VARCHAR(255),
    password VARCHAR(255),
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
);

CREATE TABLE fingerprints (
    id INT NOT NULL AUTO_INCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    fingerprint LONGTEXT NOT NULL,
    tmp BLOB NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_fingerprint_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE user_perms (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    perm_id INT NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_user_perm_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_user_perm_perm FOREIGN KEY (perm_id) REFERENCES permissions (id) ON DELETE CASCADE
);