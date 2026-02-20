-- Active: 1770062672705@@mysql-1c7e1346-sulemanabdulmanan-5813.l.aivencloud.com@22696@ecommerce_db
CREATE DATABASE ecommerce_db;

CREATE TABLE events (
    event_id VARCHAR(100) PRIMARY KEY,
    user_id INT,
    product_id INT,
    product_name VARCHAR(100),
    event_type VARCHAR(50),
    price INT,
    event_time TIMESTAMP
);