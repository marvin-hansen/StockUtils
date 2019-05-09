import os
import pickle
import shutil
from datetime import date
from pathlib import Path
from typing import Any, Union

import pandas as pd
from alpha_vantage.timeseries import TimeSeries

from src.enum import INTERVAL
from src.enum import Ticker
from src.enum import TimeFrame
from src.procs import Procs as p
from src.utils import KeyManager as k
from src.utils.KeyManager import KEYS

"""
Utils to fetch stock data from alpha vantage. 

wrapper: https://github.com/RomelTorres/alpha_vantage
Example: https://github.com/RomelTorres/av_example/blob/master/Alpha%20vantage%20examples.ipynb
Alpha Vantage: https://www.alphavantage.co/
API DOC: https://www.alphavantage.co/documentation/

API Key: https://www.alphavantage.co/support/#api-key
API limit: 5 API requests per minute and 500 requests per day
https://www.alphavantage.co/support/#support
"""

DBG = False
cache_folder = "cache"
exp_file = cache_folder + "/" + "expiration.p"
out_form = 'pandas'

if DBG: print("Loading keys from files...")
a_key = k.set_key(KEYS.ALPHA)
KEY = a_key

ts = TimeSeries(key=KEY, output_format=out_form, indexing_type='date')


def load_data(stock=Ticker.Ticker,
              timeframe: TimeFrame.TimeFrame = TimeFrame.TimeFrame.DAILY,
              full: bool = True):
    """
    Returns OHLCV data for the given stock and timeframe.
    If full is false, then a smaler one year sample will be returned

    :param stock:
    :param timeframe:
    :param full:
    :param vrb:
    :return:
    """

    if DBG: print("Loading Data for stock: " + stock.name)
    df_all, df_meta = cached_stock_loader(stock, timeframe, full=full)
    if DBG:
        print("Done!")
        print("Raw data: ")
        print(df_all.info())

    if DBG: print("Renaming columns: ")
    df_all = p.rename_data(df_all)
    if DBG: print("Done! New columns : ", df_all.info())

    if DBG: print("Converting date to DateTime: ")
    df_all = p.convert_date(df_all, "Date")
    if DBG: print("Done!")

    return df_all, df_meta


def cached_stock_loader(stock: Ticker, period: TimeFrame = TimeFrame.TimeFrame.DAILY, full: bool = False):
    """
    Cached data loader that returns the last 100 days of data by default.
    By default, any data from loaded from the web gets cached locally.
    If a data-requests is cached, then the cached version will be returned.

    Important, cached data have no expiration data so to bypass caching, just clear the cache.

    :param stock: [ENUM] stock ticker
    :param period: [ENUM] DAILY, WEEKLY, MONTHLY
    :param full: Full dataset from IP to today. False by default.
    :return: Tuple: [Data, Meta_Data]
    """
    dbg: bool = DBG
    # Meta-data cannot be stored as CSV and thus gets pickled as plain python objects.
    f_full = cache_folder + "/" + stock.name + "-full.csv"
    f_meta_full = cache_folder + "/" + stock.name + "-full-meta.p"
    f_comp = cache_folder + "/" + stock.name + "-comp.csv"
    f_meta_com = cache_folder + "/" + stock.name + "-comp-meta.p"

    check_cache()

    if full:
        path: Union[Path, Any] = Path(f_full)
        exists: bool = os.path.isfile(path)

        if exists:
            if dbg: print("Load full data from cache")
            return __load_from_local_file(path, f_meta_full)

        else:
            if dbg: print("Load full data from web")
            df, df_meta = get_stock(stock=stock, period=period, full=full)
            if dbg: print("Cache full data to local file")
            df.to_csv(f_full)
            pickle.dump(df_meta, open(f_meta_full, "wb"))

            if dbg: print("Return full data file")
            return __load_from_local_file(path, f_meta_full)

    else:
        if dbg: print("Set path to: " + f_comp)
        path = Path(f_comp)
        exists = os.path.isfile(path)

        if exists:
            if dbg: print("Load compact (last 100 days) from cache")
            return __load_from_local_file(path, f_meta_com)

        else:
            if dbg: print("Load compact data from web")
            df, df_meta = get_stock(stock=stock, period=period, full=False)
            if dbg: print("Cache compact data to file")
            df.to_csv(f_comp)
            if dbg: print("Cache compact meta data to file")
            pickle.dump(df_meta, open(f_meta_com, "wb"))

            if dbg: print("Return compact data file")
            return df, df_meta


