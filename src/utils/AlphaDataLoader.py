from src.enum import INTERVAL
from src.enum import Ticker
from src.enum import TimeFrame
from src.utils.CachedNetLoader import CachedNetLoader
from src.utils.DataLoaderInf import DataLoaderInf


class AlphaDataLoader(DataLoaderInf):
    # Get API Key: https://www.alphavantage.co/support/#api-key

    def __init__(self, api_key, dbg):
        super().__init__(api_key, dbg)
        self.API_KEY = api_key
        self.DBG = dbg

        self.cnl = CachedNetLoader(self.API_KEY, self.DBG)

    # @staticmethod
    def load_local_data(self, path: str, vrb: bool):
        return self.cnl.load_local_data(path, vrb)

    # All stock data are cached
    # @staticmethod
    def load_web_data(self, stock: Ticker.Ticker, time_frame: TimeFrame.TimeFrame, full: bool = False,
                      vrb: bool = False):
        return self.cnl.load_data(stock, time_frame, full, vrb)

    # Intraday data are never cached due to the relatively short expiration time
    # @staticmethod
    def load_intraday_data(self, stock: Ticker.Ticker, interval: INTERVAL.INTERVAL, full: bool = False,
                           vrb: bool = False):
        return self.cnl.load_intraday_data(stock=stock, interval=interval, full=full, vrb=vrb)

    # crypto data are NOT cached. Can be added later based on the cached_stock_loader
    # @staticmethod
    def load_crypto_data(self, crypto_symbol: str, time_frame: TimeFrame.TimeFrame, market: str):
        return self.cnl.load_crypto(crypto_symbol=crypto_symbol, time_frame=time_frame, market=market)

    # Intraday data are never cached due to the relatively short expiration time
    # @staticmethod
    def load_intraday_crypto_data(self, crypto_symbol: str = "BTC", market: str = "USD"):
        """
         Returns the intraday (with 5-minute intervals) time series for a
        digital currency (e.g., BTC) traded on a specific market
        (e.g., CNY/Chinese Yuan), updated realtime. Prices and volumes are
        quoted in both the market-specific currency and USD.
        :param stock:
        :param market:
        :return:
        """
        return self.cnl.load_intraday_crypto(crypto_symbol=crypto_symbol, market=market)
