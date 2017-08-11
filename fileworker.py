# -*- coding: windows-1251 -*-

from tkinter import *
import os

# Main ===============

def getPath():
    try:
        f = open("configs\\settings.dak", "r")
        for line in f.readlines():
            if line.__contains__("Data path: ") == True:
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()
        return os.getcwd()
    except FileNotFoundError as err:
        return os.getcwd()



def getLogin():
    try:
        f = open("configs\\settings.dak", "r")
        for line in f.readlines():
            if line.__contains__("Login: ") == True:
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()
            f.close()
        return ""
    except FileNotFoundError as err:
        return ""


def getPassword():
    try:
        f = open("configs\\settings.dak", "r")
        for line in f.readlines():
            if line.__contains__("Password: ") == True:
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()
            f.close()
        return ""
    except FileNotFoundError as err:
        return ""


def getSaveCb():
    try:
        f = open("configs\\settings.dak", "r")
        for line in f.readlines():
            if line.__contains__("Save: ") == True:
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()
        f.close()
        return ""
    except FileNotFoundError as err:
        return ""


# PageFetcher ===============


def save_id(ids):
    try:
        counter = 0
        f = open("configs\\history.dak", "a+")
        f2w = open("configs\\curr_victims.dak", "a+")
        for id in ids:
            id_in_list = False
            f.seek(0)
            for line in f.readlines():
                if line.__contains__(id) == True:
                    id_in_list = True

            if id_in_list is False:
                f.write("0"+id +"\n")
                f2w.write("0"+id +"\n")
                counter += 1
        f.close()
        f2w.close()
        return counter
    except FileNotFoundError as err:
        return 0


# Pref ===============


def getGender():
    try:
        f = open("configs\\prefs.dak", "r")
        for line in f.readlines():
            if line.__contains__("Gender: "):
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()
        f.close()
        return ""
    except FileNotFoundError as err:
        return ""


def getAgeFrom():
    try:
        f = open("configs\\prefs.dak", "r")
        for line in f.readlines():
            if line.__contains__("Age from: "):
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()
        f.close()
        return "18"
    except FileNotFoundError as err:
        return "18"


def getAgeTo():
    try:
        f = open("configs\\prefs.dak", "r")
        for line in f.readlines():
            if line.__contains__("Age to: "):
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()
        f.close()
        return "100"
    except FileNotFoundError as err:
        return "100"


def getBirth():
    try:
        f = open("configs\\prefs.dak", "r")
        for line in f.readlines():
            if line.__contains__("Lives in: "):
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()\
                    .replace("(", "")\
                    .replace('\',)', "\')")\
                    .replace(")", "")\
                    .replace('\'', "")\
                    .split(', ')
        f.close()
        return None
    except FileNotFoundError as err:
        return None


def getJobs():
    try:
        f = open("configs\\prefs.dak", "r")
        for line in f.readlines():
            if line.__contains__("Jobs: ") == True:
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()\
                    .replace("(", "")\
                    .replace('\',)', "\')")\
                    .replace(")", "")\
                    .replace('\'', "")\
                    .split(', ')
        f.close()
        return ""
    except FileNotFoundError as err:
        return ""


def getTrips():
    try:
        f = open("configs\\prefs.dak", "r")
        for line in f.readlines():
            if line.__contains__("Trips: "):
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()\
                    .replace("(", "")\
                    .replace('\',)', "\')")\
                    .replace(")", "")\
                    .replace('\'', "")\
                    .split(', ')
        f.close()
        return ""
    except FileNotFoundError as err:
        return ""


def getBudget():
    try:
        f = open("configs\\prefs.dak", "r")
        for line in f.readlines():
            if line.__contains__("Budget: ") == True:
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()
        f.close()
        return ""
    except FileNotFoundError as err:
        return ""


def getAnyBudgetCb():
    try:
        f = open("configs\\prefs.dak", "r")
        for line in f.readlines():
            if line.__contains__("No budget: "):
                f.close()
                return int(line.replace("\n", "").split(": ")[1].__str__())
        f.close()
        return 0
    except FileNotFoundError as err:
        return 1


def getNoTripCb():
    try:
        f = open("configs\\prefs.dak", "r")
        for line in f.readlines():
            if line.__contains__("No trip: "):
                f.close()
                return int(line.replace("\n", "").split(": ")[1].__str__())
        f.close()
        return 0
    except FileNotFoundError as err:
        return 1


def getNoJobCb():
    try:
        f = open("configs\\prefs.dak", "r")
        for line in f.readlines():
            if line.__contains__("No job: ") == True:
                f.close()
                return int(line.replace("\n", "").split(": ")[1].__str__())
        f.close()
        return 0
    except FileNotFoundError as err:
        return 1


def getNoCountryCb():
    try:
        f = open("configs\\prefs.dak", "r")
        for line in f.readlines():
            if line.__contains__("No country: ") == True:
                f.close()
                return int(line.replace("\n", "").split(": ")[1].__str__())
        f.close()
        return 0
    except FileNotFoundError as err:
        return 1


def getPremOnly():
    try:
        f = open("configs\\prefs.dak", "r")
        for line in f.readlines():
            if line.__contains__("Premium: "):
                f.close()
                return int(line.replace("\n", "").split(": ")[1].__str__())
        f.close()
        return 0
    except FileNotFoundError as err:
        return 0


def get_chk_value(chk):
    if chk.state().__str__() == "()":
        return 0
    else:
        return 1


def save(window, gender, ageFrom, ageTo, pobirth, jobs, travelList, all_budget, any_budget, no_job, no_country, no_trip, prem_only):
    try:
        f = open("configs\\prefs.dak", "w")
        if gender.get():
            f.write("\nGender: " + gender.get().__str__())
        if ageFrom.get():
            f.write("\nAge from: " + ageFrom.get().__str__())
        if ageTo.get():
            f.write("\nAge to: " + ageTo.get().__str__())
        if pobirth.get(0, END):
            f.write("\nLives in: " + pobirth.get(0, END).__str__())
        if jobs.get(0, END):
            f.write("\nJobs: " + jobs.get(0, END).__str__())
        if travelList.get(0, END):
            f.write("\nTrips: " + travelList.get(0, END).__str__())
        if all_budget.get():
            f.write("\nBudget: " + all_budget.get().__str__())

        if any_budget.state():
            f.write("\nNo budget: " + get_chk_value(any_budget).__str__())
        if no_job.state():
            f.write("\nNo country: " + get_chk_value(no_job).__str__())
        if no_country.state():
            f.write("\nNo job: " + get_chk_value(no_country).__str__())
        if no_trip.state():
            f.write("\nNo trip: " + get_chk_value(no_trip).__str__())
        if prem_only.state():
            f.write("\nPremium: " + get_chk_value(prem_only).__str__())
        f.close()
    finally:
        window.destroy()
