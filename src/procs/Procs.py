import pandas as pd

from src.enum import TECHIND
from src.enum import Ticker
from src.utils import TechInd as t

DBG = False


def proc_close_only(df, cont_vars):
    """
    Proc that removes the Open, High, Low, and Volume column from a standard OHLCV dataset.
    :param df: pandas dataframe
    :param cont_vars: meta-data
    :return: pandas dataframe that contains only the Close price
    """
    features = ["Open", "High", "Low", "Volume"]
    cont_vars.append("Close")
    return df.drop(columns=features)


def proc_add_previous_values(df, column_name, number, cont_vars):
    """ Adds n-previous values and stores each in a seperate column
        According to findings by tsfresh, the previous value can have as much
        as 88.5% significance on predicting the current value.
        https://github.com/blue-yonder/tsfresh/blob/master/notebooks/timeseries_forecasting_google_stock.ipynb
    :param df: pandas data frame
    :param column_name: source column
    :param number: number of time periods to add
    :return: Void - modifies the frame in place
    """
    for n in range(1, (number + 1)):
        df[column_name + str("-") + str(n)] = df[column_name].shift(-n)
        cont_vars.append(column_name + str("-") + str(n))


def proc_add_percent_change(df, column_name, cont_vars):
    """ Calculates the percentage change for each value in the given column
    :param df: pandas data frame
    :param column_name: String - name of the column
    :return: Void - modifies the frame in place
    """
    df[column_name + '-delta'] = df[column_name] - df[column_name].shift(-1)
    df[column_name + "-pct-chng"] = (df[column_name + "-delta"] / df[column_name]) * 100
    cont_vars.append(column_name + '-delta')
    cont_vars.append(column_name + "-pct-chng")


def proc_add_datepart(df, cont_vars, cat_vars, date_col_name: str = "Date"):
    """
    Categorifies date field
    :param df: pandas data frame
    :param cont_vars: continous meta data
    :param cat_vars: categorial meta data
    :return: pandas data frame with date categories
    """
    # requires fast.ai install
    # add_datepart(df, date_col_name, drop=False)
    cont_vars.append("Elapsed")
    column_names = df.columns.values.tolist()
    start = column_names.index("Year")
    end = column_names.index("Is_year_end")
    for i in range(start, end):
        cat_vars.append(column_names[i])


def proc_add_bband(df, stock: Ticker, cont_vars,
                   merge_on: str = "Date",
                   add_diff_to_bb: bool = False,
                   diff_col: str = "Close"):
    """
    Adds Bollinger Band to the dataframe for the given stock & update meta-data accordingly.
    Add the following columns:

     * 'Real Upper Band',
     * 'Real Middle Band',
     * 'Real Lower Band'

    If add_diff_to_bb is set to true, three more columns will be added. Suppose the diff_col is "Close",
    then the additional columns would be:

    * 'Close_BB_UP_Diff',
    * 'Close_BB_MID_Diff',
    * 'Close_BB_LOW_Diff'


    :param df: pandas dataframe
    :param stock: stock ticker
    :param cont_vars: continous mete data
    :param merge_on: shared key over which to join the BB & df table. "Date" by default.
    :param add_diff_to_bb: If true, adds the difference between the diff_column and each of the three bands
    :param diff_col: column to calculate difference to BB
    :return: data-frame that contains all previous data and the three columns of the bollinger band
    """
    bb_data = t.get_cached_tech_indicator(indicator=TECHIND.TECHIND.BBANDS, stock=stock)
    bb_data = __rename_column(bb_data, "Real Upper Band", 'BB_UP')
    bb_data = __rename_column(bb_data, "Real Middle Band", 'BB_MID')
    bb_data = __rename_column(bb_data, "Real Lower Band", 'BB_LOW')
    bb_data = __rename_column(bb_data, "date", 'Date')
    # Date needs to be converted to datetime for the table merge below.
    convert_date(bb_data, "Date")

    print(bb_data.info())

    # update meta-data
    cont_vars = __update_meta_data(cont_vars, bb_data.columns.values.tolist())

    if DBG:
        print("Merging data with BB")
        # inner join merge over Date
        merged = pd.merge(df, bb_data, on="Date")
        print("Merged")
        print()
        print("Date len: " + str(len(df)))
        print("BB len: " + str(len(bb_data)))
        print("Merged len: " + str(len(merged)))
        print(merged.info())
        print(merged.head(3))
        print()
        print(merged.tail(3))

    if (add_diff_to_bb):
        # Merge
        df_merge = pd.merge(df, bb_data, on=merge_on)
        # Calculate distance between specified price column each of the three BB bands.
        df_merge['Close_BB_UP_Diff'] = df_merge[diff_col] - df_merge['BB_UP']
        cont_vars.append('Close_BB_UP_Diff')
        df_merge['Close_BB_MID_Diff'] = df_merge[diff_col] - df_merge['BB_MID']
        cont_vars.append('Close_BB_MID_Diff')
        df_merge['Close_BB_LOW_Diff'] = df_merge[diff_col] - df_merge['BB_LOW']
        cont_vars.append('Close_BB_LOW_Diff')
        return df_merge

    else:
        return pd.merge(df, bb_data, on=merge_on)


