import cgi
import os.path
import pickle

from modulus.CommonDoc import MyDoc
from sqlcommandsnew import sqlcommands

TableIn = sqlcommands('TableIn')
TableOut = sqlcommands('TableOut')

skin = "cgi-bin/forms/f_front.html"

def MakeForm():
    global skin
    form = ""
    with open(skin) as f:
        lines = f.readlines()
        form = form.join(lines[0:])
    print(form)

def MakeTableHead():
    head = "<tr><th>Time In</th><th>Time Out</th></tr>"
    return head

def decode(data):
    if isinstance(data, dict):
        return data
    zsave = dict()
    if not data:
        return zsave
    for key in data:
        ukey = key
        uval = data[key].value
        zsave[ukey] = uval
    return zsave

def MakeBtn(numeral, inout):
    btn = f'''<button id='{numeral}' inout='{inout}' onclick="AxRemove('{numeral}', '{inout}')">Delete</button>'''
    return btn

def MakeSelector(numeral, inout):
    sel = f'''<div id='{numeral}' inout='{inout}' onclick="AxFetch('time','date','{numeral}')">{numeral}</div>'''
    return sel

def DelData(dat, table):
    table.Open()
    table.DelOne(dat)
    table.End()

def LoadOne(dat, table):
    ret, bet = table.GetOne(dat)
    return ret, bet

def LoadData():
    TableIn.Open()
    TableOut.Open()
    TableIn.CreateTable()
    TableOut.CreateTable()
    tableinfo = CreateFormattedTable()
    return tableinfo

def CreateFormattedTable():
    recordsIn = TableIn.GetAll()
    recordsOut = TableOut.GetAll()
    bloom = MakeTableHead()
    noChar = "!@,(){}[];' "
    for each, out in zip(recordsIn, recordsOut):
        for char in noChar:
            each = str(each).replace(char,"")
            out = str(out).replace(char,"")
        bloom = bloom + f"<tr><td id='{each}'>" + MakeSelector(str(each), "TableIn") + str(MakeBtn(each, 'TableIn')) + "</td>"
        bloom = bloom + f"<td id='{out}'>" + MakeSelector(str(out), "TableOut") + str(MakeBtn(out, 'TableOut') + "</td></tr>")
    return bloom

    #Create new alternating list for load
    listIn
    pairing = []
    

def StripData(clothed):
    clothed = str(clothed)
    nochar = "!@,(){}[]' "
    naked = ""
    for each in clothed:
        for char in nochar:
            each = str(each).replace(char,"")
        naked = naked + each
    return naked

def SaveData(data, table):
    table.NewEntry(data)
    table.End()

#def DoAjaxTime():
 #   res = TableIn.GetAll()
 #   bloom = ""
 #   if res != []:
 #       for each in res:
 #           bloom = bloom + each
 #       return bloom
 #   else:
 #       return "nothing"
    

LoadData()

data = cgi.FieldStorage()
data = decode(data)
ztime = None
currentTable = TableIn

if not data:
    MyDoc.Do_Start()
    #print("Welcome")
    print(LoadData())
if "table" in data:
    currentTable = eval(data['table'])
    if "update" in data:
        print("Content-Type: text/html; charset=UTF-8\n")
        currentTable.UpdateOne(data['update'], data['time'], data['oldday'], data['oldtime'])
        print(LoadData())
        currentTable.End()
        quit()
    elif "delete" in data:
        print("Content-Type: text/html; charset=UTF-8\n")
        DelData(data['delete'], currentTable)
        print(LoadData())
        quit()
    elif "fetch" in data:
        print("Content-Type: text/html; charset=UTF-8\n")
        ret, bet = currentTable.LoadOne(data['fetch'])
        ret = StripData(ret)
        bet = StripData(bet)
        print(ret + "|" + bet)
        quit()
    elif "timein" in data:
        print("Content-Type: text/html; charset=UTF-8\n")
        timein = StripData(data['timein'])
        SaveData(timein, currentTable)
        print(LoadData())
        #print(DoAjaxTime())

        quit()


MakeForm()
MyDoc.Do_End()
