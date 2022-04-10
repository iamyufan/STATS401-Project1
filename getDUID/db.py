import pymysql

class duke:
    def __init__(self) -> None:
        self.db = pymysql.connect(
            host = "",
            user = "",
            password = "",
            database="")
        self.cursor = self.db.cursor()
        
    def insert(self, data):
        sql = "update duke set id = %s where name =%s"
        self.cursor.execute(sql, (data[1], data[0]))
        self.db.commit()
        
    def readLst(self):
        sql = "select name from duke where id is null"
        self.cursor.execute(sql)
        return self.cursor.fetchall()