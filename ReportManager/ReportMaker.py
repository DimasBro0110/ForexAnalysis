__author__ = 'dimas'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from MySQL_db_Connection.ConnectionHandler import DataHandler

def Parser(string):
    whole_lst = string.split("\n")
    time_lst, real_data_lst, predicted_data_lst = [], [], []
    for i in whole_lst:
        lst = i.split(" ")
        if len(lst) > 3:
            time_lst.append(lst[2] + " " + lst[3])
            real_data_lst.append(float(lst[0]))
            predicted_data_lst.append(float(lst[1]))
    time_lst = pd.to_datetime(time_lst)
    real_data_series = pd.TimeSeries(real_data_lst, index=time_lst)
    predicted_data_series = pd.TimeSeries(predicted_data_lst, index=time_lst)
    return real_data_lst, predicted_data_lst, time_lst

data = DataHandler("localhost", "Dimas", "Dimas", "Forex")
s = data.GetReportForResearch()

real_data, predicted_data, time_ser = Parser(s)

real_data = np.array(real_data)
predicted_data = np.array(predicted_data)

deviation = np.std(real_data) / np.sqrt(len(real_data))
print(deviation)

real_data_plus = real_data + 1.96*deviation
real_data_minus = real_data - 1.96*deviation

plt.plot_date(x=time_ser, y=real_data, fmt="b-", label="Real Data", linewidth=2.0)
plt.plot_date(x=time_ser, y=real_data_plus, fmt="r--", label="Trustee Interval")
plt.plot_date(x=time_ser, y=real_data_minus, fmt="r--")
plt.plot_date(x=time_ser, y=predicted_data, fmt="kD:", label="Predicted Data", linewidth=2.0)
plt.legend(loc='best')
plt.show()


