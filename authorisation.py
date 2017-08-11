from views import *
import requests
from requests.auth import HTTPBasicAuth
from tkinter import *


SITE = "https://api.triptogether.com/identity"
s = requests.session()


def authorizeOnSite(output, login, password):
    output.insert(END, "\n==============================================")
    output.insert(END, "Authorising at " + SITE + "...")
    r = 0
    if login.get() == "" or password.get() == "":
        output.insert(END, "You forgot your login or password!")

    try:
        r = s.get(SITE, auth=HTTPBasicAuth(login.get(), password.get()))
    except ConnectionError or TimeoutError:
        output.insert(END, "Looks like their server is down, but just in case, try checking your wi-fi ;)")

    if r.status_code == 200:
        output.insert(END, "\nInfiltration successful! xD")
    else:
        if r.status_code == 404:
            output.insert(END, "Error code: " + r.status_code.__str__())
            output.insert(END, "Error connecting to site. Try later... ")
        else:
            output.insert(END, "Something went wrong :(")
            output.insert(END, "Error code: " + r.status_code.__str__())
            output.insert(END, "Try to check your login info and try again...")

    return r