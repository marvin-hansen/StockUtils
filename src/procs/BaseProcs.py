class BaseProcs:

    def drop_features(df, features):
        """
        Removes the collumn matching a features name
        :param df: pandas data frame
        :param  features: [String Array]
        :return: Void - modifies the frame in place
        """
        return df.drop(columns=features)

    def add_previous_values(df, column_name, number):
        """ Adds n-previous values and stores each in a seperate column
            According to findings by tsfresh, the previous value can have as much
            as 88.5% significance on predicting the current value.
            https://github.com/blue-yonder/tsfresh/blob/master/notebooks/timeseries_forecasting_google_stock.ipynb

        :param df: pandas data frame
        :param column_name: source column
        :param number: number of time periods to add
        :return: Void - modifies the frame in place
        """
        for n in range(1, (number + 1)):
            df[column_name + str("-") + str(n)] = df[column_name].shift(-n)

    def calc_percent_change(df, column_name):
        """
        Calculates the percentage change for each value in the given column
        :param df: pandas data frame
        :param column_name: String - name of the column
        :return: Void - modifies the frame in place
        """
        df[column_name + "-pct-chng"] = (df[column_name + "-delta"] / df[column_name]) * 100

    def calc_row_delta(df, column_name):
        """
        calculates the difference between the current and the previous value in the given column
        :param df: pandas data frame
        :param column_name: String - name of the column
        :return: Void - modifies the frame in place
        """
        df[column_name + '-delta'] = df[column_name] - df[column_name].shift(-1)
