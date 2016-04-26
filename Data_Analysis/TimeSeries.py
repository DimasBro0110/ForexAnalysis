__author__ = 'dimas'

import pandas as pd
import numpy as np
import statsmodels.api as sm

ls_time = ['2016-03-14 08:30:50',
           '2016-03-14 08:30:55',
           '2016-03-14 08:31:01',
           '2016-03-14 08:31:06',
           '2016-03-14 08:31:12',
           '2016-03-14 08:31:18',
           '2016-03-14 08:31:23',
           '2016-03-14 08:31:29',
           '2016-03-14 08:32:50',
           '2016-03-14 08:32:55',
           '2016-03-14 08:33:01',
           '2016-03-14 08:33:06',
           '2016-03-14 08:37:26',
           ]

ls_vals = [1.11614,
           1.11604,
           1.11604,
           1.11606,
           1.11606,
           1.11606,
           1.1161,
           1.11608,
           1.11624,
           1.11624,
           1.11624,
           1.11624,
           1.11655
           ]

ls_time = pd.to_datetime(ls_time)
ts = pd.Series(ls_vals, index=ls_time)

dataset = ts[0:len(ts) - 2]

arima_model = sm.tsa.ARIMA(dataset, (4, 1, 2), freq='T').fit()
forecast = arima_model.forecast(steps=2)
forecasted_data = forecast[0]

print(forecasted_data)
