import pymysql

class MufiData:
    def __init__(self):
        self.__db = pymysql.connect(
            user='junghun9904', 
            passwd='kmk20216*', 
            host='127.0.0.1', 
            db='mufibooth', 
            charset='utf8'
        )
        self.__cursor = self.__db.cursor(pymysql.cursors.DictCursor)

    def insertdb(self, sql):
        check = self.__cursor.execute(sql)
        self.__db.commit()
        return check
    def selectdb(self, sql):
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()

mf = MufiData()
print(mf)
