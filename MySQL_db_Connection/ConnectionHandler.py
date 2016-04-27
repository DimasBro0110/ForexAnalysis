import datetime
from time import strftime

__author__ = 'dimas'

import mysql.connector


class DataHandler(object):
    def __init__(self, host, username, password, dbname):

        self.host = host
        self.username = username
        self.password = password
        self.dbname = dbname

    def EstablishConnection(self):

        connection = None

        try:
            connection = mysql.connector.connect(host=self.host,
                                                 database=self.dbname,
                                                 user=self.username,
                                                 password=self.password
                                                 )

            if connection.is_connected():
                print("Succesfully connected to Database !!!")

        except Exception as ex:
            print(ex)

        return connection

    def GetReport(self):
        query = """
          select st.STOCKID, st.TIME, st.BID, st.STATUS
            from Forex.STOCKS st
            where DATE(st.TIME) = curdate()
            order by st.STOCKID DESC
            limit 50;
        """
        try:
            conn = self.EstablishConnection()
            cursor = conn.cursor()
            cursor.execute(query)
            s = ''
            d = cursor.fetchall()
            if len(d) >= 50:
                for (STOCK_ID, DAT, ASK_BID, STATUS) in d:
                    s += str(STOCK_ID) + " " + \
                        str(DAT) + " " + \
                        str(ASK_BID) + \
                        str(STATUS) + "\n"
                    print(s)
            else:
                print('not data')
            return cursor, s
        except Exception as ex:
            print(ex)

dat = DataHandler("localhost", "Dimas", "Dimas", "Forex")
cur, s = dat.GetReport()
print(s)