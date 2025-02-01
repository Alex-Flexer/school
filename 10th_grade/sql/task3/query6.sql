alter table products
add column temp_price FLOAT;

update products
set temp_price = price;

alter table products
drop column price;

alter table products
rename column temp_price to price;
