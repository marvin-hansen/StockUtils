from abc import ABC, abstractmethod

from src.enum import INTERVAL
from src.enum import Ticker
from src.enum import TimeFrame


class DataLoaderInf(ABC):
    """
    Abstract Base Class (ABC)Interface to specify generic DataLoading functionality. Implementations can implemented
    other interfaces to add more specified functionality or add more unspecified functions.
    """

    def __init__(self, api_key: str, dbg: bool):

        assert isinstance(api_key, str)
        assert isinstance(dbg, bool)
        self.API_KEY: str = api_key
        self.DBG: bool = dbg

    @abstractmethod
    def load_local_data(self, path: str, vrb: bool):
        """
        Loads data from local path.

        :param vrb: verbose - Console printout. False by default.
        :param path: str - Relative or absolute path to file. Example: '/data/TSLA.csv"
        :return: Either pandas data frame or None if no data was found at the given path.
        """
        pass

    @abstractmethod
    def load_web_data(self, stock: Ticker.Ticker, time_frame: TimeFrame.TimeFrame, full: bool, vrb: bool):
        """
        Data loader that returns the last 100 days of data for the given stock on the given time frame

        :param stock: [ENUM] stock ticker
        :param time_frame: [ENUM] DAILY, WEEKLY, MONTHLY
        :param full: [bool] Full dataset from beginning to today. False by default.
        :param vrb: [bool] verbose - Console printout. False by default.
        :return: pandas data frame
        """
        pass

    def load_intraday_data(self, stock: Ticker.Ticker, interval: INTERVAL.INTERVAL, full: bool, vrb: bool):
        """
        Returns intraday tick data for the given stock ticker in the given time interval

        :param stock: [ENUM] ticker
        :param interval: [ENUM] 1min, 5min, 15min, 30min, 60min
        :param full: [bool] Returns only last 100 ticks if False, otherwise full tick data set if True. False by default.
        :param vrb: [bool] verbose - Console printout. False by default.
        :return: pandas data frame
        """
        pass
