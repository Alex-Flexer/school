create table users (
    user_id INTEGER PRIMARY KEY,
    user_name VARCHAR(50),
    created_at DATETIME
);

create table copy_orders (
    order_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

insert into copy_orders
select order_id, product_id, NULL FROM orders;

drop table orders;

alter table copy_orders
rename to orders;

insert into users (user_name, created_at)
values
('alex', '12.12.1984 23:59:59'),
('boris', '12.12.1984 23:59:59'),
('valdislav igorevich lazar', '01.00.127 12:00:01');

delete from orders;
insert into orders (product_id, user_id)
values
(1, 1),
(2, 1),
(2, 2),
(3, 3);

select * from orders;
select * from users;
