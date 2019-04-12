import os
import shutil
from pathlib import Path

import pandas as pd
from alpha_vantage.techindicators import TechIndicators

from src.enum import TECHIND
from src.enum import Ticker
from src.enum import TimeFrame
from src.utils import KeyManager as k
from src.utils.KeyManager import KEYS

DBG = True
cache_folder = "cache"
out_form = 'pandas'
if DBG:
    print("Loading keys from files...")
KEY = k.set_key(KEYS.ALPHA)

ti = TechIndicators(key=KEY, output_format=out_form)


def clear_cache():
    """
    Clears the cache by deleting and recreating the cache folder.
    Note, the clear function doesn't care if there are subdirectories or any other data in the cache folder.
    :return: void
    """
    if os.path.exists(cache_folder) and os.path.isdir(cache_folder):
        shutil.rmtree(cache_folder)

    os.makedirs(cache_folder)


def get_cached_tech_indicator(indicator: TECHIND,
                              stock: Ticker,
                              interval: TimeFrame = TimeFrame.TimeFrame.DAILY,
                              time_period: int = 20,
                              ):
    """
    Cached technical indicator loader. If the requested indicator is in the local cache,
    the cached copy will be returned. If not, it loads the indicator from the web, stores
    a copy in the local cache, and returns a pandas dataframe containing the technical indicator
    for all available recorded dates of the stock.

    Note: The cache must be cleared manually otherwise all objects will remain there forever.
    Only daily close and only reduced 100 day close data are pre-cached to prevent bandwidth pressure.

    :param stock: [ENUM]
    :param indicator [ENUM]: @See TECHIND
    :param stock [ENUM]: Ticker
    :param interval: Daily, Weekly, Monthly. Set to Daily by default
    :param time_period: Nr of time units between two calculating points. Set to 20 by default.
    :return: pandas dataframe containing the technical indicator for all recorded trading days of the stock.

    """

    if not os.path.exists(cache_folder):
        os.makedirs(cache_folder)
    # path to cache-file
    f_name = cache_folder + "/" + stock.name + "-" + indicator.name + "-" + str(time_period) + ".csv"

    path = Path(f_name)
    exists: bool = os.path.isfile(path)

    if exists:
        if DBG:
            print("Load full data from cache")
        return __load_from_local_file(path)

    else:
        if DBG:
            print("Load tech indicator from web")
        df = get_tech_indicator(indicator, stock, interval, time_period)

        if DBG:
            print("Store tech indicators in local cache")
        df.to_csv(path)
        if DBG:
            print("Return tech indicators for stock: " + stock.name)
        return df


def get_tech_indicator(indicator: TECHIND.TECHIND,
                       stock: Ticker,
                       interval: TimeFrame = TimeFrame.TimeFrame.DAILY,
                       time_period: int = 20,
                       ):
    """
    Returns the technical indicator for the given stock ticker on the given interval

    :param indicator [ENUM]: @See TECHIND
    :param stock [ENUM]: Ticker
    :param interval: Daily, Weekly, Monthly. Set to Daily by default
    :param time_period: Nr of time units between two calculating points. Set to 20 by default.
    :return: pandas dataframe containing the technical indicator for all recorded trading days of the stock.
    """

    if indicator is TECHIND.TECHIND.BBANDS:
        if DBG:
            print("Stock: " + stock.name)
            print("Interval: " + interval.name)
            print("time_period: " + str(time_period))

        data, _ = ti.get_bbands(symbol=stock.name, interval=interval.name.lower(), time_period=time_period)

    if indicator is TECHIND.TECHIND.SMA:
        data, _ = ti.get_sma(symbol=stock.name, interval=interval.name.lower(), time_period=time_period)

    if indicator is TECHIND.TECHIND.EMA:
        data, _ = ti.get_ema(symbol=stock.name, interval=interval.name.lower(), time_period=time_period)

    if indicator is TECHIND.TECHIND.WMA:
        data, _ = ti.get_wma(symbol=stock.name, interval=interval.name.lower(), time_period=time_period)

    if indicator is TECHIND.TECHIND.MACD:
        data, _ = ti.get_macd(symbol=stock.name, interval=interval.name.lower())

    if indicator is TECHIND.TECHIND.STOCH:
        data, _ = ti.get_stoch(symbol=stock.name, interval=interval.name.lower())

    if indicator is TECHIND.TECHIND.RSI:
        data, _ = ti.get_rsi(symbol=stock.name, interval=interval.name.lower(), time_period=time_period)

    if indicator is TECHIND.TECHIND.ADX:
        data, _ = ti.get_adx(symbol=stock.name, interval=interval.name.lower(), time_period=time_period)

    if indicator is TECHIND.TECHIND.CCI:
        data, _ = ti.get_cci(symbol=stock.name, interval=interval.name.lower(), time_period=time_period)

    if indicator is TECHIND.TECHIND.AROON:
        data, _ = ti.get_aroon(symbol=stock.name, interval=interval.name.lower(), time_period=time_period)

    if indicator is TECHIND.TECHIND.AD:
        data, _ = ti.get_ad(symbol=stock.name, interval=interval.name.lower())

    if indicator is TECHIND.TECHIND.OBV:
        data, _ = ti.get_obv(symbol=stock.name, interval=interval.name.lower())
    return data.reset_index()


def __load_from_local_file(path):
    """
    private method to load data from local files
    :param path:
    :return: local data
    """
    return pd.read_csv(path, infer_datetime_format=True)
