import requests
import csv
from pprint import pprint

import re

ITEM_IGNORE_LIST = {' SKIN', ' BLUEPRINT'}


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
    items = []
    #import csv
    with open('invTypes.csv', 'r') as f:
        reader = csv.reader(f)
        names = list(reader)
    #find Name
    itemID = 'NOT FOUND'
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
        items = {}

    return items

def getPrice(itemName):
    itemIDs = eveToIDs(itemName)
    msg = ''
    #GET grom ESI Swagger
    response = requests.get('https://esi.tech.ccp.is/latest/markets/prices/')
    for each in response.json():
        for item in itemIDs:
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
    return msg
