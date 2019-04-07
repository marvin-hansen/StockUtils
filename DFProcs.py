def check_missing_values(df, verbose: bool):
    """
    Checks the given data frame for missing value and returns a boolean value.
    When set to verbose, the function prints out number and percentage of missing data

    :param df: pandas dataframe
    :param verbose: boolean
    :return: True if df contains missing values, otherwise false.
    """

    # to get the total summation of all missing values in the DataFrame,
    # #we chain two .sum() methods together:
    if (verbose):
        nr_missing = df.isnull().sum().sum()
        nr_values = len(df)
        prct_missing = (nr_missing / nr_values) * 100

        print("Has missing values: " + str(df.isnull().values.any()))
        # inspect each column
        col_names = df.columns.values.tolist()
        for c in col_names:
            print(str(c) + " missing values: " + str(df[c].isnull().sum()))
        print()
        print("Total Values: " + str(nr_values))
        print("Total Missing: " + str(nr_missing))
        print("Percentage Missing: " + str(prct_missing))
        print()

    return df.isnull().values.any()


def remove_missing_values(df):
    """
    Drop each row in a data frame where at least one element is missing
    and returns a copy without missing values.
    :param df: pandas data frame
    :return: df without missing values.
    """
    return df.dropna()


def fill_nan(df):
    """ Fills NaN values with zero
    :param df: pandas dataframe
    :return: dataframe  without NaN
    """
    return df.fillna(0)


def reverse_df(df):
    """
    reverses all rows so that the last one are listed first
    :param df: pandas data frame
    :return: reversed frame
    """
    return df.iloc[::-1]


def rename_column(df, old_name, new_name):
    """
    renames a column in the given data frame
    :param df: pandas dataframe
    :param old_name:
    :param new_name:
    :return: void
    """
    return df.rename(index=str, columns={old_name: new_name})


def remove_column(df, col_name):
    """
    Deletes the given column(s) on the given data frame
    :param df: pandas data frame
    :param col_name: string array of column names
    :return: data frame without the columns
    """
    df.drop(columns=col_name)


def inspect_df(df):
    """
    shows key infos about the given dataframe
    :param df:
    :return: void
    """
    print("Nr. of data: " + str(len(df)))
    print("Sample data: ")
    print()
    print("Meta Data")
    print(df.info())
    print()
    print(df.head(5))
    print()
