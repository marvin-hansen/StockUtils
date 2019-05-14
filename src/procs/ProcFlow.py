from src.procs import Procs as p


class ProcFlow():
    def __init__(self, dbg):
        self.DBG = dbg

    def proc_switch(self, data, stock, y_col="", nr_nxt=1, proc_id=1):

        if proc_id == 1:
            return self.proc_01(data, stock, y_col, nr_nxt=nr_nxt)

        if proc_id == 2:
            return self.proc_02(data, stock, y_col, nr_nxt=nr_nxt)

        if proc_id == 3:
            return self.proc_03(data, stock, y_col, nr_nxt=nr_nxt)
        else:
            print("No matching proc ID found")

    @staticmethod
    def proc_01(data, stock, y_col, nr_nxt: int):
        # seperate  columns into continous data columns and category data columns
        cont_vars = []  # clear everything, just in case
        cat_vars = []
        cont_vars = ["Open", "High", "Low", "Close", "Volume"]

        # ad y
        p.proc_add_next_y(df=data, y_column=y_col, number=nr_nxt, cont_vars=cont_vars)
        # run procs
        # add previous n values of y-column
        p.proc_add_previous_values(df=data, column_name=y_col, number=5, cont_vars=cont_vars)
        # percennt change of y-column
        p.proc_add_percent_change(df=data, column_name=y_col, cont_vars=cont_vars)
        # add Bollinger Band
        # data = p.proc_add_bband(df=data, stock=stock, cont_vars=cont_vars, add_diff_to_bb=True)
        data = p.proc_add_bband(df=data, stock=stock, cont_vars=cont_vars, add_diff_to_bb=False, add_ohlc_diff=True)
        # Remove NaN
        data = p.proc_fill_nan

        return data

    @staticmethod
    def proc_02(data, stock, y_col, nr_nxt: int):
        # seperate  columns into continous data columns and category data columns
        cont_vars = []  # clear everything, just in case
        cat_vars = []
        cont_vars = ["Open", "High", "Low", "Close", "Volume"]

        # ad y
        p.proc_add_next_y(df=data, y_column=y_col, number=nr_nxt, cont_vars=cont_vars)
        # run procs
        # add previous n values of y-column
        p.proc_add_previous_values(df=data, column_name=y_col, number=5, cont_vars=cont_vars)

        # categorify date
        p.proc_add_datepart(df=data, cont_vars=cont_vars, cat_vars=cat_vars)

        # percennt change
        p.proc_add_percent_change(df=data, column_name="Open", cont_vars=cont_vars)
        p.proc_add_percent_change(df=data, column_name="High", cont_vars=cont_vars)
        p.proc_add_percent_change(df=data, column_name="Low", cont_vars=cont_vars)
        p.proc_add_percent_change(df=data, column_name="Close", cont_vars=cont_vars)
        #
        p.proc_add_abs_percent_change(df=data, column_name="Close", cont_vars=cont_vars)

        # add Bollinger Band
        data = p.proc_add_bband(df=data, stock=stock, cont_vars=cont_vars, add_diff_to_bb=False, add_ohlc_diff=True)
        # Add SMA
        data = p.proc_add_sma20(df=data, cont_vars=cont_vars, stock=stock, add_diff=True)
        data = p.proc_add_sma200(df=data, cont_vars=cont_vars, stock=stock, add_diff=True)
        data = p.proc_add_sma20_sma_200_diff(df=data, cont_vars=cont_vars, stock=stock)
        data = p.proc_add_wma20_wma_60_diff(df=data, cont_vars=cont_vars, stock=stock, add_ohlc_diff=True)
        # Remove NaN
        data = p.proc_fill_nan

        return data

    @staticmethod
    def proc_03(data, stock, y_col="", nr_nxt=1):
        # seperate  columns into continous and category data columns
        cont_vars = []  # clear everything, just in case
        cat_vars = []
        cont_vars = ["Open", "High", "Low", "Close", "Volume"]

        # categorify date
        p.proc_add_datepart(df=data, cont_vars=cont_vars, cat_vars=cat_vars)

        # percent change
        p.proc_add_percent_change(df=data, column_name="Open", cont_vars=cont_vars)
        p.proc_add_percent_change(df=data, column_name="High", cont_vars=cont_vars)
        p.proc_add_percent_change(df=data, column_name="Low", cont_vars=cont_vars)
        p.proc_add_percent_change(df=data, column_name="Close", cont_vars=cont_vars)
        #
        p.proc_add_abs_percent_change(df=data, column_name="Close", cont_vars=cont_vars)

        # add momentum
        data = p.proc_add_mom(df=data, cont_vars=cont_vars, stock=stock)
        # add momentum percentage change
        data = p.proc_add_percent_change(df=data, column_name="MOM", cont_vars=cont_vars)

        # ad y
        p.proc_add_next_y(df=data, y_column=y_col, number=nr_nxt, cont_vars=cont_vars)
        # run procs
        # add previous 5
        p.proc_add_previous_values(df=data, column_name="Close", number=5, cont_vars=cont_vars)

        # add Bollinger Band
        data = p.proc_add_bband(df=data, stock=stock, cont_vars=cont_vars, add_diff_to_bb=True)
        # Add SMA
        data = p.proc_add_sma20(df=data, cont_vars=cont_vars, stock=stock, add_diff=True)
        data = p.proc_add_sma200(df=data, cont_vars=cont_vars, stock=stock, add_diff=True)
        data = p.proc_add_sma20_sma_200_diff(df=data, cont_vars=cont_vars, stock=stock)
        # SMA percentage change
        data = p.proc_add_percent_change(df=data, column_name="SMA_20", cont_vars=cont_vars)
        data = p.proc_add_percent_change(df=data, column_name="SMA_200", cont_vars=cont_vars)

        # Add WMA with ohlc_diff=True
        data = p.proc_add_wma20_wma_60_diff(df=data, cont_vars=cont_vars, stock=stock, add_ohlc_diff=True)
        # WMA percentage change
        data = p.proc_add_percent_change(df=data, column_name="WMA_20", cont_vars=cont_vars)
        data = p.proc_add_percent_change(df=data, column_name="WMA_60", cont_vars=cont_vars)
        # Remove NaN
        data = p.proc_fill_nan

        return data
