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


import csv
import feedparser
import re

def getWeather(connection=None, event=None, place=None):
    '''Replies to a message with the current weather at a given location'''
    place = str(place)
    if re.match("[0-9]{5}", place) == None:
        print place
        print "Looking up city..."
        zipcodes = findZip(place)  # Find the zip code from the city & state
    else:
        zipcodes = [place]

    for zip in zipcodes:
        url = "http://weather.yahooapis.com/forecastrss?p=" + zip + "&u=f"
        data = feedparser.parse(url)
        summary = data.entries[0].summary
        summary = re.split(r'\n',re.sub('<.+?>','',summary))

        if not summary[0].startswith("Sorry"):
            reply = summary[2]
            break

    if not "reply" in locals():
        connection.privmsg(event.target(), "No such city in our totally awesome database of cities")
        return


    if connection == None:
        print reply
    else:
        connection.privmsg(event.target(), reply)


def findZip(place):
    '''Takes a city and state, then finds that place's zip code'''
    if len(place.split(",")) > 1:
        city = place.partition(",")[0]
    else:
        city = place.split()[:-2]
    city = city.lower()
    print city
    state = place[-2:].upper()
    zipcodes = []  # There is sometimes more than one zipcode for a single city

    reader = csv.DictReader(open("zipcodes.csv"), ("zip", "city", "state", "latitude", "longitude", "timezone", "dst"), delimiter=",", quotechar='"')
    for place in reader:
        if place["city"].lower() == city and place["state"] == state:
            zipcodes.append(place["zip"])
    return zipcodes