def proc_add_wma20_wma_60_diff(df, cont_vars, stock: Ticker):
    """

    :param df:
    :param cont_vars:
    :param stock:
    :return:
    """

    wma20: str = "WMA_20"
    wma60: str = "WMA_60"
    res_name: str = "WMA_20_EMA_60_Diff"
    columns = df.columns.values.tolist()

    if wma20 not in columns:
        df = proc_add_wma20(df=df, cont_vars=cont_vars, stock=stock, add_diff=True)

    if wma60 not in columns:
        df = proc_add_wma60(df=df, cont_vars=cont_vars, stock=stock, add_diff=True)

    # calculate difference between WMA 20 and 60
    df[res_name] = df[wma20] - df[wma60]
    # update meta data
    cont_vars.append(res_name)

    return df


def proc_add_wma60(df, cont_vars, stock: Ticker, add_diff: bool = False, diff_col: str = "Close"):
    """
    Returns dataframe with the 60 day weighted moving average

    :param df: pandas data frame
    :param cont_vars: mete data
    :param stock: stock
    :param add_diff:
    :param diff_col:
    :return:
    """
    return proc_add_mov_avg(df=df, cont_vars=cont_vars, stock=stock,
                            mov_avg='wma', time_period=60, add_diff=add_diff, diff_col=diff_col)


def proc_add_wma20(df, cont_vars, stock: Ticker, add_diff: bool = False, diff_col: str = "Close"):
    """
    Returns dataframe with the 20 day weighted moving average

    :param df: pandas data frame
    :param cont_vars: mete data
    :param stock: stock
    :param add_diff:
    :param diff_col:
    :return:
    """
    return proc_add_mov_avg(df=df, cont_vars=cont_vars, stock=stock,
                            mov_avg='wma', time_period=20, add_diff=add_diff, diff_col=diff_col)


def proc_add_ema10_ema_30_diff(df, cont_vars, stock: Ticker, add_ohlc_diff: bool = False):
    """

    :param df:
    :param cont_vars:
    :param stock:
    :return:
    """
    ema10: str = "EMA_10"
    ema30: str = "EMA_30"
    res_name: str = "EMA_10_EMA_30_Diff"
    columns = df.columns.values.tolist()

    if ema10 not in columns:
        df = proc_add_ema10(df=df, cont_vars=cont_vars, stock=stock, add_ohlc_diff=add_ohlc_diff)

    if ema30 not in columns:
        df = proc_add_ema30(df=df, cont_vars=cont_vars, stock=stock, add_ohlc_diff=add_ohlc_diff)

    # calculate difference between EMA  10 and 30
    df[res_name] = df[ema10] - df[ema30]
    # update meta data
    cont_vars.append(res_name)

    return df


def proc_add_ema30(df, cont_vars, stock: Ticker, add_diff: bool = False, diff_col: str = "Close"):
    """
    Returns dataframe with the 30 day expontial moving average

    :param df: pandas data frame
    :param cont_vars: mete data
    :param stock: stock
    :param add_diff:
    :param diff_col:
    :return:
    """
    return proc_add_mov_avg(df=df, cont_vars=cont_vars, stock=stock,
                            mov_avg='ema', time_period=30, add_diff=add_diff, diff_col=diff_col)


def proc_add_ema10(df, cont_vars, stock: Ticker, add_diff: bool = False, diff_col: str = "Close"):
    """
    Returns dataframe with the 10 day expontial moving average

    :param df: pandas data frame
    :param cont_vars: mete data
    :param stock: stock
    :param add_diff:
    :param diff_col:
    :return:
    """
    return proc_add_mov_avg(df=df, cont_vars=cont_vars, stock=stock,
                            mov_avg='ema', time_period=10, add_diff=add_diff, diff_col=diff_col)


