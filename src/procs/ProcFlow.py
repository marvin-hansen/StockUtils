from src.procs import Procs as p

"""
Pre-processor-worklows (ProcFlows) simplify data pre-processing as each apply a well 
specified formula of how to prepare the data. 

Usage example: 

     # Create a ProcFlow
     pf = ProcFlow(DBG)
     # Call the selected ProcFlow with ID=3 
     data = pf.proc_switch(data=df_all, stock=stock, y_col="Close", nr_n=5, proc_id=3)
     # Parameters:
     # data - data from the default data-loader. By convention, the DataLoader does column renaming
     # stock - Stock ticker. Required to pull technical indactors that match the data for the ticker
     # y_col - The "prediction" field, or the main attrbiute. Often the "Close" price, but really can be anything
     # nr_n - A parameter to certain procs. For example, next_N takes y and n as a parameter and adds the next n instances of y
     # proc_id= the id of pre-defined ProcFlows. Currently, only 1 - 3 procs are there, but custom procs can be added
            

That allows a couple of handy things:  

1) Rapid experimentation 
2) Comparision of different ProcFlows
3) Comparision between different data with the same ProcFlows

Example, say one want to figure our whether Bollinger Bands, MACD and RSI have any impact on the algorithm 
under investigation. To do so, just copy the base_proc and add the MACD and RSI procs, as shown
in proc_01.   

It is good practice to stuff every new idea in a seperate ProcFlow and then run the experiment again 
to truly measure the actual impact of each pre-processor. For instance, procs01 - proc03 have explored different ideas, but
ultimately proc_03 improved the model accurcay in the most in a series of experiments. 
The dozen or so intermediate steps have been removed for brevity reasons. However, the main take aways from
the experiments are

1) Fully Connected Network with AutoEncoders outperforms LSTM / RNN 

2) Only few technical indicators improved model accurcay:
* WMA 20
* WMA 60 
* SMA 20
* SMA 200 
* Bollinger Bands
* Momentum & Change in momentum 

3) Those few indicators above that actually work, all perform better when 
distance to Close price is added given the model trains on the close price.
In some cases, adding percentage change and or absolute percentage change relative
to previous values improves the model.

4) Most commonly used indicatorshave performed poorly and actually deteriorated 
model accuracy. Among these were:
* MACD 
* RSI 
* ADX 
* EMA 10 
* EMA 30 
* OBV 
* ALL chart_patterns
* Most "exotic" moving averages (double, triple etc.) except WMA 
* All volume studies. 

These results remain inconclusive because just one single specialised model has been tested for
many different procs, but results may vary when another model is used. 


5) The surprise model improvements:

* categorify date to capture trends, patterns, and ciclical patterns 
* Distance between OHLC / Close price to just any moving average 
* Change in momentum

In retrospect, all of the three make perfect sense as each one encodes a certain
aspect of domain knowledge in the data. For instace, the quartly drop in equity prices due to rotation
at the mega-funds is captured when the date is categorified. 

The distance between  20 or 200 SMA, widely used (among other things) by portfolio managers 
to buy or sell larger positions is captured whenever those distance values are added to the data.

Finally, many trading algorithms tend to follow momentum to buy or sell before the actual price flips, and
again the change in momentum captures this.  
 
 
Proc_03 contains all of the best perform procs  


Open ares of exploration:

1) Net impact of sentiment analysis on model accuracy 
2) Net impact of best procs on trend prediction 
3) Net impact of best procs on RL trading agent  
 
 
 For contacts, 
 email at marvin.hansen@gmail.con
 Github: https://github.com/marvin-hansen/ 
 
"""


