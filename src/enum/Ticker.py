from enum import Enum, unique


@unique
class Ticker(Enum):
    # FANG_PLUS
    # https://www.theice.com/fangplus
    SPX = 1
    VIX = 2
    AAPL = 3
    AMZN = 4
    GOOGL = 5
    FB = 6
    NFLX = 7
    BABA = 8
    BIDU = 9
    NVDA = 10
    TWTR = 11
    CMR = 12