def proc_add_sma20_sma_200_diff(df, cont_vars, stock: Ticker, add_ohlc_diff: bool = False):
    """
    :param add_ohlc_diff:
    :param df:
    :param cont_vars:
    :param stock:
    :return:
    """
    sma20: str = "SMA_20"
    sma200: str = "SMA_200"
    res_name: str = "SMA_200_SMA_20_Diff"
    columns = df.columns.values.tolist()

    if sma20 not in columns:
        df = proc_add_sma20(df=df, cont_vars=cont_vars, stock=stock, add_diff=False, add_ohlc_diff=add_ohlc_diff)

    if sma200 not in columns:
        df = proc_add_sma200(df=df, cont_vars=cont_vars, stock=stock, add_diff=False, add_ohlc_diff=add_ohlc_diff)

    # calculate difference between SMA 20 and 200
    df[res_name] = df[sma20] - df[sma200]
    # update meta data
    cont_vars.append(res_name)

    return df


def proc_add_sma20(df, cont_vars, stock: Ticker, add_diff: bool = False, diff_col: str = "Close",
                   add_ohlc_diff: bool = False):
    """
    Returns dataframe with the 20 day simple moving average

    :param df: pandas data frame
    :param cont_vars: mete data
    :param stock: stock
    :param add_diff:
    :param diff_col:
    :return:
    """
    return proc_add_mov_avg(df=df, cont_vars=cont_vars, stock=stock, mov_avg='sma', time_period=20,
                            add_diff=add_diff, diff_col=diff_col, add_ohlc_diff=add_ohlc_diff)


def proc_add_sma200(df, cont_vars, stock: Ticker, add_diff: bool = False, diff_col: str = "Close",
                    add_ohlc_diff: bool = False):
    """

    Returns dataframe with the 200 day simple moving average

    :param df:
    :param cont_vars:
    :param stock:
    :param add_diff:
    :param diff_col:
    :return:
    """
    return proc_add_mov_avg(df=df, cont_vars=cont_vars, stock=stock, mov_avg='sma', time_period=200,
                            add_diff=add_diff, diff_col=diff_col, add_ohlc_diff=add_ohlc_diff)


def proc_add_mov_avg(df, cont_vars,
                     stock: Ticker,
                     mov_avg,
                     time_period: int = 20,
                     merge_on: str = "Date",
                     add_diff: bool = False,
                     diff_col: str = "Close",
                     add_ohlc_diff: bool = False):
    """
    :param df: pandas dataframe
    :param cont_vars: mete data
    :param stock: stock ticker
    :param mov_avg: moving average. Possible values: ema, sma, wma. Set to sma by default
    :param time_period: Time period for the moving average. By default 20. (i.e. 20 day SMA)
    :param merge_on: Index to merge data. Set to "Date" by default
    :param add_diff: Add a difference column that contains the difference between the specified column and the moving average. Set to False by default.
    :param diff_col: Specifies the column for calculating the difference. Set to "Close" by default
    :param add_ohlc_diff: Calculates the difference between the mov. avarage and each of the four OHLC prices.
    :return: pandas dataframe  with moving average column and diff column add_diff is set to true.
    """

    # moving average
    ma_data = __load_moving_avg(stock=stock, mov_avg=mov_avg, time_period=time_period)

    columns = ma_data.columns.values.tolist()
    # Rename to enable the inner join over "Date", which would fail w/o the rename
    ma_data = __rename_column(ma_data, "date", 'Date')
    columns = df.columns.values.tolist()

    # construct new column name with time period in it
    col_name = mov_avg.upper() + "_" + str(time_period)
    # Rename MA column
    ma_data = __rename_column(ma_data, mov_avg.upper(), col_name)
    # update meta-data
    cont_vars = __update_meta_data(cont_vars, ma_data.columns.values.tolist())

    if (add_diff):
        # Merge
        df_merge = pd.merge(df, ma_data, on=merge_on)
        # Calculate distance between specified price column and the moving average
        df_merge[diff_col + "_" + col_name + "_Diff"] = df_merge[diff_col] - df_merge[col_name]
        # update meta data
        cont_vars.append(diff_col + "_" + col_name + "_Diff")

        return df_merge

    elif (add_ohlc_diff):
        # Merge
        df_merge = pd.merge(df, ma_data, on=merge_on)
        ohcl = ["Open", "High", "Low", "Close"]
        col_name = mov_avg.upper() + "_" + str(time_period)

        for c_name in ohcl:
            # Calculate distance between specified price column and the moving average
            df_merge[c_name + "_" + col_name + "_Diff"] = df_merge[c_name] - df_merge[col_name]
            # update meta data
            cont_vars.append(c_name + "_" + col_name + "_Diff")

        return df_merge

    else:
        return pd.merge(df, ma_data, on=merge_on)


