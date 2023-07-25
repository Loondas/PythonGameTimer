import sqlite3

class sqlcommands:
    

    def Open(self):
        if self.bOpen is False:
            self.conn = sqlite3.connect(self.db)
            self.curs = self.conn.cursor()
            self.bOpen = True
        return True

    def __init__(self):
        self.db = './~sqlcommandsnew.sqlt3'
        self.conn = None
        self.curs = None
        self.bOpen = False
        self.fields = [('entry', 'DateTime'),('number', 'Text',)]
        self.table_name = 'chronos'

    def NewTable(self):
        sqlCommand = """CREATE TABLE if not EXISTS chronos (
        number TEXT PRIMARY KEY,
        entry TEXT);"""
        self.curs.execute(sqlCommand)

    def NewEntry(self, field):
        if self.bOpen:
            self.curs.execute("INSERT INTO chronos (entry, number) VALUES (date('now', 'localtime'), '" + field + "');")
            self.conn.commit()
            return True
        return False

    def FillTable(self, fields):
        if self.bOpen:
            self.curs.execute("INSERT INTO chronos (entry, number) VALUES (date('now', 'localtime'),?);", [fields])
            return True
        return False

    def GetAll(self):
        self.curs.execute("SELECT number FROM chronos")
        ans = self.curs.fetchall()
    ##    for i in ans:
    ##        print(i)
        return ans

    def GetSome(self, count):
        self.curs.execute("SELECT * FROM chronos ORDER BY entry LIMIT 5 OFFSET %s" % count)
        ans = self.curs.fetchall()
        return ans

    def GetPrimary(self):
        self.curs.execute("SELECT number FROM chronos")
        ans = self.curs.fetchall()
        return ans

    def CountEntry(self):
        self.curs.execute("SELECT COUNT(entry) FROM chronos")
        ans = self.curs.fetchone()
        return ans

    def DelTable(self):
        if self.bOpen:
            self.curs.execute("DrOp TaBLe IF EXISTS chronos;")
            return True
        return False

    def GetOne(self, number):
        if self.bOpen:
            self.curs.execute("Select entry from chronos where number = '" + number + "';")
            Lalist = self.curs.fetchone()
            self.curs.execute("Select number from chronos where number = '" + number + "';")
            Lelist = self.curs.fetchone()
            return Lalist, Lelist
##            for ref in zlist:
##                yield ref #Must itterate throught the yield
        return None
    
    def DelEm(self, numbers):
        if self.bOpen:
            if len(numbers) != 0:
                self.curs.execute("DELETE from chronos where " + " or ".join(("number = " + str(n) for n in numbers)))
                self.conn.commit()
                return True
        return False

    def UpdateOne(self, new, time, oldday, oldtime):
        if self.bOpen:
            self.curs.execute("UPDATE chronos SET entry = '" + new + "', number = '" + time + "' WHERE number = '" + oldday + "' and entry = '" + oldtime + "';")
            self.conn.commit()
            return True
        return False

    def DelOne(self, number):
        if self.bOpen:
            self.curs.execute("DELETE from chronos where number = '" + number + "';")
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


    
