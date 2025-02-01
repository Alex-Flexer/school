create table copy_orders (
    order_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES copy_products (id) ON DELETE CASCADE
);

insert into copy_orders
select * from orders;

drop table orders;

alter table copy_orders
rename to orders;
