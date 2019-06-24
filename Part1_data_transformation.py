import pandas as pd
import re
import datetime
import numpy as np

from statsmodels.tsa.stattools import adfuller


def adf_test(time_series):
    print('Result for Dickey Fuller test:')
    dftest = adfuller(time_series, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags used', 'Number of observation used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print(dfoutput)


dates = [0]
prices = [0]
with open('./Datas/IBM.txt', 'r') as f:
    next(f)
    for line in f:
        data_list = re.split(',', line)
        data_list[0] = datetime.datetime.strptime(data_list[0], '%Y-%m-%d')
        data_list[1] = float(data_list[1][:-1])
        dates.append(data_list[0])
        prices.append(data_list[1])
dates = np.array(dates)
prices = np.array(prices)

df = pd.DataFrame(prices[1:])
diff = df.diff(1)
diff.dropna(inplace=True)
adf_test(diff[0])
