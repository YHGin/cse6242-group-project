DROP TABLE IF EXISTS stock_price;
DROP TABLE IF EXISTS index_price;

Create table stock_price
(
    date   text,
    ric    text,
    high   float,
    low    float,
    close  float,
    volume integer
);
Create table index_price
(
    date   text,
    ric    text,
    high   float,
    low    float,
    close  float,
    volume integer
);


SELECT * FROM stock_price where ric = '00001.HK';
SELECT * FROM stock_price where ric = '00002.HK';
SELECT * FROM stock_price where ric in ('00002.HK','00001.HK',);
SELECT * FROM index_price where ric = '.HSI'