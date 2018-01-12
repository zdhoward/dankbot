import requests
import csv
from pprint import pprint


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

def getPrice(itemName):
    itemID = eveToID(itemName)
    msg = ''
    #GET grom ESI Swagger
    response = requests.get('https://esi.tech.ccp.is/latest/markets/prices/')
    for each in response.json():
#TODO# THIS SHOLD BE A GREP
        if each['type_id'] == int(itemID):
            msg += itemName
            msg += '> avg: '
            msg += '{:,}'.format(each['average_price'])
            msg += ' adj: '
            msg += '{:,}'.format(each['adjusted_price'])
    return msg
