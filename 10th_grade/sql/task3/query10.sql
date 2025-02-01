CREATE TABLE copy_orders (
    order_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES products (id)
);

INSERT INTO copy_orders
SELECT * FROM orders;

DROP TABLE orders;

ALTER TABLE copy_orders
RENAME TO orders;

CREATE TABLE copy_products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price FLOAT,
    cat_id INTEGER,
    FOREIGN KEY (cat_id) REFERENCES categories (cat_id),
    CHECK (price >= 0)
);

INSERT INTO copy_products
SELECT * FROM products;

DROP TABLE products;

ALTER TABLE copy_products
RENAME TO products;