def check_cache():
    """
    Ensures a working and warm cache.
    Checks
     * Whether cache exists, and if not creates one
     * Checks cache expiration, and if cache has expired, clears it
     * Checks cache warm-up and if not, conducts a warm-up

    :return: void
    """

    cache_is_cold = False

    # if no cache, create cache
    if not os.path.exists(cache_folder):
        if DBG: print("Create cache folder: ", cache_folder)
        create_cache(cache_folder)
        cache_is_cold = True

    if DBG: print("Load expiration date from cache folder: ")
    expiration_date = pickle.load(open(exp_file, "rb"))
    if DBG: print("Expiration date is : ", expiration_date)
    today = str(date.today())
    if DBG: print("Today is: ", today)

    # if cache has expired, clear it and create a new one
    if DBG: print("Check if expiration is older than today: ")
    if expiration_date < today:
        if DBG: print("Cache has expired: Clear cache")
        clear_cache()
        if DBG: print("Create new cache: ")
        create_cache(cache_folder)
        cache_is_cold = True

    # If cache is there, not expired, and cold cache, warm it up.
    if cache_is_cold:
        if DBG: print("Warming the cache by pre-loading the most commonly used stocks & indices    : ")
        warm_cache(Ticker.Ticker)


def create_cache(cache_folder):
    """
    Creates a cache and sets expiration day to today.
    :param cache_folder:
    :return:
    """
    if not os.path.exists(cache_folder):
        os.makedirs(cache_folder)
        today = str(date.today())
        pickle.dump(today, open(exp_file, "wb"))


def clear_cache():
    """
    Clears the cache by deleting and recreating the cache folder.
    Note, the clear function doesn't care if there are subdirectories or any other data in the cache folder.
    :return: void
    """
    if os.path.exists(cache_folder) and os.path.isdir(cache_folder):
        shutil.rmtree(cache_folder)


def warm_cache(tickers: Ticker):
    """
    Loads all stocks from the ticker ENUM in the persistent file cache. The cached stock loader
    ensures that each dataset will be loaded only once no matter how often the warm function is called.

    Note: The cache must be cleared manually otherwise all objects will remain there forever.
    Only daily close and only reduced 100 day close data are pre-cached to prevent bandwidth pressure.
    :param tickers: [ENUM]
    :return: void
    """
    for stock in tickers:
        if DBG: print("Caching Data for stock: " + stock.name)
        cached_stock_loader(stock, TimeFrame.TimeFrame.DAILY, full=True)


def __load_from_local_file(data_path, meta_path):
    """
    private method to load data and meta-data from two different local files.

    :param data_path:
    :param meta_path:
    :return: Tuple: [Data, Meta_Data]
    """
    df = pd.read_csv(data_path, infer_datetime_format=True)
    df_meta = pickle.load(open(meta_path, "rb"))
    return df, df_meta


def get_stock(stock: Ticker, period: TimeFrame = TimeFrame.TimeFrame.DAILY, full: bool = False):
    """
    Returns stock data and meta data of the ticker for the specified time frame

    :param stock: [ENUM]: Stock ticker
    :param period: [ENUM] DAILY, WEEKLY, MONTHLY
    :param full: Returns only last 100 ticks if False, otherwise full tick data set if True. False by default.
    :return: stock data, meta_data
    """
    if period is TimeFrame.TimeFrame.DAILY:
        if full:
            return ts.get_daily(symbol=stock.name, outputsize='full')
        else:
            return ts.get_daily(symbol=stock.name, outputsize='compact')

    if period is TimeFrame.TimeFrame.WEEKLY:
        if full:
            return ts.get_weekly(symbol=stock.name, outputsize='full')
        else:
            return ts.get_weekly(symbol=stock.name, outputsize='compact')

    if period is TimeFrame.TimeFrame.MONTHLY:
        if full:
            return ts.get_monthly(symbol=stock.name, outputsize='full')
        else:
            return ts.get_monthly(symbol=stock.name, outputsize='compact')


def get_intraday(stock: Ticker, interval: INTERVAL = INTERVAL.INTERVAL.FIVE_MIN, full: bool = False):
    """
    Returns intraday tick data for the given stock in the given time interval

    :param stock: [ENUM] ticker
    :param interval: [ENUM] 1min, 5min, 15min, 30min, 60min
    :param full: Returns only last 100 ticks if False, otherwise full tick data set if True. False by default.
    :return: stock data, meta_data
    """

    if full:
        return ts.get_intraday(symbol=stock.name, interval=interval.value, outputsize='full')
    else:
        return ts.get_intraday(symbol=stock.name, interval=interval.value, outputsize='compact')
