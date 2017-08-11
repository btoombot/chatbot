from tkinter import *
from tkinter import ttk
import tkinter as tk
from fileworker import *

# Some very dirty magic
window = Tk()

gen_var = StringVar()
trip_val = StringVar()
country_val = StringVar()
job_val = StringVar()
budget_val = StringVar()
all_budget_val = StringVar()

window.update()
window.destroy()

def on_closing(window):
    window.grab_release()


def add(listbox, value):
    if value.get() != "":
        listbox.insert(END, value.get())


def addTrip(listbox, value, addvalue):
    if value.get() != "":
        listbox.insert(END, value.get() + " | " + addvalue.get())


def remove(listbox):
    try:
        listbox.delete(listbox.curselection())
    except:
        pass


def create_window(window):
    prefframe = ttk.Frame(window, name="prefs", padding="3 3 12 12")
    prefframe.grid(column=0, row=0, sticky=(N, W, E, S))
    prefframe.columnconfigure(0, weight=1)
    prefframe.rowconfigure(0, weight=1)

    ttk.Label(prefframe, text="Gender: ").grid(column=1, row=1, sticky=W)
    gender = ttk.Combobox(prefframe, name="gender", textvariable=gen_var, state="readonly", width=10)
    gender['values'] = ('male', 'female')
    gender.current(0)
    gender.grid(column=2, row=1, sticky=W)

    try:
        gender.current(gender['values'].index(getGender()))
    except ValueError:
        pass


    chk_prem = IntVar(prefframe)
    only_prem = ttk.Checkbutton(prefframe, name="chk_prem", text="premium only", variable=chk_prem)
    only_prem.grid(column=3, row=1, sticky=(W, N))
    try:
        chk_prem.set(int(getPremOnly()))
    except:
        pass

    ttk.Label(prefframe, text="Age from/to: ").grid(column=1, row=2, sticky=W)
    age = Spinbox(prefframe, name="age", from_=18, to=99, width=10)
    age.grid(column=2, row=2, sticky=(W, E))
    age.delete(0, END)
    age.insert(0, getAgeFrom())

    ageTo = Spinbox(prefframe, name="ageTo", from_=19, to=100, width=10)
    ageTo.grid(column=3, row=2, sticky=(W, E))
    ageTo.delete(0, END)
    try:
        ageTo.insert(0, getAgeTo())
    except:
        ageTo.insert(0, 100)
        pass

    ttk.Label(prefframe, text="Include ppl that has no: ").grid(column=1, row=3, sticky=W)

    chk_nocountry = IntVar(prefframe)
    no_country = ttk.Checkbutton(prefframe, name="chk_nocountry", text="countries", variable=chk_nocountry)
    no_country.grid(column=2, row=3, sticky=(W, N))
    try:
        chk_nocountry.set(int(getNoCountryCb()))
    except:
        chk_nocountry.set(1)
        pass

    chk_nojob = IntVar(prefframe)
    no_jobs = ttk.Checkbutton(prefframe, name="chk_nojob", text="jobs", variable=chk_nojob)
    no_jobs.grid(column=3, row=3, sticky=(W, N))
    try:
        chk_nojob.set(int(getNoJobCb()))
    except:
        chk_nojob.set(1)
        pass

    chk_notrip = IntVar(prefframe)
    no_trips = ttk.Checkbutton(prefframe, name="chk_notrip", text="trips", variable=chk_notrip)
    no_trips.grid(column=4, row=3, sticky=(W, N))
    try:
        chk_notrip.set(int(getNoTripCb()))
    except:
        chk_notrip.set(1)
        pass
# Budget =====================

    ttk.Label(prefframe, text="All budgets higher than (or equal): ").grid(column=1, row=4, sticky=(W, N))
    all_budget = ttk.Combobox(prefframe, name="all_budget", textvariable=all_budget_val, state="readonly", width=10)
    all_budget['values'] = ('low', 'medium', 'high', 'very-high')
    all_budget.current(0)
    all_budget.grid(column=2, row=4, sticky=(W, N))

    try:
        all_budget.current(all_budget['values'].index(getBudget()))
    except:
        pass

    chk_any = IntVar(prefframe)
    any_budget = ttk.Checkbutton(prefframe, name="chk_any", text="+ no budget", variable=chk_any, onvalue=1, offvalue=0)
    any_budget.grid(column=3, row=4, sticky=(W, N))
    try:
        chk_any.set(int(getAnyBudgetCb()))
    except:
        pass

