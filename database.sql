CREATE DATABASE calculator;

USE userdb;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(50) UNIQUE,
    email VARCHAR(120) UNIQUE,
    mobile VARCHAR(15),
    dob DATE,
    password_hash VARCHAR(200)
);