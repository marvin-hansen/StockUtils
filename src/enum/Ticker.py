from enum import Enum, unique


@unique
class Ticker(Enum):
    SPX = 1
    VIX = 2
    AAPL = 3
    AMZN = 4
    GOOGL = 5
