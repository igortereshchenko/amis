INSERT INTO clients  (client_id, client_name, age, money, contact, created)
VALUES (1, 'Katia',20, 2000, 0673127886, NOW());

INSERT INTO clients  (client_id, client_name, age, money, contact, created)
VALUES (2, 'Oleh',25, 3500, 098123455, NOW());

INSERT INTO clients  (client_id, client_name, age, money, contact, created)
VALUES (3, 'Olha',33, 1350, 098333456, NOW());

-- 
INSERT INTO tests  (test_id, price, productor, Created, client_idIDFK)
VALUES (1, 1700, 'Ukraine', NOW(), 1);

INSERT INTO tests (test_id, price, productor, Created, client_idIDFK)
VALUES ( 2, 3000, 'China',NOW(), 2);

INSERT INTO tests (test_id, price, productor, Created, client_idIDFK)
VALUES (3, 900, 'Germany', NOW(), 3);



INSERT INTO products (product_id, product_name ,product_price, Created, test_idIDFK)
VALUES (1,'jewellery', 1500, NOW(), 1);

INSERT INTO products  (product_id, product_name ,product_price, Created, test_idIDFK)
VALUES ( 2,'bags', 2700, NOW(), 3);

INSERT INTO products (product_id, product_name ,product_price, Created, test_idIDFK)
VALUES ( 3,'clothe', 900, NOW(), 3);


INSERT INTO shops (shop_id, shop_name ,locale, shop_contact, Created, product_idIDFK)
VALUES (1,'Beauty', 'Kyiv', 044123567, NOW(),1);

INSERT INTO shops (shop_id, shop_name ,locale, shop_contact, Created, product_idIDFK)
VALUES (2, 'All for women', 'Lviv', 012345678, NOW(), 2);

INSERT INTO shops (shop_id, shop_name ,locale, shop_contact, Created, product_idIDFK)
VALUES ( 3,'Clothe', 'Irpin', 067123999, NOW(), 3);

-- 
INSERT INTO vendors (vendor_id, vendor_name, city, rating, year, Created, product_idIDFK)
VALUES (1,'Anna', 'Kyiv', 5, 1999, NOW(),1);

INSERT INTO vendors (vendor_id, vendor_name, city, rating, year, Created, product_idIDFK)
VALUES (2, 'Olya', 'Lviv', 6, 2000, NOW(), 2);

INSERT INTO vendors (vendor_id, vendor_name, city, rating, year, Created, product_idIDFK)
VALUES ( 3,'Kate', 'Odessa', 8, 2001, NOW(), 3);



INSERT INTO inits (init_id, Created, product_idIDFK, client_idIDFK)
VALUES (1, NOW(), 1, 1);

INSERT INTO inits (init_id, Created, product_idIDFK, client_idIDFK)
VALUES (2, NOW(), 2, 2);

INSERT INTO inits (init_id, Created, product_idIDFK, client_idIDFK)
VALUES ( 3, NOW(), 3, 3);


















select * from Clients;
select * from Tests;
select * from Products;
select * from Shops;
select * from Vendors;
select * from Inits;
