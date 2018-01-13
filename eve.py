import requests
import csv
from pprint import pprint

import re

ITEM_IGNORE_LIST = {' SKIN'} #, ' BLUEPRINT'}


def eveToName(itemID):
    #import csv
    with open('invTypes.csv', 'r') as f:
        reader = csv.reader(f)
        items = list(reader)
    #find Name
    name = 'NOT FOUND'
    for item in items:
        if item[0] == itemID:
            name = item[2]
    return name

def eveToID(itemName):
    #import csv
    with open('invTypes.csv', 'r') as f:
        reader = csv.reader(f)
        names = list(reader)
    #find Name
    itemID = 'NOT FOUND'
    for name in names:
        if name[2].upper() == itemName.upper():
            itemID = name[0]
    return itemID

def eveToIDs(itemName):
    #import csv
    with open('invTypes.csv', 'r') as f:
        reader = csv.reader(f)
        names = list(reader)
    #find Name
    itemID = 'NOT FOUND'
    items = []
    for name in names:
        if itemName.upper() in name[2].upper():
            check = True
            for word in ITEM_IGNORE_LIST:
                if word.upper() in name[2].upper():
                    check = False
            if check:
                itemID = name[0]
                items.append(itemID)


    if len(items) < 1:
        items = [{'type_id': 0, 'average_price': 0.00}]

    return items

def getPrice(itemName):
    itemIDs = eveToIDs(itemName)
    msg = ''
    #GET grom ESI Swagger
    response = requests.get('https://esi.tech.ccp.is/latest/markets/prices/')
    for each in response.json():
        for item in itemIDs:
            if (each['type_id'] != None) & (each['type_id'] != 0) & (each['type_id'] != '0'):
                if each['type_id'] == int(item):
                    msg += item
                    msg += '> '
                    msg += eveToName(item)
                    msg += '> avg: '
                    msg += '{:,}'.format(each['average_price'])
                    msg += '\n'
                    #msg += ' adj: '
                    #msg += '{:,}'.format(each['adjusted_price'])
                    #msg += 'DEBUG:\n'
                    #msg += str(each)

                    #
                    #Ignoring exception in on_message
                    #Traceback (most recent call last):
                    #  File "/home/zecx/.local/lib/python3.5/site-packages/discord/client.py", line 307, in _run_event
                    #    yield from getattr(self, event)(*args, **kwargs)
                    # File "dankbot.py", line 222, in on_message
                    #    msg += getPrice(item)
                    # File "/home/zecx/Scripts/dankbot/eve.py", line 70, in getPrice
                    #    msg += '{:,}'.format(each['average_price'])
                    #KeyError: 'average_price'
                    #

    return msg
