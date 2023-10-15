"""
Make a portfolio
"""
from module_datalayer.reader import DbReader
from module_core.container.portfolio import Portfolio
from module_core.container.stock import Stock,run_stock_test

def make_portofolio():
    portfolio = Portfolio()
    stock1 = run_stock_test("00001.HK")
    stock1 = run_stock_test("00002.HK")


if __name__ == '__main__':
    make_portofolio()