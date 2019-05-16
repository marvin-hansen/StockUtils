from src.enum import Ticker
from src.enum import TimeFrame
from src.procs.ProcFlow import ProcFlow
from src.utils import KeyManager as k
from src.utils.CachedNetLoader import CachedNetLoader
from src.utils.KeyManager import KEYS


class Preperator:

    def __init__(self):
        self.n = CachedNetLoader(k.set_key(KEYS.ALPHA), False)

    def prepare_experiment(self, stock=Ticker.Ticker, prep_id: int = 1, all_data=True, proc_flow_id=5, DBG=True):
        """

        ID | Steps
        1 | Load Data | Apply ProcFlow | Splits data in train & test
        2 | Load Data | Apply ProcFlow | Regularize data | Splits data in train & test


        Prepares a DS / DL experiment for the given stock by applying the specified preperations and pre-processors
        :param stock: Stock (ticker)
        :param prep_id: preperation id of the specified prep workflow
        :param all_data: True when working on a full data set. False for a (smaller) sample to speed things up
        :param proc_flow_id: ID of the specified pre-processor workflow (ProcFlow) that preperes the data
        :param DBG: Debug / vebose console output. True by default
        :return:
        """
        # dataloder
        n = self.n

        if prep_id == 1:
            if DBG: print("Loading Data for stock: " + stock.name)
            df_all = n.load_data(stock, TimeFrame.TimeFrame.DAILY, full=all_data)
            if DBG: print("Create a ProcFlow")
            pf = ProcFlow(DBG)
            if DBG: print("Applying pre-processor: ", proc_flow_id, "on stock: " + stock.name)
            df_all = pf.proc_switch(data=df_all, stock=stock, y_col="Close", nr_n=5, proc_id=proc_flow_id)

            if DBG:
                df = df_all
                print("Done!")
                print("Raw data: ")
                print(df.info())
                print("Describing data: ")
                print(df.describe())
                print("Sample data: ")
                print(df.tail(5))

            if DBG: print("Split df_all in train & test")
            train_df, test_df = pf.split_data(df=all_data, split_ratio=0.80, vrb=True)

            return train_df, test_df

        if prep_id == 2:
            if DBG: print("Loading Data for stock: " + stock.name)
            df_all = n.load_data(stock, TimeFrame.TimeFrame.DAILY, full=all_data)
            if DBG: print("Create a ProcFlow")
            pf = ProcFlow(DBG)
            if DBG: print("Applying pre-processor: ", proc_flow_id, "on stock: " + stock.name)
            df_all = pf.proc_switch(data=df_all, stock=stock, y_col="Close", nr_n=5, proc_id=proc_flow_id)
            # if DBG: print("Apply MinMax regularization")
            #  MinMax regularization has a but that sets all percentage values to ZERO :-(
            # df_all = p.proc_min_max_normalize(df=df_all, max_scale=20, all_col=False, exclude_col=["Date"])

            return df_all

        if prep_id == 3:
            if DBG: print("Loading Data for stock: " + stock.name)
            df_all = n.load_data(stock, TimeFrame.TimeFrame.DAILY, full=all_data)

            # TODO
            return df_all
