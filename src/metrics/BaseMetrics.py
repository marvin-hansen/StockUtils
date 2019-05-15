import numpy as np

from src.procs.OnlineVariance import OnlineVariance


class BaseMetrics:
    def __init__(self):
        self.ov = OnlineVariance()

    def daily_returns(self, df, column_name: str = "Close", log: bool = False):
        """
        Adds daily returns for the given column in the given data frame.

        :param df: pandas dataframe
        :param column_name: column for which the day returns to calculate
        :param log: Applies logarithm scale when flag is set to true
        :return: pandas dataframe
        """

        if log:
            df["Log_Returns"] = np.log(df[column_name] / df[column_name].shift(1))

        else:
            df["Day_Returns"] = df[column_name] / df[column_name].shift(1)

        return df

    def sharpe_ratio(self, returns, risk_free_rate=2.0, days=255):
        """

        Sharpe ratio is a measure for calculating risk adjusted return.

        :param returns:
        :param risk_free_rate:
        :param days:
        :return:
        """

        volatility = returns.std() * np.sqrt(days)

        return (returns.mean() - risk_free_rate) / volatility

    def information_ratio(self, returns, benchmark_returns=12.0, days=252):
        """
        The information ratio is an extension of the Sharpe ratio which replaces
        the risk-free rate of return with the returns of a benchmark portfolio


        :param returns:
        :param benchmark_returns:
        :param days:
        :return:
        """
        return_difference = returns - benchmark_returns
        volatility = return_difference.std() * np.sqrt(days)
        information_ratio = return_difference.mean() / volatility
        return information_ratio

    def m2_ratio(self, returns, benchmark_returns, rf, days=255):
        """
        The Modigliani (M2) ratio measures the returns of the portfolio,
        adjusted for the risk of the portfolio relative to that of some benchmark
        :param returns:
        :param benchmark_returns:
        :param rf:
        :param days:
        :return:
        """
        volatility = returns.std() * np.sqrt(days)
        sharpe_ratio = (returns.mean() - rf) / volatility
        benchmark_volatility = benchmark_returns.std() * np.sqrt(days)
        m2_ratio = (sharpe_ratio * benchmark_volatility) + rf
        return m2_ratio
