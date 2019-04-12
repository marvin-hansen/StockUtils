from enum import Enum, unique

@unique
class PROCS(Enum):
    ALL_PROCS = -7
    CAT_DATE = 0
    PRV_VAL = 1
    PRCT_CHNGE = 2
    BBAND = 3
    SMA = 4
    EMA = 5
    WMA = 6
    OHLC_AVG = 7
    MOM = 8
    OBV = 9
    ADX = 10
    MACD = 11
    RSI = 12
