CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    name VARCHAR(1024) NOT NULL,
    author VARCHAR(100),
    publication_year INTEGER,
    edition TEXT,
    wardrobe_id INTEGER,
    shelf_id INTEGER
);

CREATE TABLE IF NOT EXISTS debtors (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    book_id INTEGER
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULl,
    surname VARCHAR(50) NOT NULL,
    patronymic VARCHAR(50),
    license_id INTEGER NOT NULL,
    address TEXT
);