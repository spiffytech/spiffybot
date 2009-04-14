#!/usr/bin/env python
# Brian Cottingham
# 2008
# Provides a few functions for going back and forth with Unix timestamps

import time

MINUTE = 60
HOUR = 3600
DAY = 216000
WEEK = 1512000
YEAR = 78840000

def toEpoch(human, format="%Y-%m-%d %H:%M"):
    '''Converts a human-readable date to the Unix epoch'''
    try:
        epoch = int(time.mktime(time.strptime(human, format)))
    except ValueError:  #No minutes specified
        try:
            epoch = int(time.mktime(time.strptime(human, '%Y-%m-%d')))
        except:
            print "enter a properly-formatted human date for toEpoch to convert"
    return epoch



def fromEpoch(epoch, secs = 0):  # Returns the full date and time
    '''Convert a Unix timestamp to a human-readable format. Seconds in output is optional.'''
    epoch = float(epoch)
    human_array = time.localtime(epoch)
    human = str(human_array[0])+"-"+str(human_array[1]).zfill(2)+"-"+str(human_array[2]).zfill(2)+" "+str(human_array[3]).zfill(2) + ":" + str(human_array[4]).zfill(2)
    if secs == 1:
        human += ":" + str(human_array[5])
    return human



def extractDate(epoch):  # Returns only the date
    '''Get just the date from a Unix timestamp'''
    human_array = time.localtime(epoch)
    human = str(human_array[0])+"-"+str(human_array[1]).zfill(2)+"-"+str(human_array[2]).zfill(2)
    return human



def extractTime(epoch):  # Returns only the time
    '''Get just the time from a Unix timestamp'''
    human_array = time.localtime(epoch)
    human = str(human_array[3]).zfill(2)+":"+str(human_array[4]).zfill(2)
    return human
