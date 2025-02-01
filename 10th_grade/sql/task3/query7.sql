create table copy_products (
    id INTEGER,
    name VARCHAR(50),
    price FLOAT,
    CHECK (price > 0)
);

insert into copy_products (id, name, price)
select id, name, price from products;

drop table products;

alter table copy_products
rename to products;

-- checking:
-- insert into products (name, price)
-- values ('chiken', -12);
