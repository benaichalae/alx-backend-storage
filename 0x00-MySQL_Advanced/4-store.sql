-- SQL script that lists all bands
-- Initial
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS orders;

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL DEFAULT 10
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    number INT NOT NULL,
    FOREIGN KEY (item_name) REFERENCES items(name)
);

INSERT INTO items (name) VALUES ("apple"), ("pineapple"), ("pear");

