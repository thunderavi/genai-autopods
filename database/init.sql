-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS autopods_db;

-- Use the newly created database
USE autopods_db;

-- Drop the pods table if it exists (for re-initialization purposes)
DROP TABLE IF EXISTS pods;

-- Create the pods table
CREATE TABLE pods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    project_description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (name)  -- Ensure pod names are unique
);

-- Insert initial data into the pods table
INSERT INTO pods (name, project_description) VALUES
('Pod A', 'Description for Pod A'),
('Pod B', 'Description for Pod B'),
('Pod C', 'Description for Pod C');
