SELECT * FROM stock_price where ric in ('00002.HK','00001.HK','00003.HK','00005.HK') and date <= date('2023-06-02') and  date >= date('2023-06-01');
SELECT * FROM index_price where ric = '.HSI' and date <= date('2023-06-02') and  date >= date('2023-06-01')


SELECT distinct ric FROM stock_price;