# Lists =====================

    ttk.Label(prefframe, text="Exclude countries(born at):").grid(column=1, row=6, sticky=W)

    frame_contry = ttk.Frame(prefframe, name="frame_country")

    sbar_country = Scrollbar(frame_contry)
    sbar_country.pack(side=RIGHT, fill=Y)

    pobirth = Listbox(frame_contry, name="pobirth", height=5)
    pobirth.pack()

    sbar_country.config(command=pobirth.yview)
    pobirth.config(yscrollcommand=sbar_country.set)

    frame_contry.grid(column=3, row=7, rowspan=2, columnspan=2, sticky=(W, E))

    try:
        loaded_pobirth = getBirth()
        for item in loaded_pobirth:
            pobirth.insert(END, item)
    except:
        pass

    textbox = ttk.Entry(prefframe, width=20, textvariable=country_val)
    textbox.grid(column=1, columnspan=1, row=7, sticky=(W, E, N))

    ttk.Button(prefframe, text=">>>", command=lambda: add(pobirth, textbox)).grid(column=2, row=7, sticky=(W, S))
    ttk.Button(prefframe, text="<<<", command=lambda: remove(pobirth)).grid(column=2, row=8, sticky=(W, N))

    ttk.Label(prefframe, text="Include jobs:").grid(column=1, row=9, sticky=W)

    frame_job = ttk.Frame(prefframe, name="frame_job")

    sbar_job = Scrollbar(frame_job)
    sbar_job.pack(side=RIGHT, fill=Y)

    jobs = Listbox(frame_job, name="jobs", height=5)
    jobs.pack()

    sbar_job.config(command=jobs.yview)
    jobs.config(yscrollcommand=sbar_job.set)

    frame_job.grid(column=3, row=10, rowspan=2, columnspan=2, sticky=(W, E))

    try:
        loaded_jobs = getJobs()
        for item in loaded_jobs:
            jobs.insert(END, item)
    except:
        pass
    textboxJ = ttk.Entry(prefframe, width=20, textvariable=job_val)
    textboxJ.grid(column=1, columnspan=1, row=10, sticky=(W, E, N))

    ttk.Button(prefframe, text=">>>", command=lambda: add(jobs, textboxJ)).grid(column=2, row=10, sticky=(E, S))
    ttk.Button(prefframe, text="<<<", command=lambda: remove(jobs)).grid(column=2, row=11, sticky=(E, N))

    ttk.Label(prefframe, text="Travel destinations & budget:").grid(column=1, row=12, sticky=W)

    frame_trip = ttk.Frame(prefframe, name="frame_trip")

    sbar_trip = Scrollbar(frame_trip)
    sbar_trip.pack(side=RIGHT, fill=Y)

    travelList = Listbox(frame_trip, name="travelList", height=5)
    travelList.pack()

    sbar_trip.config(command=travelList.yview)
    travelList.config(yscrollcommand=sbar_trip.set)

    frame_trip.grid(column=3, row=13, columnspan=2, rowspan=2, sticky=(W, E))

    try:
        loaded_travelList = getTrips()
        for item in loaded_travelList:
            travelList.insert(END, item)
    except:
        pass

    tripbox = ttk.Entry(prefframe, width=20, textvariable=trip_val)
    tripbox.grid(column=1, row=13, sticky=(W, E, N))

    ttk.Label(prefframe, text="Budget for trip: ").grid(column=1, row=14, sticky=(N, W))
    budget = ttk.Combobox(prefframe, name="budget", textvariable=budget_val, state="readonly", width=10)
    budget['values'] = ('', 'low', 'medium', 'high', 'very-high')
    budget.current(0)
    budget.grid(column=1, row=14, sticky=(N, E))

    ttk.Button(prefframe, text=">>>", command=lambda: addTrip(travelList, tripbox, budget)).grid(column=2, row=13, sticky=(S, E))
    ttk.Button(prefframe, text="<<<", command=lambda: remove(travelList)).grid(column=2, row=14, sticky=(N, E))

    for child in prefframe.winfo_children():
        child.grid_configure(padx=5, pady=5)
