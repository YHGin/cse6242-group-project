DROP TABLE IF EXISTS stock_price;
DROP TABLE IF EXISTS index_price;

Create table stock_price
(
    date   timestamp,
    ric    text,
    open   float,
    high   float,
    low    float,
    close  float,
    volume integer
);
Create table index_price
(
    date   timestamp,
    ric    text,
    open   float,
    high   float,
    low    float,
    close  float,
    volume integer
);
