from views import *
import requests
import json
from datetime import datetime
import pycountry
from fileworker import *
from multiprocessing.pool import ThreadPool
import threading
from time import sleep

SITE = "https://api.triptogether.com/"

fetching_thread_list = []


def get_budget_weight(word):
    if word == 'low':
        return 0
    if word == 'medium':
        return 1
    if word == 'high':
        return 2
    if word == 'very-high':
        return 3


def iniciate_fetching(output):
    output.insert(END, "\n==============================================")
    output.insert(END, "Fetching IDs from " + SITE + "...")

    fetching_thread = threading.Thread(target=get_page_ids, args=(output,))
    fetching_thread.daemon = True
    fetching_thread.start()
    fetching_thread_list.append(fetching_thread)
    output.insert(END, "Now wait until thread will finish fetching IDs...")
    output.insert(END, "I will let you now, when its done ;)")


def get_page_ids(output):
    ids_to_save = []
    list_victims = []
    r = None
    while r is None:
        try:
            r = requests.get(SITE + "users?filter=photos&omit=0&select=100&sort=7")
            list_victims = json.JSONDecoder().decode(r.text)
        except:
            output.insert(END, "Couldn't connect to site. Check your internet.")
            output.insert(END, "Retrying...")
            sleep(20)
            continue
            
    for item in list_victims:
        try:
            info = requests.get(SITE + 'users/' + item['id'])
            info_list = json.JSONDecoder().decode(info.text)
            output.delete(END)
            output.insert(END, "Checking user " + info_list['name'] + " (" + info_list['id'] + ")")
        except:
            output.delete(END)
            output.insert(END, "Couldn't fetch user " + item['id'] + " (" + item['id'] + ")")
            continue

        if int(getPremOnly()) == 1:
            if 'profileHighlighting' in info_list:
                if 'mark' in info_list:
                    if info_list['profileHighlighting']['mark'] != "premium":
                        continue

        if 'gender' in info_list:
            if info_list['gender'] != getGender()[:3]:
                continue

        if 'birthday' in info_list:
            age = datetime.now() - datetime.strptime(info_list['birthday'], '%Y-%m-%dT%H:%M:%SZ')
            age = age.days/365

            if not (int(getAgeFrom()) <= int(age) <= int(getAgeTo())):
                continue
        else:
            continue

        if getBirth():
            if 'country' in info_list:
                if pycountry.countries.get(alpha_2=info_list['country'].__str__()).name in getBirth():
                    continue
            else:
                continue

        if getJobs():
            if 'occupation' in info_list:
                if info_list['occupation'] not in getJobs():
                    continue
            else:
                if getNoJobCb() != 1:
                    continue
        try:
            trips = requests.get(SITE + 'trips/' + item['id'] + '?status=planned')
            trips_list = json.JSONDecoder().decode(trips.text)
        except:
            output.delete(END)
            output.insert(END, "Couldn't fetch trips form user " + item['id'] + " (" + item['id'] + ")")
            continue

        suitable_trip = False

        if getNoTripCb() == 1 and trips_list == []:
            suitable_trip = True

        for trip in trips_list:
            if getNoTripCb() == 1:
                suitable_trip = True
                break

            if getTrips():
                if 'destination' in trip:
                    if 'country' in trip['destination'] and 'budget' in trip:
                        if pycountry.countries.get(alpha_2=trip['destination']['country']).name + " | " + trip['budget'] \
                                 in getTrips():
                            suitable_trip = True

                        elif getBudget():

                            if 'budget' in trip:
                                if get_budget_weight(trip['budget']) >= get_budget_weight(getBudget()):
                                    suitable_trip = True

                            else:
                                if getAnyBudgetCb():
                                    suitable_trip = True
                                else:
                                    continue
                # else

            else:
                suitable_trip = True

        if suitable_trip:
            output.delete(END)
            output.insert(END, "User " + info_list['name'] + " (" + info_list['id'] + ") was added to check list!")
            output.insert(END, "")
            ids_to_save.append(info_list['id'])

    counter = save_id(ids_to_save)

    output.delete(END)
    output.insert(END, "Done! New IDs: " + counter.__str__())
    if counter == 0:
        output.insert(END, "New IDs: " + counter.__str__() + ". Try lowering your preferences.")

    fetching_thread_list.clear()

