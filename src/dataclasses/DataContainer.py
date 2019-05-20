from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class DataContainer:
    # Slots classes take up less memory and are typically faster to work with
    # https://realpython.com/python-data-classes/#immutable-data-classes
    __slots__ = ['meta_data', 'split_ratio', 'all_data', 'train_data', 'test_data', 'cat_vars', 'cont_vars']
    #
    meta_data: bool
    split_ratio: float
    #
    all_data: pd.DataFrame
    train_data: pd.DataFrame
    test_data: pd.DataFrame
    cat_vars: List[str]
    cont_vars: List[str]
