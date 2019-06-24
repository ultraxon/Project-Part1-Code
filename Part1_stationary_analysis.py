import pandas as pd

from statsmodels.tsa.stattools import adfuller

df = pd.read_csv('./Datas/IBM.txt', index_col='Date')
df.index = pd.to_datetime(df.index)


def adf_test(time_series):
    print('Result for Dickey Fuller test:')
    dftest = adfuller(time_series, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags used', 'Number of observation used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print(dfoutput)


adf_test(df['High'])
