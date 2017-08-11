# -*- coding: windows-1251 -*-

from tkinter import *
from tkinter import ttk
import tkinter as tk
from fileworker import save

class MsgWindow:
    msg_list = []

    def __init__(self, window):
        self.get_msgs()

        msgframe = ttk.Frame(window, padding="3 3 12 12")
        msgframe.grid(column=6, row=0, sticky=(N, W, E))
        msgframe.columnconfigure(0, weight=1)
        msgframe.rowconfigure(0, weight=1)

        ttk.Label(msgframe, text="Your text: ").grid(column=1, row=1, sticky=W)

        ttk.Label(msgframe, text="Tip: use {{name}} to paste victim's name in message ").grid(column=1, row=2, sticky=(W, N))

        ttk.Label(msgframe, text="Delay before your answer (sec): ").grid(column=1, row=3, sticky=(S, E))
        spin_sec = Spinbox(msgframe, name="spin_sec", from_=1, to=99999, width=10)
        spin_sec.grid(column=3, row=3, sticky=(S, W))
        spin_sec.bind('<FocusOut>', lambda event, spin=spin_sec: self.spin_chk(spin))
        spin_sec.delete(0, END)
        spin_sec.insert(0, self.get_delay())

        ttk.Label(msgframe, text="Timeout for chatting (min): ").grid(column=1, row=4, sticky=(S, E))
        spin_min = Spinbox(msgframe, name="spin_min", from_=1, to=99999, width=10)
        spin_min.grid(column=3, row=4, sticky=(S, W))
        spin_min.bind('<FocusOut>', lambda event, spin=spin_min: self.spin_chk(spin))
        spin_min.delete(0, END)
        spin_min.insert(0, self.get_timeout())

        #ttk.Label(msgframe, text="Amount of people to chat with synchronously: ").grid(column=1, row=5, sticky=(S, E))
        #spin_ppl = Spinbox(msgframe, name="spin_ppl", from_=1, to=99999, width=10)
        #spin_ppl.grid(column=3, row=5, sticky=(S, W))
        #spin_ppl.bind('<FocusOut>', lambda event, spin=spin_ppl: self.spin_chk(spin))
        #spin_ppl.delete(0, END)
        #spin_ppl.insert(0, self.get_threads())

        frame_your_msg = ttk.Frame(msgframe)

        sbar_msg = Scrollbar(frame_your_msg)
        sbar_msg.pack(side=RIGHT, fill=Y)

        your_msg = Text(frame_your_msg, height=10, width=30)
        your_msg.pack()

        sbar_msg.config(command=your_msg.yview)
        your_msg.config(yscrollcommand=sbar_msg.set)

        frame_your_msg.grid(column=1, row=2, columnspan=2, rowspan=2, sticky=(W, E))

        # Right

        frame_all_msgs = ttk.Frame(msgframe)

        sbar_all_msg = Scrollbar(frame_all_msgs)
        sbar_all_msg.pack(side=RIGHT, fill=Y)

        all_msgs = Listbox(frame_all_msgs, height=15, width=30)
        all_msgs.bind('<<ListboxSelect>>', lambda event, listbox=all_msgs, text=your_msg: self.on_select(listbox, text))
        all_msgs.pack()

        for item in self.msg_list:
            if item != "\n" and item != "":
                all_msgs.insert(END, item[:23] + "...")

        sbar_all_msg.config(command=all_msgs.yview)
        all_msgs.config(yscrollcommand=sbar_all_msg.set)

        frame_all_msgs.grid(column=4, row=2, columnspan=2, rowspan=2, sticky=(W, E))

        ttk.Button(msgframe, width=5, text="/\\", command=lambda: self.up(all_msgs)).grid(column=3, row=2, sticky=(N, E))
        ttk.Button(msgframe, width=5, text="\\/", command=lambda: self.down(all_msgs)).grid(column=3, row=2, sticky=E)

        ttk.Button(msgframe, text=">>>", command=lambda: self.add(all_msgs, your_msg)).grid(column=3, row=2, sticky=(S, E))
        ttk.Button(msgframe, text="<<<", command=lambda: self.remove(all_msgs)).grid(column=3, row=3, sticky=(N, E))

        ttk.Label(msgframe, text="All your messages: ").grid(column=4, row=1, sticky=W)

        ttk.Button(msgframe, text="Reset history", command=lambda: self.purge_history()).grid(column=1, row=7, rowspan=2,
                                                                                  sticky=(N, E, S))
        ttk.Label(msgframe, text="Tip: removes users, who didn't reply").grid(column=2, row=7,  columnspan=3, sticky=(S, E))

        ttk.Button(msgframe, text="Exit", command=lambda: window.destroy()).grid(column=1, row=9, rowspan=2,
                                                                                  sticky=(W, N, E, S))
        ttk.Button(msgframe, text="Save", command=lambda: self.save(window, spin_sec, spin_min)).grid(column=3, columnspan=3, row=9, rowspan=2, sticky=(W, N, E, S))


        for child in msgframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def purge_history(self):
        try:
            f = open("configs\\history.dak", "w")
            f2 = open("configs\\fetched_ids.dak", "r")
            for line in f2.readlines():
                f.write(line)
            f.close()
        except FileNotFoundError:
            pass

    def on_closing(self, root):
        root.grab_release()

    def add(self, listbox, value):
        if value.get("1.0", END) != "\n":
            listbox.insert(END, value.get("1.0", "1.23") + "...")
            self.msg_list.append(value.get("1.0", END))
            value.delete("1.0", END)

    def remove(self, listbox):
        index = listbox.curselection()[0]
        self.msg_list = self.msg_list[:index] + self.msg_list[index + 1:]
        listbox.delete(listbox.curselection())

    def up(self, listbox):
        currIndex = listbox.curselection()[0]
        if currIndex != 0:
            self.msg_list[currIndex-1], self.msg_list[currIndex] = self.msg_list[currIndex], self.msg_list[currIndex-1]

            tmp = listbox.get(currIndex)
            listbox.delete(currIndex)
            listbox.insert(currIndex-1, tmp)
        listbox.select_set(currIndex-1)

    def down(self, listbox):
        currIndex = listbox.curselection()[0]
        if currIndex != listbox.size()-1:
            self.msg_list[currIndex], self.msg_list[currIndex+1] = self.msg_list[currIndex+1], self.msg_list[currIndex]

            tmp = listbox.get(currIndex)
            listbox.delete(currIndex)
            listbox.insert(currIndex + 1, tmp)
        listbox.select_set(currIndex+1)

    def on_select(self, listbox, textarea):
        textarea.delete("1.0", END)
        textarea.insert("1.0", self.msg_list[listbox.curselection()[0]])

    def save(self, window, spin, spin2, ):
        try:
            f = open("configs\\messages.dak", "w")
            for item in self.msg_list:
                f.write("Message: " + item)
            f.write("Delay: " + spin.get().__str__())
            f.write("\nTimeout: " + spin2.get().__str__())
            #f.write("\nThreads: " + spin3.get().__str__())
            f.close()
            save_all(window)
        finally:
            window.destroy()

    def get_msgs(self):
        self.msg_list.clear()
        try:
            f = open("configs\\messages.dak", "r")
            stri = ""

            for line in f.readlines():
                if line.__contains__("Message: ") or line.__contains__("Delay: "):
                   self.msg_list.append(stri)
                   stri = line.replace("Message: ", "")
                else:
                    stri = stri + line

            #self.msg_list.append(stri)
            self.msg_list = self.msg_list[1:]
            f.close()
        except FileNotFoundError:
            pass

    def get_timeout(self):
        try:
            f = open("configs\\messages.dak", "r")
            for line in f.readlines():
                if line.__contains__("Timeout: ") == True:
                    f.close()
                    return line.replace("\n", "").split(": ")[1].__str__()
            f.close()
            return 1
        except FileNotFoundError as err:
            return 0

    def get_delay(self):
        try:
            f = open("configs\\messages.dak", "r")
            for line in f.readlines():
                if line.__contains__("Delay: ") == True:
                    f.close()
                    return line.replace("\n", "").split(": ")[1].__str__()
            f.close()
            return 1
        except FileNotFoundError as err:
            return 1

    def get_threads(self):
        try:
            f = open("configs\\messages.dak", "r")
            for line in f.readlines():
                if line.__contains__("Threads: ") == True:
                    f.close()
                    return line.replace("\n", "").split(": ")[1].__str__()
            f.close()
            return 1
        except FileNotFoundError as err:
            return 1


    def spin_chk(self, spin):
        try:
            if int(spin.get()) > 99999:
                spin.delete(0, END)
                spin.insert(0, "99999")
            if int(spin.get()) < 1:
                spin.delete(0, END)
                spin.insert(0, "1")
        except:
            spin.delete(0, END)
            spin.insert(0, "1")
            pass


