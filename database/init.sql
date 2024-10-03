-- init.sql

CREATE DATABASE IF NOT EXISTS autopods_db;

USE autopods_db;

CREATE TABLE IF NOT EXISTS pods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    project_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
