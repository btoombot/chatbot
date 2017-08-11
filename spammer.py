from views import *
import requests
from authorisation import authorizeOnSite
import threading
import time
from fileworker import getPath
import re
import pycountry
import os
import json
from tkinter import *
from tkinter import ttk

spam_thread_list = []
thread_list = []


def manage_threads(output, path):

    while 1:
        time.sleep(1)

        thread_is_active = False

        for thread in thread_list:
            if thread.isAlive():
                thread_is_active = True

        if thread_is_active is False:
            output.insert(END, "Bot done chatting. Check results at: " + path + "\\fetched_emails")
            thread_list.clear()
            spam_thread_list.clear()
            f = open("configs\\curr_victims.dak", "w")
            f.close()
            break



def save_soap(output, email, user):
    info = json.JSONDecoder().decode(user.text)
    path = getPath().replace("\n", "") + "\\fetched_emails\\" + info['name'] + "\\"
    if os.path.isfile(path + info['name'] + ".txt") is False:
        os.makedirs(os.path.dirname(path + info['name'] + ".txt"))

    f = open(path + info['name'] + ".txt", "w")
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

    try:
        img = requests.get("https://api.triptogether.com/users/" + info['id'] + "/photos", stream=True)
    except:
        pass
    if img:
        img_list = json.JSONDecoder().decode(img.text)
        for item in img_list:
            try:
                r = requests.get("https://api7.triptogether.com/users/" + info['id'] + "/photos/" + item + ".310x455")
            except:
                pass
            with open(path + item + ".jpg", 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)


def get_ids():
    try:
        f = open("configs\\curr_victims.dak", "r")      # <--------------------------------------CHANGE FILENAME HERE!
        id_list = []
        for line in f.readlines():
            if line[0] == "0":
                id_list.append(line.replace("\n", "")[1:])

        return id_list
    except FileNotFoundError as err:
        return []


def get_timeout():
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


def get_delay():
    try:
        f = open("configs\\messages.dak", "r")
        for line in f.readlines():
            if line.__contains__("Delay: ") == True:
                f.close()
                return line.replace("\n", "").split(": ")[1].__str__()
        f.close()
        return 1
    except FileNotFoundError as err:
        return 0


def get_msgs():
    try:
        f = open("configs\\messages.dak", "r")
        msg_list = []
        stri = ""

        for line in f.readlines():
            if line.__contains__("Message: ") or line.__contains__("Delay: "):
                msg_list.append(stri)
                stri = line.replace("Message: ", "")
            else:
                stri = stri + line

        # self.msg_list.append(str)
        f.close()
        return msg_list[1:]
    except FileNotFoundError as err:
        return []


def listen(header, recipient, your_id):
    response = None
    sender = []
    while response is None or sender == []:
        try:
            response = requests.get("https://api.triptogether.com/events/" + your_id + "?token=" + int(time.time()).__str__(), headers=header)
        except:
            pass

        if response.text != "[]":
            if response:
                print(response.text)
                sender = json.JSONDecoder().decode(response.text)[0]['details']['payload']['sender-id']

                if 'id'in sender:
                    if sender['id'] == recipient:
                        return response
                    else:
                        response = None
                        sender = []

        else:
            response = None
            sender = []

    return response


