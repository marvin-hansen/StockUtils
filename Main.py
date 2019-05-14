from src.enum import INTERVAL
from src.enum import PROCS
from src.enum import TECHIND
from src.enum import Ticker
from src.enum import TimeFrame
from src.procs import Procs as p
from src.utils import KeyManager as k
from src.utils import TechInd as t
from src.utils.AlphaDataLoader import AlphaDataLoader
from src.utils.CachedNetLoader import CachedNetLoader
from src.utils.KeyManager import KEYS


def main():
    def run():
        # Debug
        DBG = True
        # Default data loader
        KEY = k.set_key(KEYS.ALPHA)
        n = CachedNetLoader(KEY, DBG)
        # set flags
        load = False
        load_intra_day = False
        alpha_loader = True
        key = False
        tech = False
        splt = False
        procs = False
        proc_flow = False

        if load:
            stock = Ticker.Ticker.AMZN
            all = True
            DBG = True

            if DBG: print(stock.name)
            if DBG: print("Loading Data for stock: " + stock.name)
            df_all = n.load_data(stock, TimeFrame.TimeFrame.DAILY, full=all)
            if DBG:
                print("Done!")
                print("Raw data: ")
                print(df_all.info())
                print(df_all.info())
                print(df_all.tail(3))

        if load_intra_day:

            stock = Ticker.Ticker.AMZN
            DBG = True

            if DBG: print(stock.name)
            if DBG: print("Loading Data for stock: " + stock.name)
            df_all = n.load_intraday_data(stock, INTERVAL.INTERVAL.FIVE_MIN, full=False, vrb=True)
            if DBG:
                print("Done!")
                print("Raw data: ")
                print(df_all.info())

                print(df_all.info())
                print(df_all.tail(3))

        if alpha_loader:
            stock = Ticker.Ticker.AAPL
            DBG = True
            all = True

            n = AlphaDataLoader(api_key=KEY, dbg=DBG)

            if DBG: print(stock.name)
            if DBG: print("Loading Daily Close Data for stock: " + stock.name)
            df_all = n.load_web_data(stock, TimeFrame.TimeFrame.DAILY, full=all, vrb=DBG)
            if DBG:
                print("Done!")
                print("Raw data: ")
                print(df_all.info())
                print(df_all.info())
                print(df_all.tail(3))

            if DBG: print(stock.name)
            if DBG: print("Loading Intradeday Data for stock: " + stock.name)
            df_all = n.load_intraday_data(stock, INTERVAL.INTERVAL.FIVE_MIN, full=False, vrb=True)
            if DBG:
                print("Done!")
                print("Raw data: ")
                print(df_all.info())
                print(df_all.info())
                print(df_all.tail(3))

            crypto_symbol: str = "BTC"
            market: str = "CNY"

            if DBG: print(crypto_symbol)
            if DBG: print("Loading Closing price Data for : " + crypto_symbol)
            df_all = n.load_crypto_data(crypto_symbol=crypto_symbol, time_frame=TimeFrame.TimeFrame.DAILY,
                                        market=market)
            if DBG:
                print("Done!")
                print("Raw data: ")
                print(df_all.info())
                print(df_all.info())
                print(df_all.tail(3))

        if proc_flow:
            stock = Ticker.Ticker.GOOGL
            all = True
            DBG = True

            if DBG: print(stock.name)
            if DBG: print("Loading Data for stock: " + stock.name)
            df_all = n.load_data(stock, TimeFrame.TimeFrame.DAILY, full=all)




        if key:
            # sample usage
            print("Loading keys from files...")
            a_key = k.set_key(KEYS.ALPHA)
            q_key = k.set_key(KEYS.QUANDL)

        if procs:

            # set stock
            stock = Ticker.Ticker.AMZN

            # Set which proc to run
            proc = PROCS.PROCS.BBAND


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

            def init_cont_vars():
                cont_vars = []  # clear everything, just in case
                cont_vars = ["Open", "High", "Low", "Close", "Volume"]
                return cont_vars


            cat_vars = []

            data_all = load_data()

            # Run selected procs...
            if proc is PROCS.PROCS.NXT_VAL:
                print("Apply proc: " + proc.name)
                nr_nxt = 2
                cont_vars = init_cont_vars()
                p.proc_add_next_y(df=data_all, y_column="Close", number=nr_nxt, cont_vars=cont_vars)
                p.inspect_data(data_all, cont_vars, cat_vars)

            # Run selected procs...
            if proc is PROCS.PROCS.PRV_VAL:
                print("Apply proc: " + proc.name)
                nr_prv = 5
                cont_vars = init_cont_vars()
                p.proc_add_previous_values(df=data_all, column_name="Close", number=nr_prv, cont_vars=cont_vars)
                p.inspect_data(data_all, cont_vars, cat_vars)

            if proc is PROCS.PROCS.PRCT_CHNGE:
                print("Apply proc: " + proc.name)
                cont_vars = init_cont_vars()

                p.proc_add_percent_change(df=data_all, column_name="Close", cont_vars=cont_vars)
                p.inspect_data(data_all, cont_vars, cat_vars)

            if proc is PROCS.PROCS.ABS_PRCT_CHNG:
                print("Apply proc: " + proc.name)
                cont_vars = init_cont_vars()
                p.proc_add_abs_percent_change(df=data_all, column_name="Close", cont_vars=cont_vars)
                p.inspect_data(data_all, cont_vars, cat_vars)


            if proc is PROCS.PROCS.MACD:
                print("Apply proc: " + proc.name)
                print("Test normal MACD ")
                data_macd = None
                cont_vars = init_cont_vars()
                data_macd = p.proc_add_macd(df=data_all, cont_vars=cont_vars, stock=stock)

                p.inspect_data(data_macd, cont_vars, cat_vars)

            if proc is PROCS.PROCS.RSI:
                print("Apply proc: " + proc.name)
                print("Test normal RSI ")
                cont_vars = init_cont_vars()
                data_macd = None
                rsi_data = p.proc_add_rsi(df=data_all, cont_vars=cont_vars, stock=stock)

                p.inspect_data(rsi_data, cont_vars, cat_vars)

                print("Apply proc: " + proc.name)
                print("Test normal RSI with percentage change ")
                cont_vars = init_cont_vars()
                data_macd = None
                rsi_data = p.proc_add_rsi(df=data_all, cont_vars=cont_vars, stock=stock, change=True)

                p.inspect_data(rsi_data, cont_vars, cat_vars)

            if proc is PROCS.PROCS.ADX:
                print("Apply proc: " + proc.name)
                print("Test normal ADX ")
                data_adx = None
                cont_vars = init_cont_vars()
                data_adx = p.proc_add_adx(df=data_all, cont_vars=cont_vars, stock=stock)
                p.inspect_data(data_adx, cont_vars, cat_vars)

                print("Apply proc: " + proc.name)
                print("Test  ADX with percentage change ")
                data_obv = None
                cont_vars = init_cont_vars()
                data_adx = p.proc_add_adx(df=data_all, cont_vars=cont_vars, stock=stock, change=True)
                p.inspect_data(data_adx, cont_vars, cat_vars)

            if proc is PROCS.PROCS.OBV:
                print("Apply proc: " + proc.name)
                print("Test normal OBV ")
                data_obv = None
                cont_vars = init_cont_vars()
                data_obv = p.proc_add_obv(df=data_all, cont_vars=cont_vars, stock=stock)
                p.inspect_data(data_obv, cont_vars, cat_vars)

                print("Apply proc: " + proc.name)
                print("Test  OBV with percentage change ")
                data_obv = None
                cont_vars = init_cont_vars()
                data_obv = p.proc_add_obv(df=data_all, cont_vars=cont_vars, stock=stock, change=True)
                p.inspect_data(data_obv, cont_vars, cat_vars)

            if proc is PROCS.PROCS.MOM:
                print("Apply proc: " + proc.name)
                print("Test normal momentum  ")
                data_mom = None
                cont_vars = init_cont_vars()
                data_mom = p.proc_add_mom(df=data_all, cont_vars=cont_vars, stock=stock)
                p.inspect_data(data_mom, cont_vars, cat_vars)

                print("Apply proc: " + proc.name)
                print("Test momentum with percentage change ")
                data_mom = None
                cont_vars = init_cont_vars()
                data_mom = p.proc_add_mom(df=data_all, cont_vars=cont_vars, stock=stock, change=True)
                p.inspect_data(data_mom, cont_vars, cat_vars)

            if proc is PROCS.PROCS.OHLC_AVG:
                print("Apply proc: " + proc.name)
                print("Test normal OHLC average ")
                cont_vars = init_cont_vars()
                data_ohlc = p.proc_add_ohlc_avg(data_all, cont_vars)
                p.inspect_data(data_ohlc, cont_vars, cat_vars)

                print("Test OHLC average with diff to close price")
                data_ohlc = None
                cont_vars = init_cont_vars()

                data_ohlc = p.proc_add_ohlc_avg(data_all, cont_vars, add_diff=True)
                p.inspect_data(data_ohlc, cont_vars, cat_vars)

                print("Test normal OHLC average with diff to all OHLC prices")
                data_ohlc = None
                cont_vars = init_cont_vars()
                data_ohlc = p.proc_add_ohlc_avg(data_all, cont_vars, add_ohlc_diff=True)
                p.inspect_data(data_ohlc, cont_vars, cat_vars)

            if proc is PROCS.PROCS.BBAND:
                print("Apply proc: " + proc.name)
                print("Test normal bands")
                data_bb = None
                cont_vars = init_cont_vars()
                data_bb = p.proc_add_bband(df=data_all, stock=stock,
                                           cont_vars=cont_vars, add_diff_to_bb=False)
                p.inspect_data(data_bb, cont_vars, cat_vars)

                print("Test bands with diff to close price ")
                data_bb = None
                cont_vars = init_cont_vars()
                data_bb = p.proc_add_bband(df=data_all, stock=stock,
                                           cont_vars=cont_vars, add_diff_to_bb=True)
                p.inspect_data(data_bb, cont_vars, cat_vars)

                print("Test bands with diff to all four OHLC prices ")
                data_bb = None
                cont_vars = init_cont_vars()
                data_bb = p.proc_add_bband(df=data_all, stock=stock,
                                           cont_vars=cont_vars, add_diff_to_bb=False, add_ohlc_diff=True)
                p.inspect_data(data_bb, cont_vars, cat_vars)

            if proc is PROCS.PROCS.SMA:
                print("Apply proc: " + proc.name)

                cont_vars = init_cont_vars()
                # data_sma = p.proc_add_sma20(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=False,add_ohlc_diff=True)
                # data_sma = p.proc_add_sma200(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=False,add_ohlc_diff=True)

                data_sma = p.proc_add_sma20_sma_200_diff(df=data_all, cont_vars=cont_vars, stock=stock,
                                                         add_ohlc_diff=True)

                p.inspect_data(data_sma, cont_vars, cat_vars)

                print(data_sma.info())

            if proc is PROCS.PROCS.EMA:
                print("Apply proc: " + proc.name)
                print("Test normal EMA")
                data_ema = None
                cont_vars = init_cont_vars()
                # data_ema = p.proc_add_ema10(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=True)
                # data_ema = p.proc_add_ema30(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=True)

                data_ema = p.proc_add_ema10_ema_30_diff(df=data_all, cont_vars=cont_vars, stock=stock,
                                                        add_ohlc_diff=True)

                p.inspect_data(data_ema, cont_vars, cat_vars)

            if proc is PROCS.PROCS.WMA:
                print("Apply proc: " + proc.name)

                data_wma = None
                cont_vars = init_cont_vars()

                data_wma = p.proc_add_wma20(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=True)
                data_wma = p.proc_add_wma60(df=data_all, cont_vars=cont_vars, stock=stock, add_diff=True)

                data_wma = None
                cont_vars = init_cont_vars()
                data_wma = p.proc_add_wma20_wma_60_diff(df=data_all, cont_vars=cont_vars, stock=stock,
                                                        add_ohlc_diff=True)
                p.inspect_data(data_wma, cont_vars, cat_vars)

                data_wma = None
                cont_vars = init_cont_vars()
                data_wma = p.proc_add_wma5_wma_20_diff(df=data_all, cont_vars=cont_vars, stock=stock,
                                                       add_ohlc_diff=True)
                p.inspect_data(data_wma, cont_vars, cat_vars)

        if splt:
            stock = Ticker.Ticker.AMZN
            all = True
            print(stock.name)
            data_all = n.load_data(stock, TimeFrame.TimeFrame.DAILY, full=all)

            # Split df_all in train & test
            train_df, test_df = p.split_data(df=data_all, split_ratio=0.80, vrb=True)

            print()
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
