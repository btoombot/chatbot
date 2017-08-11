import requests
import time
import json
import pycountry
import os
from tkinter import *
from tkinter import ttk
from fileworker import getPath

def read_old_msg(output, auth):

    save_path = getPath()
    token = int(time.time())
    #time.sleep(1800)
    sender_info = json.JSONDecoder().decode(auth.text)
    header = {'authorization': "Token token=\"" + auth.headers['X-Token'] + "\""}

    email = None
    m_sender = None
    pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    pattern2 = re.compile("(^[a-zA-Z0-9_.+-]+ [a-zA-Z0-9-] +\.[a-zA-Z0-9-.]+$)")

    while True:
        try:
            response = requests.get(
                "https://api.triptogether.com/events/" + sender_info['id'] + "?token=" + token.__str__(),
                headers=header)
        except ConnectionError as err:
            output.insert(END, "!!! " + err.__str__())
            pass

        if response.text != "[]" and response:
            message = json.JSONDecoder().decode(response.text)
            for item in message:
                try:
                    if item['type'] == "added:event":
                        if 'details' in item:
                            if 'payload' in item['details']:
                                if 'text' in item['details']['payload']:
                                    t_item = item['details']['payload']['text']
                                    if t_item.split(" ").__len__() > 1:
                                        t_item = t_item.split(" ")

                                    if type(t_item) is list:
                                        for word in t_item:
                                            if pattern.match(word) or pattern2.match(word):
                                                email = word
                                                m_sender = item['details']['payload']['sender-id']
                                    else:
                                        if pattern.match(t_item) or pattern2.match(t_item):
                                            email = t_item
                                            m_sender = item['details']['payload']['sender-id']

                    token = message[0]['token']
                    break
                except:
                    m_sender = ""
                    pass
        else:
            m_sender = ""

        info = None
        try:
            info = requests.get('https://api.triptogether.com/users/' + m_sender)
            info = json.JSONDecoder().decode(info.text)
        except:
            pass

        if email and info:
            output.insert(END, "Reader successfully fetched an e-mail from " + info['name'] + "(" + m_sender + ")")
            path = save_path.replace("\n", "") + "\\fetched_emails\\" + info['name'] + info['id'] + "\\"
            if os.path.isfile(path + info['name'] + info['id'] + ".txt") is False:
                os.makedirs(os.path.dirname(path + info['name'] + info['id'] + ".txt"))

            f = open(path + info['name'] + info['id'] + ".txt", "w")
            f.write("mail: " + email + "\n")

            if 'name' in info:
                f.write("name: " + info['name'] + "\n")

            if 'id' in info:
                f.write("page: www.triptogether.com/travellers/#" + info['id'] + "\n")

            if 'gender' in info:
                if info['gender'] == "mal":
                    f.write("gender: male\n")
                else:
                    if info['gender'] == "fem":
                        f.write("gender: female\n")
                    else:
                        f.write("gender: -bender\n")

            if 'birthday' in info:
                f.write("birthday: " + info['birthday'] + "\n")

            if 'country' in info:
                f.write("country: " + pycountry.countries.get(alpha_2=info['country']).name + "\n")

            if 'occupation' in info:
                f.write("job: " + info['occupation'] + "\n")

            f.close()
            img = None
            try:
                img = requests.get("https://api.triptogether.com/users/" + info['id'] + "/photos", stream=True)
            except:
                pass
            if img:
                img_list = json.JSONDecoder().decode(img.text)
                for item in img_list:
                    try:
                        r = requests.get(
                            "https://api7.triptogether.com/users/" + info['id'] + "/photos/" + item + ".310x455")
                    except:
                        pass
                    with open(path + item + ".jpg", 'wb') as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
            email = None

            try:
                f = open("configs\\fetched_ids.dak", "a+")
                f.write("0" + info['id'] + "\n")
                f.close()

            except FileNotFoundError as err:
                print(err.__str__())
                pass

