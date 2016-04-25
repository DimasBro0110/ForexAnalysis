__author__ = 'dimas'

from MySQL_db_Connection.ConnectionHandler import DataHandler
from ClientTCP.Client import ClientHandler

if __name__ == "__main__":
    obj = DataHandler("localhost", "Dimas", "Dimas", "Forex")
    cur, s = obj.GetReport()
    print(s)