import cgi
import os.path
import pickle

from modulus.CommonDoc import MyDoc
from newsqlcommands import sqlcommands

TimeTable = sqlcommands('TimeTable')

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

def DelData(dat):
    TimeTable.Open()
    TimeTable.DelOne(dat)
    TimeTable.End()

def LoadOne(dat):
    ret, bet = TimeTable.GetOne(dat)
    return ret, bet

def LoadData():
    TimeTable.Open()
    TimeTable.CreateTable()
    tableinfo = CreateFormattedTable()
    return tableinfo

def CreateFormattedTable():
    recordsIn = TimeTable.GetAll()
    bloom = MakeTableHead()
    noChar = "!@,(){}[];' "
    intertwining = [[enter, exit] for enter, exit in recordsIn]
    table = 'TableIn'
    for twin in intertwining:
        for each in twin:
            for char in noChar:
                each = str(each).replace(char,"")
            if table == 'TableIn':
                bloom = bloom + "<tr><td>" + MakeSelector(str(each), table) + '</td>'
                table = 'TableOut'
            else:
                bloom = bloom + "<td>" + MakeSelector(str(each), table)
                table = 'TableIn'
        bloom = bloom + str(MakeBtn(twin[0], table)) + '</td></tr>'
    return bloom

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
    if table == 'TableIn':
        TimeTable.NewIn(data)
        TimeTable.End()
    else:
        TimeTable.GetLast()
        TimeTable.NewOut(data)
        TimeTable.End()
    

LoadData()

data = cgi.FieldStorage()
data = decode(data)
ztime = None
currentTable = TimeTable

if not data:
    MyDoc.Do_Start()
    #print("Welcome")
    print(LoadData())
if "table" in data:
    currentTable = data['table']
    if "update" in data:
        print("Content-Type: text/html; charset=UTF-8\n")
        currentTable.UpdateOne(data['update'], data['time'], data['oldday'], data['oldtime'])
        print(LoadData())
        currentTable.End()
        quit()
    elif "delete" in data:
        print("Content-Type: text/html; charset=UTF-8\n")
        DelData(data['delete'])
        print(LoadData())
        quit()
    elif "fetch" in data:
        print("Content-Type: text/html; charset=UTF-8\n")
        ret, bet = LoadOne(data['fetch'])
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