def send(recipient, auth, output, save_path, gotten_msg_lisg):
    token_list = []
    token = int(time.time())
    end_token = 0
    sender_info = json.JSONDecoder().decode(auth.text)

    email = None
    user = None

    exhists = True
    no_answer = False
    info = ""
    try:
        info = requests.get('https://api.triptogether.com/users/' + recipient)
    except:
        pass
    name = ""

    if info:
        name = json.JSONDecoder().decode(info.text)['name']
    else:
        output.insert(END, "Sorry, but user with ID " + recipient + " wasn't found.")
        exhists = False

    header = {'authorization': "Token token=\"" + auth.headers['X-Token'] + "\""}
    token_shadow = token
    for message_txt in gotten_msg_lisg:
        if exhists is False or no_answer:
            break

        payload = {'text': message_txt.replace("{{name}}", name), 'recipient': recipient, 'sender': sender_info['id']}

        try:
            rP = requests.post("https://api.triptogether.com/talks/" + sender_info['id'] + ":" + recipient, headers=header, data=payload)
            output.insert(END, "Message was send to user " + recipient.__str__() + " (" + name.__str__() + ")")
        except:
            output.insert(END, "Couldn't send message to user " + recipient.__str__() + " (" + name.__str__() + ")")
            output.insert(END, "Retrying...")
            time.sleep(10)
            continue

        message = None
    # <-------------------------------------- LISTENING
        m_sender = None
        m_reciver = None
        got_message = False

        timer_loc = 0
        limiter = 0


        token_list.append(token_shadow)
        while (limiter < int(get_timeout())*60) and timer_loc < int(get_delay()):
            start = time.time()
            print('token: ' + token_shadow.__str__())
            try:
                response = requests.get(
                    "https://api.triptogether.com/events/" + sender_info['id'] + "?token=" + token_shadow.__str__(),
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
                                    if 'sender-id' in item['details']['payload']:
                                        m_sender = item['details']['payload']['sender-id']
                                    else:
                                        m_sender = ""

                                    if 'recipient-id' in item['details']['payload']:
                                        m_reciver = item['details']['payload']['recipient-id']
                                    else:
                                        m_reciver = ""

                                    if m_sender == recipient:
                                        break
                    except:
                        m_sender = ""
                        m_reciver = ""
                        pass
            else:
                m_sender = ""
                m_reciver = ""

            if m_sender == recipient or (m_sender == sender_info['id'] and m_reciver == recipient) and timer_loc == 0:
                token_shadow = message[0]['token']

            end = time.time()

            if m_sender == recipient or timer_loc:
                print('!!!Timer: ' + timer_loc.__str__() + "| m_sender:" + m_sender)
                timer_loc += end - start

            if m_sender == recipient:
                if token_shadow not in token_list:
                    token_list.append(token_shadow)

            print('!!limiter: ' + limiter.__str__())
            limiter += end - start

            if gotten_msg_lisg.__len__() - 1 == gotten_msg_lisg.index(message_txt):
                limiter = 9999999

            if limiter > ((int(get_timeout())*60) - 5):
                no_answer = True

        if gotten_msg_lisg.__len__() - 1 == gotten_msg_lisg.index(message_txt) or no_answer:
            end_token = int(time.time()) + int(get_timeout())

    time.sleep(5)

    message_list = []
    text = []
#======================MAIL RiDing
    if end_token > token:
            for token in token_list:
                print("Reading token #: " + token.__str__())
                try:
                    response = requests.get(
                        "https://api.triptogether.com/events/" + sender_info['id'] + "?token=" + token.__str__(),
                        headers=header)
                except ConnectionError as err:
                    output.insert(END, "!!! " + err.__str__())
                    continue
                #token += 1

                if response.text != "[]" and response:
                    message = json.JSONDecoder().decode(response.text)
                    try:
                        for item in message:
                            if item['type'] == "added:event":
                                if 'details' in item:
                                    if 'payload' in item['details']:
                                        if 'sender-id' in item['details']['payload']:
                                            if item['details']['payload']['sender-id'] == recipient:
                                                message_list.append(item)
                                                text.append(item['details']['payload']['text'])
                                                break
                    except:
                        pass

    # <--------------------------------------

            #for item in message_list:
                #if 'details' in item:
                    #if 'type' in item['details']:
                        #if item['details']['type'] == "message":
                            #if 'payload' in item['details']:
                                #if 'text' in item['details']['payload']:

    ############## <------------------------------
            for item in text:
                if item.split(" ").__len__() > 1:
                    index = text.index(item)
                    text[index] = item.split(" ")

            pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
            pattern2 = re.compile("(^[a-zA-Z0-9_.+-]+ [a-zA-Z0-9-] +\.[a-zA-Z0-9-.]+$)")

            for item in text:
                if type(item) is list:
                    for word in item:
                        if pattern.match(word) or pattern2.match(word):
                            email = word
                            user = info
                else:
                    if pattern.match(item) or pattern2.match(item):
                        email = item
                        user = info


    if email:
        #save_soap(output, email, user)
        output.insert(END, "Yay! Email successfully fetched from " + name + "(" + recipient + ")")
        info = json.JSONDecoder().decode(user.text)
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
                    r = requests.get("https://api7.triptogether.com/users/" + info['id'] + "/photos/" + item + ".310x455")
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
    else:
        if no_answer:
            output.insert(END, "No answer from " + name + "(" + recipient + ")")

        else:
            output.insert(END, "No mail from " + name + "(" + recipient + ")")


def get_threads():
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


def initiate_spam(output, auth_r, id_list):
    save_path = getPath()
    thread_counter = 0
    gotten_msg_list = get_msgs()
    for id_ in id_list:
        #if thread_counter > int(get_threads()):
        #    time.sleep((int(get_timeout())*60) + 5)

        time.sleep(3)
        curr_thread = threading.Thread(target=send, args=(id_, auth_r, output, save_path, gotten_msg_list))
        curr_thread.daemon = True
        thread_list.append(curr_thread)
        curr_thread.start()
        thread_counter += 1

    manager_thread = threading.Thread(target=manage_threads, args=(output, save_path))
    manager_thread.daemon = True
    manager_thread.start()
    # thread_list.append(manager_thread)


def start_spam_thread(output, login_val, password_val):
    save_path = getPath()
    if thread_list == []:
        auth_r = authorizeOnSite(output, login_val, password_val)

        if auth_r.status_code == 200:
            output.insert(END, "Looking through history...")
            id_list = get_ids()

            if id_list:
                output.insert(END, "Initiating spam...")

                spam_thread = threading.Thread(target=initiate_spam, args=(output, auth_r, id_list))
                spam_thread.daemon = True
                spam_thread_list.append(spam_thread)
                spam_thread.start()
                output.insert(END, "Done! You may go and drink some coffee.")
                output.insert(END, "Meanwhile bot will be doing your dirty work ;)")

            else:
                output.insert(END, "Could not find ids. Try fetching some first.")

    else:
        output.insert(END, "Bot already works.")