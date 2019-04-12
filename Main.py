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
        load = False
        key = False
        net = False
        tech = False
        splt = False
        DBG = True
        #
        procs = True

        if load:
            stock = Ticker.Ticker.AMZN

            def load_data():
                all = True
                print(stock.name)
                if DBG: print("Loading Data for stock: " + stock.name)
                df_all, _ = n.cached_stock_loader(stock, TimeFrame.TimeFrame.DAILY, full=all)
                if DBG:
                    print("Done!")
                    print("Raw data: ")
                    print(df_all.info())

                if DBG: print("Renaming columns: ")
                df_all = p.rename_data(df_all)
                if DBG:
                    print("Done!")
                    print("New columns : ")
                    print(df_all.info())
                # df_all.reset_index()

                if DBG: print("Converging date to DateTime: ")

                df_all = p.convert_date(df_all, "Date")
                if DBG:
                    print("Done!")
                # df_all.reset_index()

                return df_all

            # n.clear_cache()

            data_all = load_data()

            print(data_all.info())

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
                if DBG: print("Loading Data for stock: " + stock.name)
                df_all, _ = n.cached_stock_loader(stock, TimeFrame.TimeFrame.DAILY, full=all)
                if DBG:
                    print("Done!")
                    print("Raw data: ")
                    print(df_all.info())

                if DBG: print("Renaming columns: ")
                df_all = p.rename_data(df_all)
                if DBG:
                    print("Done!")
                    print("New columns : ")
                    print(df_all.info())

                if DBG: print("Converting date to DateTime: ")

                df_all = p.convert_date(df_all, "Date")
                if DBG:
                    print("Done!")

                return df_all

            cont_vars = []  # clear everything, just in case
            cont_vars = ["Open", "High", "Low", "Close", "Volume"]
            cat_vars = []

            data_all = load_data()

            print(data_all.tail(3))

            # Set which proc to run
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
                print("Test normal bands")
                data_bb = p.proc_add_bband(df=data_all, stock=stock,
                                           cont_vars=cont_vars, add_diff_to_bb=False)
                p.inspect_data(data_bb, cont_vars, cat_vars)

                print("Test bands with diff to close price ")
                data_bb = None
                data_bb = p.proc_add_bband(df=data_all, stock=stock,
                                           cont_vars=cont_vars, add_diff_to_bb=True)
                p.inspect_data(data_bb, cont_vars, cat_vars)

                print("Test bands with diff to all four OHLC prices ")
                data_bb = None
                data_bb = p.proc_add_bband(df=data_all, stock=stock,
                                           cont_vars=cont_vars, add_diff_to_bb=False, add_ohlc_diff=True)
                p.inspect_data(data_bb, cont_vars, cat_vars)


            if proc is PROCS.PROCS.ADD_SMA:
                print("Apply proc: " + proc.name)

                # data_sma = p.proc_add_sma20(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=False,add_ohlc_diff=True)
                # data_sma = p.proc_add_sma200(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=False,add_ohlc_diff=True)

                data_sma = p.proc_add_sma20_sma_200_diff(df=data_all, cont_vars=cont_vars, stock=stock,
                                                         add_ohlc_diff=True)

                p.inspect_data(data_sma, cont_vars, cat_vars)

                print(data_sma.info())

            if proc is PROCS.PROCS.ADD_EMA:
                print("Apply proc: " + proc.name)

                # data_ema = p.proc_add_ema10(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=True)
                data_ema = p.proc_add_ema30(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=True)

                #data_ema = p.proc_add_ema10_ema_30_diff(df=data_all, cont_vars=cont_vars, stock=stock)

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
            ind = TECHIND.TECHIND.EMA

            intv = TimeFrame.TimeFrame.DAILY
            print(stock.name)

            # uncached data loading on first try
            data_all = t.get_cached_tech_indicator(ind, stock, intv)

            # loading form cach on second try
            data_all = t.get_cached_tech_indicator(ind, stock, intv)

            print(data_all.info())
            print(data_all.tail(1).T)

    run()


if __name__ == '__main__':
    main()