def save_all(window):
    for item in window.winfo_children():

        if item._name.__str__() == "prefs":
            gender = None
            age = None
            ageTo = None
            pobirth = None
            jobs = None
            travelList = None
            all_budget = None
            chk_prem = None
            chk_nojob = None
            chk_notrip = None
            chk_nocountry = None
            chk_any = None
            for subitem in item.winfo_children():
                if str(subitem._name) == 'gender':
                    gender = subitem
                elif str(subitem._name) == 'age':
                    age = subitem
                elif str(subitem._name) == 'ageTo':
                    ageTo = subitem
                elif str(subitem._name) == 'all_budget':
                    all_budget = subitem
                elif str(subitem._name) == 'chk_any':
                    chk_any = subitem
                elif str(subitem._name) == 'chk_nocountry':
                    chk_nocountry = subitem
                elif str(subitem._name) == 'chk_nojob':
                    chk_nojob = subitem
                elif str(subitem._name) == 'chk_notrip':
                    chk_notrip = subitem
                elif str(subitem._name) == 'chk_prem':
                    chk_prem = subitem
                elif str(subitem._name) == "frame_country":
                    for subsubitem in subitem.winfo_children():
                        if subsubitem._name == "pobirth":
                            pobirth = subsubitem
                elif str(subitem._name) == 'frame_job':
                    for subsubitem in subitem.winfo_children():
                        if subsubitem._name == "jobs":
                            jobs = subsubitem
                elif str(subitem._name) == 'frame_trip':
                    for subsubitem in subitem.winfo_children():
                        if subsubitem._name == "travelList":
                            travelList = subsubitem
            save(window, gender, age, ageTo, pobirth, jobs, travelList, all_budget, chk_any, chk_nocountry, chk_nojob,
                 chk_notrip, chk_prem)