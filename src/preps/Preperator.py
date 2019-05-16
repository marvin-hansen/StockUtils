from src.enum import Ticker
from src.enum import TimeFrame
from src.procs.ProcFlow import ProcFlow
from src.utils import KeyManager as k
from src.utils.CachedNetLoader import CachedNetLoader
from src.utils.KeyManager import KEYS


class Preperator:

    def __init__(self):
        self.n = CachedNetLoader(k.set_key(KEYS.ALPHA), False)
        self.pf = ProcFlow(False)

    def prepare_mixed_learning_experiment(self, stock=Ticker.Ticker, prep_id: int = 1, all_data=True, proc_flow_id=5, split_train_test=False, DBG=True):
        """
        Stacks together processed datasets from different equity tickers.

        Don't forget to remove the date column before returning the combined dataset

        :param stock:
        :param prep_id:
        :param all_data:
        :param proc_flow_id:
        :param split_train_test:
        :param DBG:
        :return:
        """

        stock_AAPL = Ticker.Ticker.AAPL
        if DBG: print("Processing data for stock: " + stock_AAPL.name)
        df_AAPL = self.prepare_experiment(stock=stock_AAPL, prep_id=prep_id, all_data=all_data, proc_flow_id=proc_flow_id, split_train_test=split_train_test, DBG=DBG)

        stock_GOOGL = Ticker.Ticker.GOOGL
        if DBG: print("Processing data for stock: " + stock_GOOGL.name)
        df_GOOGL = self.prepare_experiment(stock=stock_GOOGL, prep_id=prep_id, all_data=all_data, proc_flow_id=proc_flow_id, split_train_test=split_train_test, DBG=DBG)

        stock_AMZN = Ticker.Ticker.AMZN
        if DBG: print("Processing data for stock: " + stock_AMZN.name)
        df_AMZN = self.prepare_experiment(stock=stock_AMZN , prep_id=prep_id, all_data=all_data, proc_flow_id=proc_flow_id, split_train_test=split_train_test, DBG=DBG)

        if DBG: print("Concatenate all of them together")
        # df_all = pd.concat([df_AAPL, df_GOOGL, df_AMZN], axis=0, join='inner', sort=False)
        df_all = df_AAPL # ignore_index maintains a continuous index across the combined data frame
        df_all = df_all.append(df_AMZN, sort=False, ignore_index=True)
        df_all = df_all.append(df_GOOGL, sort=False, ignore_index=True)

        df_all = df_all.drop(columns="Date")

        if split_train_test:
            if DBG: print("Split df_all in train & test")
            train_df, test_df = self.pf.split_data(df=df_all, split_ratio=0.80, vrb=DBG)
            return train_df, test_df
        else:
            return df_all



    def prepare_experiment(self, stock, prep_id: int = 1, all_data=True, proc_flow_id=5, split_train_test=False, DBG=True):
        """

        ID | Steps
        1 | Load Data | Apply ProcFlow | Splits data in train & test
        2 | Load Data | Apply ProcFlow | Regularize data [buggy] | Splits data in train & test

        Prepares a DS / DL experiment for the given stock by applying the specified preperations and pre-processors
        :param stock: Stock (ticker)
        :param prep_id: preperation id of the specified prep workflow
        :param all_data: True when working on a full data set. False for a (smaller) sample to speed things up
        :param proc_flow_id: ID of the specified pre-processor workflow (ProcFlow) that preperes the data
        :param DBG: Debug / vebose console output. True by default
        :return:
        """
        # dataloder.
        n = self.n
        pf = self.pf

        if prep_id == 1:
            if DBG: print("Loading Data for stock: " + stock.name)
            df_all = n.load_data(stock, TimeFrame.TimeFrame.DAILY, full=all_data)

            if DBG: print("Create a ProcFlow")


            if DBG: print("Applying pre-processor: ", proc_flow_id, "on: " + stock.name)
            df_all = pf.proc_switch(data=df_all, stock=stock, y_col="Close", nr_n=5, proc_id=proc_flow_id)

            if DBG: print("Remove all NaN values")
            df_all = df_all.fillna(0)

            if split_train_test:
                if DBG: print("Split df_all in train & test")
                train_df, test_df = pf.split_data(df=df_all, split_ratio=0.80, vrb=DBG)
                return train_df, test_df
            else:
                return df_all


        if prep_id == 2:
            if DBG: print("Loading Data for stock: " + stock.name)
            df_all = n.load_data(stock, TimeFrame.TimeFrame.DAILY, full=all_data)
            if DBG: print("Create a ProcFlow")
            pf = ProcFlow(DBG)
            if DBG: print("Applying pre-processor: ", proc_flow_id, "on: " + stock.name)
            df_all = pf.proc_switch(data=df_all, stock=stock, y_col="Close", nr_n=5, proc_id=proc_flow_id)
            if DBG: print("Remove all NaN values")
            df_all = df_all.fillna(0)
            # if DBG: print("Apply MinMax regularization")
            #  MinMax regularization has a but that sets all percentage values to ZERO :-(
            # df_all = p.proc_min_max_normalize(df=df_all, max_scale=20, all_col=False, exclude_col=["Date"])

            if split_train_test:
                if DBG: print("Split df_all in train & test")
                train_df, test_df = pf.split_data(df=df_all, split_ratio=0.80, vrb=True)
                return train_df, test_df
            else:
                return df_all


        if prep_id == 3:
            if DBG: print("Loading Data for stock: " + stock.name)
            df_all = n.load_data(stock, TimeFrame.TimeFrame.DAILY, full=all_data)

            # TODO
            return df_all
