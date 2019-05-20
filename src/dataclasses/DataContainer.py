from dataclasses import dataclass
from typing import List

import pandas as pd

__author__ = 'Marvin Hansen'


@dataclass(frozen=True)
class DataContainer:
    """ Immutable data container class."""
    # https://realpython.com/python-data-classes/#immutable-data-classes
    # Slots classes take up less memory and typically lead to faster access time
    __slots__ = ['meta_data', 'split_ratio', 'all_data', 'train_data', 'test_data', 'cat_vars', 'cont_vars']
    #
    meta_data: bool
    split_ratio: float
    #
    all_data: pd.DataFrame
    train_data: pd.DataFrame
    test_data: pd.DataFrame
    # Even though DataContainer is immutable, the list holding cont. & cat. variable names is not because
    # Python does not have an immutable list in the standard lib.
    cat_vars: List[str]
    cont_vars: List[str]

# subclass example:
# class MetaDataContainer(DataContainer):
# inherits all previous fields and adds the following fields below:
#    meta_name: str
#    meta_type: int