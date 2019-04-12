from enum import Enum, unique


@unique
class Ticker(Enum):
    NYA = -3
    DJI = -2
    SPX = -1
    VIX = 0
    FB = 1
    AAPL = 2
    AMZN = 3
    NFLX = 4
    GOOGL = 5
    TSLA = 6
    BLK = 7
