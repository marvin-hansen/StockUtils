import os
import pickle
import shutil
from datetime import date
from pathlib import Path
from typing import Any, Union

import pandas as pd
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.timeseries import TimeSeries

from src.enum import INTERVAL
from src.enum import Ticker
from src.enum import TimeFrame
from src.procs import Procs as p


class CachedNetLoader:
    def __init__(self, api_key: str, dbg: bool = False):
        # set key
        self.API_KEY = api_key
        self.cc = CryptoCurrencies(key=self.API_KEY, output_format='pandas')
        self.ts = TimeSeries(key=self.API_KEY, output_format='pandas')
        self.DBG = dbg
        self.cache_folder = "cache"
        self.exp_file = self.cache_folder + "/" + "expiration.p"
        self.out_form = 'pandas'

    def load_local_data(path: str, vrb: bool = False):

        DBG = vrb
        exists: bool = os.path.isfile(path)

        if exists:
            if DBG: print("Load full data from path: ", path)
            return pd.read_csv(path)

        else:
            if DBG: print("ERROR: NO DATA FOUND AT PATH: ", path)
            return None

    def load_data(self, stock=Ticker.Ticker,
                  timeframe: TimeFrame.TimeFrame = TimeFrame.TimeFrame.DAILY,
                  full: bool = True, vrb: bool = False):
        """
        Returns OHLCV data for the given stock and timeframe.
        If full is false, then a smaller one year sample will be returned

        :param stock:
        :param timeframe:
        :param full:
        :param vrb:
        :return:
        """
        DBG = vrb
        if DBG: print("Loading Data for stock: " + stock.name)
        df_all, df_meta = self.cached_stock_loader(stock, timeframe, full=full)
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

        return df_all

    def load_intraday_data(self, stock: Ticker.Ticker, interval: INTERVAL.INTERVAL, full: bool, vrb: bool):
        DBG = vrb
        if DBG: print("Loading Intraday Data for stock: " + stock.name)
        df_all, _ = self.get_intraday(stock, interval, full)
        if DBG:
            print("Done!")
            print("Raw data: ")
            print(df_all.info())

        if DBG: print("Renaming columns: ")
        df_all = p.rename_data(df_all)
        if DBG: print("Done! New columns : ", df_all.info())

        return df_all

    def load_crypto(self, crypto_symbol: str, time_frame: TimeFrame.TimeFrame, market: str):
        return self.get_crypto(crypto_symbol=crypto_symbol, time_frame=time_frame, market=market)

    def get_crypto(self, crypto_symbol, time_frame: TimeFrame.TimeFrame, market: str):

        if time_frame is TimeFrame.TimeFrame.DAILY:
            data, _ = self.cc.get_digital_currency_daily(symbol=crypto_symbol, market=market)
            return data
        if time_frame is TimeFrame.TimeFrame.WEEKLY:
            data, _ = self.cc.get_digital_currency_weekly(symbol=crypto_symbol, market=market)
            return data

        if time_frame is TimeFrame.TimeFrame.MONTHLY:
            data, _ = self.cc.get_digital_currency_monthly(symbol=crypto_symbol, market=market)
            return data

    def load_intraday_crypto(self, crypto_symbol: str, market: str):
        data, _ = self.cc.get_digital_currency_intraday(symbol=crypto_symbol, market=market)
        return data

    def cached_stock_loader(self, stock: Ticker, period: TimeFrame = TimeFrame.TimeFrame.DAILY, full: bool = False):
        """
        Cached data loader that returns the last 100 days of data by default.
        By default, any data are loaded from the web gets cached locally.
        If a data-requests is cached, then the cached version will be returned.

        Important, cached data have no expiration data so to bypass caching, just clear the cache.

        :param stock: [ENUM] stock ticker
        :param period: [ENUM] DAILY, WEEKLY, MONTHLY
        :param full: Full dataset from IP to today. False by default.
        :return: Tuple: [Data, Meta_Data]
        """
        dbg: bool = self.DBG
        # Meta-data cannot be stored as CSV and thus gets pickled as plain python objects.
        f_full = self.cache_folder + "/" + stock.name + "-full.csv"
        f_meta_full = self.cache_folder + "/" + stock.name + "-full-meta.p"
        f_comp = self.cache_folder + "/" + stock.name + "-comp.csv"
        f_meta_com = self.cache_folder + "/" + stock.name + "-comp-meta.p"

        self.check_cache(stock=stock)

        if full:
            path: Union[Path, Any] = Path(f_full)
            exists: bool = os.path.isfile(path)

            if exists:
                if dbg: print("Load full data from cache")
                return self.__load_from_local_file(data_path=path, meta_path=f_meta_full)

            else:
                if dbg: print("Load full data from web")
                df, df_meta = self.get_stock(stock=stock, period=period, full=full)
                if dbg: print("Cache full data to local file")
                df.to_csv(f_full)
                pickle.dump(df_meta, open(f_meta_full, "wb"))

                if dbg: print("Return full data file")
                return self.__load_from_local_file(data_path=path, meta_path=f_meta_full)

        else:
            if dbg: print("Set path to: " + f_comp)
            path = Path(f_comp)
            exists = os.path.isfile(path)

            if exists:
                if dbg: print("Load compact (last 100 days) from cache")
                return self.__load_from_local_file(data_path=path, meta_path=f_meta_full)

            else:
                if dbg: print("Load compact data from web")
                df, df_meta = self.get_stock(stock=stock, period=period, full=False)
                if dbg: print("Cache compact data to file")
                df.to_csv(f_comp)
                if dbg: print("Cache compact meta data to file")
                pickle.dump(df_meta, open(f_meta_com, "wb"))

                if dbg: print("Return compact data file")
                return df, df_meta

    def check_cache(self, stock: Ticker):
        """
        Ensures a working and warm cache.
        Checks
         * Whether cache exists, and if not creates one
         * Checks cache expiration, and if cache has expired, clears it
         * Checks cache warm-up and if not, conducts a warm-up

        :return: void
        """

        cache_is_cold = False
        DBG = self.DBG
        cache_folder = self.cache_folder

        # if no cache, create cache
        if not os.path.exists(cache_folder):
            if DBG: print("Create cache folder: ", cache_folder)
            self.create_cache(cache_folder)
            cache_is_cold = True

        if DBG: print("Load expiration date from cache folder: ")
        expiration_date = pickle.load(open(self.exp_file, "rb"))
        if DBG: print("Expiration date is : ", expiration_date)
        today = str(date.today())
        if DBG: print("Today is: ", today)

        # if cache has expired, clear it and create a new one
        if DBG: print("Check if expiration is older than today: ")
        if expiration_date < today:
            if DBG: print("Cache has expired: Clear cache")
            self.clear_cache()
            if DBG: print("Create new cache: ")
            self.create_cache(cache_folder)
            cache_is_cold = True

        # If cache is there, not expired, and cold cache, warm it up.
        if cache_is_cold:
            if DBG: print("Warming the cache by pre-loading the most commonly used stocks & indices    : ")
            self.warm_cache(stock=stock)

    def create_cache(self, cache_folder: str):
        """
        Creates a cache and sets expiration day to today.
        :param cache_folder:
        :return:
        """
        if not os.path.exists(cache_folder):
            os.makedirs(cache_folder)
            today = str(date.today())
            pickle.dump(today, open(self.exp_file, "wb"))

    def clear_cache(self):
        """
        Clears the cache by deleting and recreating the cache folder.
        Note, the clear function doesn't care if there are subdirectories or any other data in the cache folder.
        :return: void
        """
        if os.path.exists(self.cache_folder) and os.path.isdir(self.cache_folder):
            shutil.rmtree(self.cache_folder)

    def get_stock(self, stock: Ticker, period: TimeFrame = TimeFrame.TimeFrame.DAILY, full: bool = False):
        """
        Returns stock data and meta data of the ticker for the specified time frame

        :param stock: [ENUM]: Stock ticker
        :param period: [ENUM] DAILY, WEEKLY, MONTHLY
        :param full: Returns only last 100 ticks if False, otherwise full tick data set if True. False by default.
        :return: stock data, meta_data
        """
        if full:
            output_size = 'full'
        else:
            output_size = 'compact'

        if period is TimeFrame.TimeFrame.DAILY:
            return self.ts.get_daily(symbol=stock.name, outputsize=output_size)

        if period is TimeFrame.TimeFrame.WEEKLY:
            return self.ts.get_weekly(symbol=stock.name, outputsize=output_size)

        if period is TimeFrame.TimeFrame.MONTHLY:
            return self.ts.get_monthly(symbol=stock.name, outputsize=output_size)


    def warm_cache(self, stock: Ticker):
        """
        Loads all stocks from the ticker ENUM in the persistent file cache. The cached stock loader
        ensures that each dataset will be loaded only once no matter how often the warm function is called.

        Loads both, the 100 day and the full data-set in the cache.

        :param stock: stock to load
        :return: void
        """
        self.cached_stock_loader(stock, TimeFrame.TimeFrame.DAILY, full=False)
        self.cached_stock_loader(stock, TimeFrame.TimeFrame.DAILY, full=True)

    def get_intraday(self, stock: Ticker, interval: INTERVAL = INTERVAL.INTERVAL.FIVE_MIN, full: bool = False):
        """
        Returns intraday tick data for the given stock ticker in the given time interval

        :param stock: [ENUM] ticker
        :param interval: [ENUM] 1min, 5min, 15min, 30min, 60min
        :param full: Returns only last 100 ticks if False, otherwise full tick data set if True. False by default.
        :return: stock data, meta_data
        """

        if full:
            return self.ts.get_intraday(symbol=stock.name, interval=interval.value, outputsize='full')
        else:
            return self.ts.get_intraday(symbol=stock.name, interval=interval.value, outputsize='compact')

    def __load_from_local_file(self, data_path, meta_path):
        """
        private method to load data and meta-data from two different local files.

        :param data_path:
        :param meta_path:
        :return: Tuple: [Data, Meta_Data]
        """
        df = pd.read_csv(data_path, infer_datetime_format=True)
        df_meta = pickle.load(open(meta_path, "rb"))
        return df, df_meta