class ProcFlow():
    def __init__(self, dbg):
        self.DBG = dbg

    def proc_switch(self, data, stock, y_col="", nr_n=5, proc_id=1):

        if proc_id == 1:
            return self.proc_01(data, stock, y_col, nr_n=nr_n)

        if proc_id == 2:
            return self.proc_02(data, stock, y_col, nr_n=nr_n)

        if proc_id == 3:
            return self.proc_03(data, stock, y_col, nr_n=nr_n)

        # if proc_id == 4:
        #    return self.proc_04(data, stock, y_col, nr_n=nr_n)

        else:
            print("No matching proc ID found")

    @staticmethod
    def base_proc_00(data, stock, y_col, nr_n: int):
        """
        Base proc that is meant to be used as template.

        :param data: Pandas dataframe containing data from the DataLoder
        :param stock: [Ticker] the stock to which the data belong. This is import since
                      most technical indicators are fetched by the ticker symbol.
        :param y_col: the column to predict, for a regression problem.
                      Otherwise, this is the one you want to pass as input to other procs
        :param nr_n: the number of n, serves as an input to other procs such as previous-n.
        :return: pre-processed data in a pandas dataframe
        """
        # Meta-data tracking [Optional]
        # seperate  columns into continous and category data columns
        # This tracks the meta-data across all procs. Some ETL frameworks
        # require these meta data. However,
        cont_vars = []  # clear everything, just in case
        cat_vars = []
        cont_vars = ["Open", "High", "Low", "Close", "Volume"]

        # Date conversion & column renaming [Optional]
        # Usually, renaming & date conversion is done in the DataLoader.
        # HOwever, in case that didn't happaned for any reason or any proc needs a different
        # naming convention, use rename_column function to adjust accordingly
        # data = p.__rename_column(data, "date", 'Date')
        # data = p.convert_date(data, "Date")

        # run procs
        # add previous n values of y-column
        p.proc_add_previous_values(df=data, column_name=y_col, number=nr_n, cont_vars=cont_vars)
        # percennt change of y-column
        p.proc_add_percent_change(df=data, column_name=y_col, cont_vars=cont_vars)
        # Your procs ...

        # Replace NaN
        # Many neuronal net and other models crash when they encounter NaN values.
        # Thus, the proc below replaces any possible NaN value with zero.
        data = p.proc_fill_nan

        return data

    @staticmethod
    def proc_01(data, stock, y_col, nr_n: int):
        # seperate  columns into continous data columns and category data columns
        cont_vars = []  # clear everything, just in case
        cat_vars = []
        cont_vars = ["Open", "High", "Low", "Close", "Volume"]

        # run procs
        # add previous n values of y-column
        p.proc_add_previous_values(df=data, column_name=y_col, number=nr_n, cont_vars=cont_vars)
        # percennt change of y-column
        p.proc_add_percent_change(df=data, column_name=y_col, cont_vars=cont_vars)

        # Example Bollinger Band
        # data = p.proc_add_bband(df=data, stock=stock, cont_vars=cont_vars, add_diff_to_bb=True)
        data = p.proc_add_bband(df=data, stock=stock, cont_vars=cont_vars, add_diff_to_bb=False, add_ohlc_diff=True)

        # Example: RSI
        data = p.proc_add_rsi(df=data, cont_vars=cont_vars, stock=stock, change=True)
        # Example: MACD
        data = p.proc_add_macd(df=data, cont_vars=cont_vars, stock=stock)

        # Remove NaN
        data = p.proc_fill_nan

        return data


    @staticmethod
    def proc_02(data, stock, y_col, nr_n: int):
        # seperate  columns into continous data columns and category data columns
        cont_vars = []  # clear everything, just in case
        cat_vars = []
        cont_vars = ["Open", "High", "Low", "Close", "Volume"]

        # run procs
        # add previous n values of y-column
        p.proc_add_previous_values(df=data, column_name=y_col, number=nr_n, cont_vars=cont_vars)

        # categorify date
        p.proc_add_datepart(df=data, cont_vars=cont_vars, cat_vars=cat_vars)

        # percennt change
        p.proc_add_percent_change(df=data, column_name="Open", cont_vars=cont_vars)
        p.proc_add_percent_change(df=data, column_name="High", cont_vars=cont_vars)
        p.proc_add_percent_change(df=data, column_name="Low", cont_vars=cont_vars)
        p.proc_add_percent_change(df=data, column_name="Close", cont_vars=cont_vars)
        #
        p.proc_add_abs_percent_change(df=data, column_name="Close", cont_vars=cont_vars)

        # add Bollinger Band
        data = p.proc_add_bband(df=data, stock=stock, cont_vars=cont_vars, add_diff_to_bb=False, add_ohlc_diff=True)
        # Add SMA
        data = p.proc_add_sma20(df=data, cont_vars=cont_vars, stock=stock, add_diff=True)
        data = p.proc_add_sma200(df=data, cont_vars=cont_vars, stock=stock, add_diff=True)
        data = p.proc_add_sma20_sma_200_diff(df=data, cont_vars=cont_vars, stock=stock)
        data = p.proc_add_wma20_wma_60_diff(df=data, cont_vars=cont_vars, stock=stock, add_ohlc_diff=True)
        # Remove NaN
        data = p.proc_fill_nan

        return data

    @staticmethod
    def proc_03(data, stock, y_col="", nr_n=1):
        # seperate  columns into continous and category data columns
        cont_vars = []  # clear everything, just in case
        cat_vars = []
        cont_vars = ["Open", "High", "Low", "Close", "Volume"]

        # categorify date
        p.proc_add_datepart(df=data, cont_vars=cont_vars, cat_vars=cat_vars)

        # Add percent change for each of the OHLC
        p.proc_add_percent_change(df=data, column_name="Open", cont_vars=cont_vars)
        p.proc_add_percent_change(df=data, column_name="High", cont_vars=cont_vars)
        p.proc_add_percent_change(df=data, column_name="Low", cont_vars=cont_vars)
        p.proc_add_percent_change(df=data, column_name="Close", cont_vars=cont_vars)
        # Add absolute percentage change
        p.proc_add_abs_percent_change(df=data, column_name="Close", cont_vars=cont_vars)
        # add momentum
        data = p.proc_add_mom(df=data, cont_vars=cont_vars, stock=stock)
        # add momentum percentage change
        data = p.proc_add_percent_change(df=data, column_name="MOM", cont_vars=cont_vars)

        # ad y
        p.proc_add_next_y(df=data, y_column=y_col, number=nr_n, cont_vars=cont_vars)
        # run procs
        # add previous 5
        p.proc_add_previous_values(df=data, column_name="Close", number=5, cont_vars=cont_vars)

        # add Bollinger Band
        data = p.proc_add_bband(df=data, stock=stock, cont_vars=cont_vars, add_diff_to_bb=True)
        # Add SMA
        data = p.proc_add_sma20(df=data, cont_vars=cont_vars, stock=stock, add_diff=True)
        data = p.proc_add_sma200(df=data, cont_vars=cont_vars, stock=stock, add_diff=True)
        data = p.proc_add_sma20_sma_200_diff(df=data, cont_vars=cont_vars, stock=stock)
        # SMA percentage change
        data = p.proc_add_percent_change(df=data, column_name="SMA_20", cont_vars=cont_vars)
        data = p.proc_add_percent_change(df=data, column_name="SMA_200", cont_vars=cont_vars)

        # Add WMA with ohlc_diff=True
        data = p.proc_add_wma20_wma_60_diff(df=data, cont_vars=cont_vars, stock=stock, add_ohlc_diff=True)
        # WMA percentage change
        data = p.proc_add_percent_change(df=data, column_name="WMA_20", cont_vars=cont_vars)
        data = p.proc_add_percent_change(df=data, column_name="WMA_60", cont_vars=cont_vars)
        # Remove NaN
        data = p.proc_fill_nan

        return data
