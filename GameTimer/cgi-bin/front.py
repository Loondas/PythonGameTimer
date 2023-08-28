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
    sel = f'''<div id='{numeral}' inout='{inout}' onclick="AxFetch('time','date','{numeral}')"><div id='sel'>{numeral}</div></div>'''
    return sel

def DelData(dat):
    TimeTable.Open()
    TimeTable.DelOne(dat)
    TimeTable.End()

def LoadOne(dat, inout):
    ret, bet, const = TimeTable.GetOne(dat, inout)
    return ret, bet, const

def LoadData():
    TimeTable.Open()
    TimeTable.CreateTable()
    TimeInfo = CreateFormattedTable()
    return TimeInfo

def CreateFormattedTable():
    recordsIn = TimeTable.GetAll()
    bloom = MakeTableHead()
    noChar = "!@,(){}[];' "
    intertwining = [[enter, exit] for enter, exit in recordsIn]
    table = 'TimeIn'
    for twin in intertwining:
        for each in twin:
            for char in noChar:
                each = str(each).replace(char,"")
            if table == 'TimeIn':
                bloom = bloom + "<tr><td>" + MakeSelector(str(each), table) + '</td>'
                table = 'TimeOut'
            else:
                bloom = bloom + "<td>" + MakeSelector(str(each), table)
                table = 'TimeIn'
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
    if table == 'TimeIn':
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

if not data:
    MyDoc.Do_Start()
    print(LoadData())
if "table" in data:
    TableInOut = data['table']
    print("Content-Type: text/html; charset=UTF-8\n")
    if "update" in data:
        if data['oldtime'] == 'None':
            TimeTable.FillMissing(data['time'],data['update'], data['ifempty'])
        else:
            TimeTable.UpdateOne(data['update'], data['time'], data['oldday'], data['oldtime'], TableInOut)
        print(LoadData())
        TimeTable.End()
        quit()
    elif "delete" in data:
        DelData(data['delete'])
        print(LoadData())
        quit()
    elif "fetch" in data:
        ret, bet, const = LoadOne(data['fetch'], TableInOut)
        ret = StripData(ret)
        bet = StripData(bet)
        const = StripData(const)
        print(ret + "|" + bet + "|"+ const)
        quit()
    elif "timein" in data:
        timein = StripData(data['timein'])
        SaveData(timein, TableInOut)
        print(LoadData())
        #print(DoAjaxTime())

        quit()


MakeForm()
MyDoc.Do_End()
