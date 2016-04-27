__author__ = 'dimas'

import pandas as pd
import numpy as np
import statsmodels.api as sm

# data to test
# st = "43574 2016-04-27 13:45:28 1.131460" + "\n" + \
#      "43573 2016-04-27 13:45:18 1.13160" + "\n" + \
#      "43572 2016-04-27 13:45:07 1.13160" + "\n" + \
#      "43571 2016-04-27 13:44:57 1.13160" + "\n"

class DataParser():

    def __init__(self, s):
        self.data = s

    def DoParse(self):
        lst = self.data.split("\n")
        lst_time, lst_vals, lst_val_id = [], [], []
        for s in lst:
            ls = s.split(" ")
            if len(ls) > 3:
                lst_time.append(ls[1] + " " + ls[2])
                lst_vals.append(float(ls[3]))
                lst_val_id.append(ls[0])
        lst_time = pd.to_datetime(lst_time)
        time_series = pd.TimeSeries(lst_vals, index=lst_time)
        return time_series, lst_vals, lst_val_id


class Forecasting():

    def __init__(self, time_ser_data):
        self.data = time_ser_data

    def DoForecast(self):
        arima_model = sm.tsa.ARIMA(self.data, (4, 2, 1), freq='T').fit()
        forecast = arima_model.forecast(steps=2)
        forecasted_data = forecast[0]
        return forecasted_data