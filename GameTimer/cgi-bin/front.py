import cgi
import os.path
import pickle

from modulus.CommonDoc import MyDoc
from sqlcommandsnew import sqlcommands

test = sqlcommands()

skin = "cgi-bin/forms/f_front.html"

def MakeForm():
    global skin
    form = ""
    with open(skin) as f:
        lines = f.readlines()
        form = form.join(lines[0:])
    print(form)

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

def MakeBtn(numeral):
    btn = f'''<button id='{numeral}' onclick="AxRemove('rep','{numeral}')">Delete</button>'''
    return btn

def MakeSelector(numeral):
    sel = f'''<div id='{numeral}' onclick="AxFetch('time','date','{numeral}')">{numeral}</div>'''
    return sel

def DelData(dat):
    test.Open()
    test.DelOne(dat)
    test.End()

def LoadOne(dat):
    ret, bet = test.GetOne(dat)
    return ret, bet

def LoadData():
    test.Open()
    test.NewTable()
    r = test.GetAll()
    bloom = "<br><p>"
    nochar = "!@,(){}[];' "
    for each in r:
        for char in nochar:
            each = str(each).replace(char,"")
        bloom = bloom + MakeSelector(str(each)) + str(MakeBtn(each)) + "</p><p>"
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

def SaveData(data):
    test.NewEntry(data)
    test.End()

def DoAjaxTime():
    res = test.GetAll()
    bloom = ""
    if res != []:
        for each in res:
            bloom = bloom + each
        return bloom
    else:
        return "nothing"
    

LoadData()

data = cgi.FieldStorage()
data = decode(data)
ztime = None
if not data:
    MyDoc.Do_Start()
    print("Welcome")
    print(LoadData())
elif "update" in data:
    print("Content-Type: text/html; charset=UTF-8\n")
    test.UpdateOne(data['update'], data['time'], data['oldday'], data['oldtime'])
    print(LoadData())
    test.End()
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
    print(MakeSelector(timein) + MakeBtn(str(data['timein'])) + '<br>')
    SaveData(timein)
    #print(DoAjaxTime())
    quit()



MakeForm()
MyDoc.Do_End()
