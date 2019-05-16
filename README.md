# StockUtils

Util collection to accelerate Deep Learnign experiments on stock market data. 
Currently pre-alpha code with frequent breaking changes. 

## Example 


```python

    print("Loading Data for stock: " + stock.name)
    df_all = n.load_data(stock, TimeFrame.TimeFrame.DAILY, full=all_data)
    
    print("Create a ProcFlow")
    pf = ProcFlow(DBG)
    
    print("Applying pre-processor: ", proc_flow_id, "on stock: " + stock.name)
    df_all = pf.proc_switch(data=df_all, stock=stock, y_col="Close", nr_n=5, proc_id=proc_flow_id)
    
    print("Split df_all in train & test")
    train_df, test_df = pf.split_data(df=all_data, split_ratio=0.80, vrb=True)
```

Full example code [here](https://github.com/marvin-hansen/StockUtils/blob/master/src/preps/Preperator.py)  


## Install 


```python

  git clone https://github.com/marvin-hansen/StockUtils.git

```



## Features

1) Cached DataLoader 
2) Various data-preprocessors (procs) 
3) Various technical indicators (from AlphaVantage) 
4) Data splitting (train & test)
5) ProcFlow 
6) Portfolio related metrics 


## Metrics 

The class BaseMetrics implements the following metrics:

* DailyReturns 
* Daily volatilty 
* Sharpe ratio 
* information ratio
* M2 Ratio (Modigliani)
* F1 score (Precision / Recall)


## Cached DataLoader

The default cachedNetLoader fetches data from the web, stores them locally in a CSV file, and returns a pandas dataframe so that a  developer does not have to deal with JSON at all.  Proc's do a myriad of transformations or feature generators to the loaded data.
The DataLoader interface can be implemented for any other data provider. A stub for Quandl is there 
and a complete implementation for AlphaVantage is there.  


## Procs & ProcFlow 

Procs are data pre-processors with each doing exactly one thing only, for instance adding percentage change 
or adding simple moving average. A number of procs have been implemented in the utils. For details, inspect the source.procs folder.
Many procs can be daisy chained and isolated in a single workflow, so called ProcFlows.

Pre-processor-worklows, ProcFlows, simplify data pre-processing as each apply a well 
specified formula of how to prepare the data. The proc_switch allows easy switching between
ProcFlows as to compare different ProcFlows on the same data or as to apply the same ProcFlow on different data. 
It is good practice to stuff every new idea in a seperate ProcFlow and then run the experiment again 
to truly measure the actual impact of each pre-processor. 

Files to get started with ProcFlow:
* [Main](https://github.com/marvin-hansen/StockUtils/blob/master/Main.py)
* [ProcFlow](https://github.com/marvin-hansen/StockUtils/blob/master/src/procs/ProcFlow.py)
* [Procs](https://github.com/marvin-hansen/StockUtils/blob/master/src/procs/Procs.py)


Transformational procs: 

* Split data in train & test 
* Rename column 
* Delete column 
* Convert date (from object to DateTime) 
* Categorify Date 

Categorify Date requires fast.ai 1.0.5 and transforms DateTime value into corresponding categorial values to capture trends, time-patterns, and cycles. 

Feature generator procs: 

* Add delta-n (difference to previous n values) 
* Add percentage change 
* Add n-previous values (add n-previous values as columns for row-wise processing
* Add Technical Indicators

Supported are several Technical Indicators provided by AlphaVantage (web API) and these are added as seperated columns by merging over the date column. DO NOT DELETE THE DATE COLUMN BEFORE ADDING ANY PROC. If your model does need or cannot handle datetime, remove it at the very last step to ensure all other procs are working correctly.

A complete list of implemented procs is codified in the [corrspodning PROC ENUM](https://github.com/marvin-hansen/StockUtils/blob/master/src/enum/PROCS.py)

## Notes

TechProcs that wrap ta-lib are legacy now and replaced with [Procs](https://github.com/marvin-hansen/StockUtils/blob/master/src/procs/Procs.py) that fetch technical indicators from AlphaVantage. 

However, the TechProcs source code is still there for cases when pulling data and indicators from AlphaVantage isn't an option
or when a very specific indicator or chart patterns is needed. 





