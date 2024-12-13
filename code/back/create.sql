DROP DATABASE IF EXISTS hackathon_2024;

CREATE DATABASE hackathon_2024;
USE hackathon_2024;

CREATE TABLE anonymisation(
    id INT PRIMARY KEY AUTO_INCREMENT,
    entities JSON NOT NULL,
    anonymous_pdf_file_path VARCHAR(255) NOT NULL UNIQUE,
    status TINYINT NOT NULL
);