__author__ = 'dimas'

import threading
import time
import socket as sock
from MySQL_db_Connection.ConnectionHandler import DataHandler
from Data_Analysis.TimeSeries import DataParser, Forecasting

host = 'localhost'
port = 8998
address = (host, port)


class ClientHandler(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.isRun = True
        self.data = DataHandler("localhost", "Dimas", "Dimas", "Forex")
        try:
            self.ClientSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            self.ClientSocket.connect(address)
        except Exception as ex:
            exit(1)

    def SetRunFlag(self, flag):
        self.isRun = flag

    def Connection(self):
        try:
            conn = sock.create_connection(address)
            return conn
        except Exception as ex:
            print(ex)

    def run(self):
        if self.ClientSocket:
            try:
                while self.isRun:
                    cur, dat = self.data.GetReport()
                    if len(dat) >= 50:
                        data = DataParser(dat)
                        dat, lst_vals, lst_vals_id = data.DoParse()
                        forecast = Forecasting(dat)
                        forested_data = forecast.DoForecast()
                        self.ClientSocket.send(
                            self.name + " " + str(forested_data[0]) + " " + str(forested_data[1]) + "\n")
                        data = self.ClientSocket.recv(10000)
                        if not data:
                            print('not data')
                        print(data)
                    else:
                        print('not expected length')
                    time.sleep(2)
            except Exception as ex:
                self.SetRunFlag(False)
                self.ClientSocket.close()
                print(ex)
                exit(1)
        else:
            print("Cannot connect to server")
            exit(1)


cl = ClientHandler("EUR_USD")
cl.run()