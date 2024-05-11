import sqlite3

class DB:
    def __init__(self):
        self.id = 0
        self.dbname = ("eldb.db")
        self.conn = sqlite3.connect(self.dbname, isolation_level=None)
        self.ResetDB()#test用
        self.cursor = self.conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS text(id, name, text)"""
        self.cursor.execute(sql)
        self.conn.commit()
    def InsertDB(self,datas):#data:=[(),(),()]
        sql = """INSERT INTO text VALUES(?, ?, ?)"""
        for data in datas:
            data.insert(0,self.id)
            self.cursor.execute(sql, tuple(data))
            self.conn.commit()
            self.id += 1

    def FetchDB(self):
        sql = """SELECT * FROM text"""#条件を変える
        self.cursor.execute(sql)
        return self.cursor.fetchall()

            
    def DeleteDB(self):
        sql = """delete from test where id=?', ({},)""".format(id) #idと一致するものを消す。
        self.conn.execute(sql)
        self.conn.commit()
        self.id += 1
    
    def RenameDB(self,id,name):
        sql = """UPDATE text SET name = "{}" WHERE id = {};""".format(name,id)
        self.conn.execute(sql) 
        self.conn.commit()

    def ResetDB(self):
        sql = """DROP TABLE if exists text""" 
        self.conn.execute(sql)
        self.conn.commit()


    def CloseDB(self):
        self.conn.close()

db = DB()
db.InsertDB(
    [["test0","fsdjfasdfsadfas"],
    ["test1","sdfjasdfj;askldfjas"],
    ["test3","ffs24314312412354325"]]
)
db.RenameDB(1,"text33333")
print(db.FetchDB())