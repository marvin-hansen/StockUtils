from src.enum import PROCS
from src.enum import TECHIND
from src.enum import Ticker
from src.enum import TimeFrame
from src.procs import Procs as p
from src.utils import KeyManager as k
from src.utils import Net as n
from src.utils import TechInd as t
from src.utils.KeyManager import KEYS


def main():
    def run():
        # set flags
        key = False
        net = False
        tech = False
        splt = False
        verbose = True
        #
        procs = True

        if key:
            # sample usage
            print("Loading keys from files...")
            a_key = k.set_key(KEYS.ALPHA)
            q_key = k.set_key(KEYS.QUANDL)

        if procs:

            stock = Ticker.Ticker.AMZN

            def load_data():
                all = True
                print(stock.name)
                df_all, _ = n.cached_stock_loader(stock, TimeFrame.TimeFrame.DAILY, full=all)
                df_all = p.rename_data(df_all)
                df_all.reset_index()
                df_all = p.convert_date(df_all, "Date")
                return df_all

            cont_vars = []  # clear everything, just in case
            cont_vars = ["Open", "High", "Low", "Close", "Volume"]
            cat_vars = []

            data_all = load_data()

            print(data_all.tail(3))
            # print(df_all.tail(3))

            proc = PROCS.PROCS.ADD_BBAND

            if proc is PROCS.PROCS.ADD_PRV_VAL:
                print("Apply proc: " + proc.name)
                nr_prv = 5
                p.proc_add_previous_values(df=data_all, column_name="Close", number=nr_prv, cont_vars=cont_vars)
                p.inspect_data(data_all, cont_vars, cat_vars)

            if proc is PROCS.PROCS.ADD_PRCT_CHNGE:
                print("Apply proc: " + proc.name)
                p.proc_add_percent_change(df=data_all, column_name="Close", cont_vars=cont_vars)
                p.inspect_data(data_all, cont_vars, cat_vars)

            if proc is PROCS.PROCS.ADD_BBAND:
                print("Apply proc: " + proc.name)
                data_bb = p.proc_add_bband(df=data_all, stock=stock,
                                           cont_vars=cont_vars, add_diff_to_bb=True)
                p.inspect_data(data_bb, cont_vars, cat_vars)

            if proc is PROCS.PROCS.ADD_SMA:
                print("Apply proc: " + proc.name)

                data_sma = p.proc_add_sma20(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=True)
                data_sma = p.proc_add_sma200(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=True)

                data_sma = p.proc_add_sma20_sma_200_diff(df=data_all, cont_vars=cont_vars, stock=stock)

                p.inspect_data(data_sma, cont_vars, cat_vars)

            if proc is PROCS.PROCS.ADD_EMA:
                print("Apply proc: " + proc.name)

                # data_ema = p.proc_add_ema10(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=True)
                # data_ema = p.proc_add_ema30(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=True)

                data_ema = p.proc_add_ema10_ema_30_diff(df=data_all, cont_vars=cont_vars, stock=stock)

                p.inspect_data(data_ema, cont_vars, cat_vars)

            if proc is PROCS.PROCS.ADD_WMA:
                print("Apply proc: " + proc.name)

                data_wma = p.proc_add_wma20(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=True)
                data_wma = p.proc_add_wma60(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=True)

                data_wma = p.proc_add_wma20_wma_60_diff(df=data_all, cont_vars=cont_vars, stock=stock)

                p.inspect_data(data_wma, cont_vars, cat_vars)

        if net:
            stock = Ticker.Ticker.AMZN
            all = False
            print(stock.name)
            data_all, _ = n.cached_stock_loader(stock, TimeFrame.TimeFrame.DAILY, full=all)
            print(data_all.tail(3))
            # print(df_all.tail(3))

        if splt:
            stock = Ticker.Ticker.AMZN
            all = False
            print(stock.name)
            data_all, _ = n.cached_stock_loader(stock, TimeFrame.TimeFrame.DAILY, full=all)
            print(data_all.tail(3))

            # Split df_all i train, test & valid
            train_df, test_df, valid_df = p.split_data(df=data_all,
                                                       split_ratio=0.90,
                                                       nr_valid=5,
                                                       vrb=True)
            print("Validation")
            print(valid_df.tail(5))

            print("Test")
            print(test_df.tail(3))

            print("Test")
            print(test_df.head(3))

            print("Train")
            print(train_df.tail(3))

        if tech:
            stock = Ticker.Ticker.AMZN
            ind = TECHIND.TECHIND.BBANDS
            intv = TimeFrame.TimeFrame.DAILY
            print(stock.name)

            # uncached on first trye
            data_all = t.get_cached_tech_indicator(ind, stock, intv)

            # cached on second try
            data_all = t.get_cached_tech_indicator(ind, stock, intv)

            print(data_all.info())
            print(data_all.tail(1).T)

    run()


if __name__ == '__main__':
    main()
