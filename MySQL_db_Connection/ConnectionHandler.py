import datetime
from time import strftime
import numpy as np

__author__ = 'dimas'

import mysql.connector


class DataHandler(object):
    def __init__(self, host, username, password, dbname):

        self.host = host
        self.username = username
        self.password = password
        self.dbname = dbname
        self.connection = self.EstablishConnection()

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

    def MakeInsert(self, predicted_ask, flag, instrument):


        cursor = self.connection.cursor()
        cursor.execute(
            """ INSERT INTO Forex.TRADE_REPORT(predicted_ask, instrument, isDone) VALUES (%s, %s, %s); """,
            (float(predicted_ask), instrument, flag)
        )
        self.connection.commit()

    def IdMaxGetter(self):

        cursor = self.connection.cursor()
        cursor.execute("""SELECT MAX(Forex.TRADE_REPORT.id) FROM Forex.TRADE_REPORT;""")
        id = cursor.fetchone()

        return id[0]


    def MakeUpdate(self, real_data, id):


        cursor = self.connection.cursor()
        cursor.execute(
            """ UPDATE Forex.TRADE_REPORT
                SET Forex.TRADE_REPORT.real_ask = %s,
                Forex.TRADE_REPORT.isDone = 1
                WHERE Forex.TRADE_REPORT.isDone = 0
                AND Forex.TRADE_REPORT.id = %s""",
            (float(real_data), id)
        )
        self.connection.commit()

    def GetReport(self):
        # query = """
        #   select st.STOCKID, st.TIME, st.ASK, st.STATUS
        #     from Forex.STOCKS st
        #     where DAY(st.TIME) = DAY(curdate())
        #     order by st.STOCKID DESC
        #     limit 30;
        # """

        query = """
          select st.STOCKID, st.TIME, st.ASK, st.STATUS
            from Forex.STOCKS st
            order by st.STOCKID DESC
            limit 30;
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            s = ''
            d = cursor.fetchall()
            if len(d) >= 30:
                for (STOCK_ID, DAT, ASK_BID, STATUS) in d:
                    s += str(STOCK_ID) + " " + \
                         str(DAT) + " " + \
                         str(ASK_BID) + \
                         str(STATUS) + "\n"
            else:
                s = ''
            return cursor, s
        except Exception as ex:
            print(ex)
