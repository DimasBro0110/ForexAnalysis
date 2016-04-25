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
        query = """  SELECT con1.STOCK_ID,
                           con1.DAT,
                           con1.ASK_MAX,
                           con1.ASK_MIN,
                           con1.ASK_AVG,
                           con1.ASK_AVG - con2.ASK_AVG as 'DIF'
                        FROM
                    (SELECT st.STOCKID as 'STOCK_ID',
                           DATE(st.TIME) as 'DAT',
                           MAX(st.BID) as 'BID_MAX',
                           MIN(st.BID) as 'BID_MIN',
                           MAX(st.ASK) as 'ASK_MAX',
                           MIN(st.ASK) as 'ASK_MIN',
                           AVG(st.ASK) as 'ASK_AVG'
                        FROM Forex.STOCKS st
                        GROUP BY DATE(st.TIME)
                    )as con1
                    INNER JOIN
                    (SELECT st.STOCKID as 'STOCK_ID',
                           DATE(st.TIME) as 'DAT',
                           MAX(st.BID) as 'BID_MAX',
                           MIN(st.BID) as 'BID_MIN',
                           MAX(st.ASK) as 'ASK_MAX',
                           MIN(st.ASK) as 'ASK_MIN',
                           AVG(st.ASK) as 'ASK_AVG'
                        FROM Forex.STOCKS st
                        GROUP BY DATE(st.TIME)
                    ) as con2
                    ON con1.STOCK_ID > con2.STOCK_ID
                    GROUP BY con2.STOCK_ID;
                """
        try:
            conn = self.EstablishConnection()
            cursor = conn.cursor()
            cursor.execute(query)
            lst = []
            s = ''
            for (STOCK_ID, DAT, ASK_MAX, ASK_MIN, ASK_AVG, DIF) in cursor:
                # print(STOCK_ID, DAT.strftime("%Y-%m-%d"), ASK_MAX, ASK_MIN, ASK_AVG, DIF)
                lst.append([
                    STOCK_ID,
                    DAT.strftime("%Y-%m-%d"),
                    ASK_MAX,
                    ASK_MIN,
                    ASK_AVG,
                    DIF
                ])
                s += str(STOCK_ID) + " " + \
                    DAT.strftime("%Y-%m-%d") + " " + \
                    str(ASK_MAX) + " " + \
                    str(ASK_MIN) + " " + \
                    str(ASK_AVG) + " " + \
                    str(DIF) + "\n"
            return cursor, s
        except Exception as ex:
            print(ex)


# dat = DataHandler("localhost", "Dimas", "Dimas", "Forex")
# dat.GetReport()