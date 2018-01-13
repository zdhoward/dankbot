import requests
import csv
from pprint import pprint

import subprocess

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
    #import csv
    with open('invTypes.csv', 'r') as f:
        reader = csv.reader(f)
        names = list(reader)
    #find Name
    itemID = 'NOT FOUND'
    items = []
    for name in names:
        #if itemName.upper() in name[2].upper():
        # '.*'
#        regex = re.compile(r"\(?:^|\W)antimatter(?:$|\W)\b", re.I)
#        items = regex.findall(name[2])

        if re.match(itemName.upper(), name[2].upper()):
            check = True
            for word in ITEM_IGNORE_LIST:
                if word.upper() in name[2].upper():
                    check = False
            if check:
                itemID = name[0]
                items.append(itemID)

    pprint(len(items))
    if len(items) < 1:
        items = [{'type_id': 0, 'average_price': 0.00}]

    return items

def getPrices(itemName, n=1):
    itemIDs = eveToIDs(itemName)
    msg = ''
    #GET grom ESI Swagger
    response = requests.get('https://esi.tech.ccp.is/latest/markets/prices/')
    for each in response.json():
        for item in itemIDs:
            if (each['type_id'] != None) & (each['type_id'] != 0) & (each['type_id'] != '0'):
                if each['type_id'] == int(item):
                    msg += eveToName(item)
                    msg += '> avg: '
                    msg += '{:,}'.format(int(each['average_price'])*n)
                    msg += '\n'
                    #msg += ' adj: '
                    #msg += '{:,}'.format(each['adjusted_price'])
    return msg

#pprint(getPrices("Antimatter"))
#pprint(getPrices("PLEX", 500))
