# StockUtils

Utils to process stock data 

## Requirements 

* Numpy 
* Pandas 
* Quandls 
* AlphaVantage 
* ta-lib (For TechProcs) 
* fast.ai (optional) 


## Notes

TechProcs that wrap ta-lib are legacy now and replaced with [Procs](https://github.com/marvin-hansen/StockUtils/blob/master/src/procs/Procs.py) that fetch technical indicators from AlphaVantage. 

However, the TechProcs source code is still there for cases when pulling data and indicators from AlphaVantage isn't an option
or when a very specific indicator or chart patterns is needed. 


## Install 


```python

  wget https://github.com/marvin-hansen/StockUtils/blob/master/StockUtils.zip
  unzip StockUtils.zip

```


## Getting started

Sample code in the main file. 


## Features

1) Cached DataLoader 
2) Various data-preprocessors (procs) 
3) Various technical indicators (from AlphaVantage) 


The default cachedNetLoader fetches data from AlphaVantage, stores them locally in a CSV file, and returns a pandas dataframe so that a  developer does not have to deal with JSON at all.  Proc's do a myriad of transformations or feature generators to the loaded data. 


Transformational procs: 

* Split data in train & test 
* Rename column 
* Delete column 
* Convert date (from object to DateTime) 
* Categorify Date 

Categorify Date requires fast.ai 1.0.5 and it splits a (continoius) DateTime value into corresponding categorial values to capture trends, time-patterns, and cycles. 

Feature generator procs: 

* Add delta-n (difference to previous n values) 
* Add percentage change 
* Add n-previous values (add n-previous values as columns for row-wise processing
* Add Technical Indicators

Supported are several Technical Indicators provided by AlphaVantage (web API) and these are added as seperated columns by merging over the date column. DO NOT DELETE THE DATE COLUMN BEFORE ADDING ANY PROC. If your model does need or cannot handle datetime, remove it at the very last step to ensure all other procs are working correctly.

A complete list of implemented procs is codified in the [corrspodning PROC ENUM](https://github.com/marvin-hansen/StockUtils/blob/master/src/enum/PROCS.py)





