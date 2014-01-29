#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from datetime import datetime
import json
import os
import sys
import time

from boto.dynamodb2.items import Item
from boto.dynamodb2.table import Table
from lib.arduino_io import arduino, fake_arduino

drinkers = Table('drinkers')
drinks = Table('drinks')

def get_drinker(code):
    drinker = drinkers.get_item(code=code)
    if (drinker == None):
        drinker = Item(drinkers, data={
                'code': code,
                'volume_consumed': 0,
                'number_of_drinks' : 0
                })
    if (drinker['code'] == None):
        drinker['code'] = code
    if (drinker['name'] == None):
        drinker['name'] = "UNKNOWN"
    if (drinker['volume_consumed'] == None):
        drinker['volume_consumed'] = 0
    if (drinker['number_of_drinks'] == None):
        drinker['number_of_drinks'] = 0
    if (drinker['allowed'] == None):
        drinker['allowed'] = 0

    return drinker
                    
def update_dynamo(values):
    # Tables:
    # DRINK_RECORD
    # -code : hash key
    # -timestamp : range key
    # -amount
    # -tap
    # USER_TOTALS
    # -code : hash key
    # -number_of_drinks
    # -volume_consumed
    code = values["CODE"]
    tap_one = values["TAP_ONE"]
    tap_two = values["TAP_TWO"]
    total_amount = tap_one + tap_two
    timestamp = long(time.time())
    if (total_amount > 0):
        drinker = get_drinker(code)
        if (tap_one > 0):
            drinker['volume_consumed'] = drinker['volume_consumed'] + int(tap_one)
            drinker['number_of_drinks'] = drinker['number_of_drinks'] + 1
            drink_1 = Item(drinks, data={
                    'code': code,
                    'timestamp': timestamp,
                    'amount': int(tap_one),
                    'tap' : 1
                    })
            drink_1.save()
            timestamp = timestamp + 1 # Not ideal, but this lets us store both drinks separately, as the code/timestamp combination must be unique
        if (tap_two > 0):
            drinker['volume_consumed'] = drinker['volume_consumed'] + int(tap_two)
            drinker['number_of_drinks'] = drinker['number_of_drinks'] + 1
            drink_2 = Item(drinks, data={
                    'code': code,
                    'timestamp': timestamp,
                    'amount': int(tap_two),
                    'tap' : 2
                    })
            drink_2.save()
        drinker.save()
        print("User " + code + " drank " + str(tap_one) + " mL from tap one and " + str(tap_two) + " mL from tap two at " + datetime.fromtimestamp(timestamp).strftime("%I:%M%p on %A, %d %B %Y"))
    else:
        print("User " + code + " tapped their badge without drinking at " + datetime.fromtimestamp(timestamp).strftime("%I:%M%p on %A, %d %B %Y"))

def amount_allowed(code):
    drinker = get_drinker(code)
    if (drinker['allowed']):
        return 500 # A bit more than a pint
    else:
        return 0

def handle_input(arduino, input):
    values = json.loads(input)
    if (values['FUNCTION'] == 'DRINK_DATA'):
        update_dynamo(values)
    elif (values['FUNCTION'] == 'CHECK_CODE'):
        arduino.send_output(str(amount_allowed(values['CODE'])))

if __name__ == "__main__":
    while (True) :
        try:
            arduino = arduino()
            #arduino = fake_arduino()
            while ( True ) :
                input = arduino.await_input()
                print("Received input: " + input)
                handle_input(arduino, input)
        except:
            print("An error occurred.  Sleeping for five seconds and continuing.")
            time.sleep(5)
