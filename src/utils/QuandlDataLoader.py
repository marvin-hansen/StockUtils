from src.enum import INTERVAL
from src.enum import Ticker
from src.enum import TimeFrame
from src.utils.DataLoaderInf import DataLoaderInf


class QuandlDataLoader(DataLoaderInf):
    def __init__(self, api_key, dbg):
        super().__init__(api_key, dbg)
        self.API_KEY = api_key
        self.DBG = dbg

    def load_local_data(self, path: str, vrb: bool):
        pass

    def load_web_data(self, stock: Ticker.Ticker, time_frame: TimeFrame.TimeFrame, full: bool = False,
                      vrb: bool = False):
        pass

    def load_intraday_data(self, stock: Ticker.Ticker, interval: INTERVAL.INTERVAL, full: bool = False,
                           vrb: bool = False):
        pass
