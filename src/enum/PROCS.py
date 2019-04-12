from enum import Enum, unique


@unique
class PROCS(Enum):
    ALL_PROCS = -7
    CAT_DATE = 0
    ADD_PRV_VAL = 1
    ADD_PRCT_CHNGE = 2
    ADD_BBAND = 3
    ADD_SMA = 4
    ADD_EMA = 5
    ADD_WMA = 6
