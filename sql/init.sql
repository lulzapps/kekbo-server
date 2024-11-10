CREATE DATABASE IF NOT EXISTS yourdatabase;
ALTER DATABASE yourdatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE yourdatabase;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    passwordstr VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE users CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO users (username, email, passwordstr) VALUES ('user1', 'user1@example.com', 'password1');
