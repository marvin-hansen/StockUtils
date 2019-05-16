import numpy as np

from src.procs.OnlineVariance import OnlineVariance


# Volatility And Measures Of Risk-Adjusted Return With Python
# https://www.quantinsti.com/blog/volatility-and-measures-of-risk-adjusted-return-based-on-volatility


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

    def daily_volatility(self, df, column_name: str = "Close", nr_days=255):
        """
      Computes daily volatility for the given column using the Welford's method

      :param df: pandas data frame
      :param column_name:
      :param nr_days: number of days to include in rolling calculatin. Defauls 1 year (255 days)
      :return: pandas data frame
        """
        # name of the new column
        name = column_name + "-volatility"

        for n in range(nr_days):
            self.ov.include(df[column_name].shift(n))

        df[name] = self.ov.std

        return df

    def sharpe_ratio(self, returns, risk_free_rate=2.0, days=255):
        """
        Sharpe ratio is a measure for calculating risk adjusted return.
        The Sharpe ratio indicates how well an equity investment performs in comparison
        to the rate of return on a risk-free investment, such as U.S. government treasury bonds or bills.

        Any Sharpe ratio greater than 1.0 is considered acceptable to good by investors
        A ratio higher than 2.0 is rated as very good
        A ratio of 3.0 or higher is considered excellent.
        A ratio under 1.0 is considered sub-optimal.

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

    def m2_ratio(self, returns, benchmark_returns, risk_free_rate=2.0, days=255):
        """
        The Modigliani (M2) ratio measures the returns of the portfolio,
        adjusted for the risk of the portfolio relative to that of some benchmark
        :param returns:
        :param benchmark_returns:
        :param risk_free_rate:
        :param days:
        :return:
        """
        volatility = returns.std() * np.sqrt(days)
        sharpe_ratio = (returns.mean() - risk_free_rate) / volatility
        benchmark_volatility = benchmark_returns.std() * np.sqrt(days)
        m2_ratio = (sharpe_ratio * benchmark_volatility) + risk_free_rate
        return m2_ratio

    def f1_score(self, y_true: list, y_pred: list):
        """
        The F1 score can be interpreted as a weighted average of the precision and recall,
        where an F1 score reaches its best value at 1 and worst score at 0.

        The F1 score formula:

        F1 = 2 * (precision * recall) / (precision + recall)

        The relative contribution of precision and recall to the F1 score are equal.
        Precision measures the ability of the classifier not to label as positive a sample that is negative.
        Recall measures the ability of the classifier to find all the positive samples.

        A higher F1-Score means:
        1) The classifier finds what it should find
        2) The classifier leaves out what it should leave out
        3) Overall accuracy and reliability of the classifier increases with its F1 score

        :param y_true: Ground truth (correct) target values.
        :param y_pred: Estimated targets as returned by a classifier.

        :return: f1_score : float
        """
        # https://codereview.stackexchange.com/questions/36096/implementing-f1-score
        y_true = set(y_true)
        y_pred = set(y_pred)

        tp = len(y_true & y_pred)
        fp = len(y_pred) - tp
        fn = len(y_true) - tp

        if tp > 0:
            # precision =  tp / (tp + fp)
            precision = float(tp) / (tp + fp)
            # recall =  tp / (tp + fn)
            recall = float(tp) / (tp + fn)
            # f1 = 2 tp / (2 tp + fp + fn)
            return 2 * ((precision * recall) / (precision + recall))
        else:
            return 0
