import cgi
import os.path
import pickle

from modulus.CommonDoc import MyDoc

skin = "cgi-bin/forms/f_view.html"

def MakeForm():
    global skin
    form = ""
    with open(skin) as f:
        lines = f.readlines()
        form = form.join(lines[0:])
    print(form)

MyDoc.Do_Start()
MakeForm()
MyDoc.Do_End()
