create table categories (
    cat_id INTEGER PRIMARY KEY,
    cat_name VARCHAR(50)
);

create table copy_products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    price FLOAT,
    cat_id INTEGER,
    FOREIGN KEY (cat_id) REFERENCES categories(cat_id)
);

insert into copy_products (id, name, price, cat_id)
select id, name, price, NULL from products;

drop table products;

alter table copy_products
rename to products;
