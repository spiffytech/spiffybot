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


import re
import urllib
from xml.dom import minidom  # Yeah, I wrote this before I found out about ElementTree and BeautifulSoup

def getWeather(irc, event, place):
    '''Returns the current weather for a given city and state'''
    # TODO: Find a way to let the user input a zip code instead of city/state
    channel = event.target()

    if not re.match("[0-9]{5}", place):  # User gave us a zip code
        city = place.partition(", ")[0].replace(" ", "%20")
        state = place.partition(", ")[2]

        content = urllib.urlopen("http://www.rssweather.com/wx/us/" + state + "/" + city + "/rss.php")  # Grab the rssweather.com page for this location
    else:  # User gave us a city & state
        content = urllib.urlopen("http://www.rssweather.com/zipcode/" + place + "/rss.php")

    xmldoc = minidom.parse(content)

    try:
        pubDate = xmldoc.getElementsByTagName("pubDate")[0].firstChild.data  # Try to find the weather on the page
    except: 
        irc.privmsg(event.target(), "I don't know that city")
    pubDate = pubDate.split(" ")[4] + " GMT " + pubDate.split(" ")[5]
    summary = xmldoc.getElementsByTagName("description")[1].firstChild.data
    reply = summary + " (" + pubDate + ")"

    irc.privmsg(channel, reply)
