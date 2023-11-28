# cse6242-group-project
This is the team project for cse6242, OMS-BackTestor

### project defintion:
1. This is a webapp tool for user test stock porfolio performance.
2. project entry point: run /oms_6242_project/module_interface/app_run.py
3. framework used in this tool: 
   1. frontend: dash/flask
   2. backend: sqlite db

### git management tip, if you use pycharm/intellij/mobaxterm, open terminal and do following
0. git config --system http.sslverify false
1. git clone https://github.com/YHGin/cse6242-group-project.git
2. git checkout -b feature/{your_name}
3. git commit -m "cse6242:first commit"
4. git push to remote your feature
   
### my project proposal 
reference site: https://algotrading101.com/learn/backtesting-py-guide/

### python env control
Would recommand to create a new python venv to avoid package conflict
1. please follow link: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/ 
1. pip install requirment.txt
2. set up project structure for each module

### modules definitions
1. module-core
   1. this module track portfolio performance with given start and end time, input csv
   2. there are 3 container class track down the result, and 2 enum class to control the keeps
      1. Portfolio: entire stock portfolio status
      2. Stock: single stock status
      3. Trade: stock daily movement status
   4. There is a parent Testor and child buy-hold testor class
      1. The child buyhold testor - BuyHoldBT, assume portfolio are selected and leave untouched through entire duration
      2. By Design, the parent - BTcore, has genric method to produce stock, portfolio level profit and lost info that applied to all other child class

2. module-datalayer
   1. this module has function to fill price data into sqlite database and provide get api to retrieve data by input:stock name,start day and end day
3. module-interface
   1. this module is the part launch web interface that use dash/flask server, it has below feature
      1. allow user to sumbit a csv contain stock portfolio, 
         1. sample portfolio path: /oms_6242_project/module_interface/resource/data/portfolio.csv
      2. allow user to review the composition of the portfolio
      3. allow user to track both single stock and portfolio level performance
      4. allow user to compare portfolio performance verse benchmark
4. module-stratgy
   1. this an independent module that create portfolio base on whatever analytics
5. module-utlity
   1. data operation uti methods

