#!/usr/bin/env python
# Brian Cottingham
# 2008
# Provides a few functions for going back and forth with Unix timestamps

#This file is part of Spiffybot.
#
#Spiffybot is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Spiffybot is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Spiffybot.  If not, see <http://www.gnu.org/licenses/>.


import time

# Constant number of seconds. Should replace with datetime module.
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