def split_data(df, split_ratio: float = 0.90, nr_valid: int = 5, vrb: bool = False):
    """
    Util to split a pandas dataframe in train, test, and validation data.

    :param df: pandas data frame
    :param split_ratio: ratio between train & test
    :param nr_valid: number of validation data to exclude from train & test. Set to 5 by default.
    :param vrb: Verbose. False by default
    :return: train_df, test_df, valid_df
    """
    assert (split_ratio <= 1.00)
    assert (len(df) > nr_valid)

    # extract validation data
    valid_df = df.tail(nr_valid)

    # remove validation data before splitting in train & test
    X = df.iloc[:-nr_valid]

    train_size = int(len(X) * split_ratio)
    train_df, test_df = X[0:train_size], X[train_size:len(X)]
    if vrb or DBG:
        total_len = len(train_df) + len(test_df) + len(valid_df)
        print('Observations: %d' % (len(df)))
        print("Train + Test + Valid: " + str(total_len))
        print('Training data: %d' % (len(train_df)))
        print('Testing data: %d' % (len(test_df)))
        print('Validating data: %d' % (len(valid_df)))

    return train_df, test_df, valid_df


def inspect_data(data, cont_vars, cat_vars):
    """
    Util to inspect the pandas data frame and meta data array
    :param data: data frame
    :param cont_vars: meta data array
    :param cat_vars: meta data array
    :return: void
    """
    print()
    print("!!INSPECT DATA FRAME!!")
    print()
    print(data.info())
    print()
    print("Cont. meta-data: " + str(cont_vars))
    print("Cat. meta-data: " + str(cat_vars))
    print()
    print(data.head(3))
    print()
    print(data.tail(3))


def rename_data(data):
    """
    :param data:
    :return:
    """
    data = __rename_column(data, "date", 'Date')
    data = __rename_column(data, "1. open", 'Open')
    data = __rename_column(data, "2. high", 'High')
    data = __rename_column(data, "3. low", 'Low')
    data = __rename_column(data, "4. close", 'Close')
    data = __rename_column(data, "5. volume", 'Volume')
    return data


def convert_date(df, date_col_name: str = None):
    """
    Converts the given date column from the standard object to an instance of datetime. 
    :param df: pandas data frame 
    :param date_col_name:
    :return: 
    """
    # Passing infer_datetime_format=True can often-times speedup a parsing
    # if its not an ISO8601 format exactly, but in a regular format.
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html
    # data = pd.to_datetime(data[col_name],  infer_datetime_format=True)
    df[date_col_name] = pd.to_datetime(df[date_col_name], infer_datetime_format=True)

    return df


def __load_moving_avg(stock: Ticker, mov_avg: str = 'sma', time_period: int = 20):
    """
    Helper function to load similar moving averages for the given stock
    :param stock: stock ticker
    :param mov_avg: ID of moving average possible values. set to SMA by default.
    :return: pandas data frame with the moving averge for the stock
    """
    if (mov_avg == 'sma'):
        ind = TECHIND.TECHIND.SMA
    elif (mov_avg == 'ema'):
        ind = TECHIND.TECHIND.EMA
    elif (mov_avg == 'wma'):
        ind = TECHIND.TECHIND.WMA
    else:
        ind = TECHIND.TECHIND.SMA

    ma_data = t.get_cached_tech_indicator(indicator=ind, stock=stock, time_period=time_period)
    date_col_name: str = "date"
    ma_data[date_col_name] = pd.to_datetime(ma_data[date_col_name], infer_datetime_format=True)

    return ma_data


def __rename_column(df, old_name, new_name):
    """
    Renames a column  in a pandas dataframe
    :param df: pandas dataframe
    :param old_name:
    :param new_name:
    :return: data frame with renamed column
    """
    return df.rename(index=str, columns={old_name: new_name})


def __update_meta_data(var, column_names):
    if "Date" in column_names:
        column_names.remove("Date")
    else:
        for i in range(len(column_names)):
            var.append(column_names[i])

    return var
