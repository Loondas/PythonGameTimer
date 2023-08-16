import sqlite3

class sqlcommands:
    

    def Open(self):
        if self.bOpen is False:
            self.conn = sqlite3.connect(self.db)
            self.curs = self.conn.cursor()
            self.bOpen = True
        return True

    def __init__(self, table):
        self.db = './~newsqlcommands.sqlt3'
        self.conn = None
        self.curs = None
        self.bOpen = False
        self.fields = None
        self.table_name = table

    def CreateTable(self):
        sqlCommand = f"""CREATE TABLE if not EXISTS {self.table_name} (
        TimeIn TEXT PRIMARY KEY,
        DateIn TEXT,
        TimeOut TEXT,
        DateOut TEXT);"""
        self.curs.execute(sqlCommand)

    def NewIn(self, field):
        if self.bOpen:
            self.curs.execute(f"INSERT INTO {self.table_name} (DateIn, TimeIn) VALUES (date('now', 'localtime'), '{field}');")
            self.conn.commit()
            self.fields = field
            return True
        return False
    
    def NewOut(self, field):
        if self.bOpen:
            self.curs.execute(f"UPDATE {self.table_name} SET DateOut = date('now', 'localtime'), TimeOut = '{field}' WHERE TimeIn = '{self.fields}';")
            self.conn.commit()
            return True
        return False

    def GetAll(self):
        self.curs.execute("SELECT TimeIn, TimeOut FROM " + self.table_name + ";")
        ans = self.curs.fetchall()
    ##    for i in ans:
    ##        print(i)
        return ans

    def GetLast(self):
        self.curs.execute(f"SELECT TimeIn FROM {self.table_name} WHERE ROWID IN ( SELECT max( ROWID ) FROM {self.table_name});")
        nochar = "!@,(){}[]' "
        naked = ""
        self.fields = self.curs.fetchone()
        for each in self.fields:
            for char in nochar:
                each = str(each).replace(char,"")
            naked = naked + each
        self.fields = naked
        return self.fields

    def GetSome(self, count):
        self.curs.execute("SELECT * FROM " + self.table_name + " ORDER BY DateIn LIMIT 5 OFFSET %s" % count + ";")
        ans = self.curs.fetchall()
        return ans

    def GetPrimary(self):
        self.curs.execute("SELECT TimeIn FROM " + self.table_name + ";")
        ans = self.curs.fetchall()
        return ans

    def CountDateIn(self):
        self.curs.execute("SELECT COUNT(DateIn) FROM " + self.table_name + ";")
        ans = self.curs.fetchone()
        return ans

    def DelTable(self):
        if self.bOpen:
            self.curs.execute("DROP TABLE IF EXISTS " + self.table_name + ";")
            return True
        return False

    def GetOne(self, TimeIn):
        if self.bOpen:
            self.curs.execute("Select DateIn from " + self.table_name + " where TimeIn = '" + TimeIn + "';")
            Lalist = self.curs.fetchone()
            self.curs.execute("Select TimeIn from " + self.table_name + " where TimeIn = '" + TimeIn + "';")
            Lelist = self.curs.fetchone()
            return Lelist, Lalist
##            for ref in zlist:
##                yield ref #Must itterate throught the yield
        return None
    
    def DelEm(self, TimeIns):
        if self.bOpen:
            if len(TimeIns) != 0:
                self.curs.execute("DELETE from " + self.table_name + " where " + " or ".join(("TimeIn = " + str(n) for n in TimeIns)))
                self.conn.commit()
                return True
        return False

    def UpdateOne(self, new, time, oldday, oldtime):
        if self.bOpen:
            self.curs.execute("UPDATE " + self.table_name + " SET DateIn = '" + new + "', TimeIn = '" + time + "' WHERE TimeIn = '" + oldday + "' and DateIn = '" + oldtime + "';")
            self.conn.commit()
            return True
        return False

    def DelOne(self, TimeIn):
        if self.bOpen:
            self.curs.execute("DELETE from " + self.table_name + " where TimeIn = '" + TimeIn + "';")
            return True
        return False

    def End(self):
        if self.bOpen:
            self.conn.commit()
            self.bOpen = False
        return True

        @staticmethod
        def Import(dao, encoding=None, text_file='Employees.csv', hasHeader=True, sep='|'):
            try:
                # dao.open()
                with open(text_file, encoding=encoding) as fh:
                    line = fh.readline().strip()
                    if hasHeader is True:
                        line = fh.readline().strip()
                    while len(line) is not 0:
                        if dao.insert(line.split(sep)) is False:
                            return False
                        line = fh.readline().strip()
                # dao.close()
                return True
            except:
                pass
            return False


    
