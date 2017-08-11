from views import *
import requests
from requests.auth import HTTPBasicAuth
from tkinter import *
from time import sleep


SITE = "https://api.triptogether.com/identity"
s = requests.session()


def authorizeOnSite(output, login, password):
    output.insert(END, "\n==============================================")
    output.insert(END, "Authorising at " + SITE + "...")
    r = None
    if login.get() == "" or password.get() == "":
        output.insert(END, "Duh... You forgot your login or password!")

    while r is None:
        try:
            r = s.get(SITE, auth=HTTPBasicAuth(login.get(), password.get()))
        except:
            output.insert(END, "Something went wrong...")
            sleep(20)

        if r and r.status_code == 200:
            output.insert(END, "\nInfiltration successful!")
        else:
            output.insert(END, "\nRetrying...")
    return r