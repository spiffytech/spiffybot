#!/usr/bin/env python

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


import xml.etree.cElementTree as ET
import urllib
import tiny


latestTitle = ""
latestPrice = ""
soldout = 1

url = "http://www.woot.com/salerss.aspx"

def checkWoot(event, force=True):
    '''Checks woot.com for the latest deal. force says whether to report the deal if it hasn't changed since the last check.'''
    global latestTitle
    global latestPrice
    global soldout
    try:
        rss = ET.parse(urllib.urlopen(url)).getroot()  # Get the woot RSS feed and prepare to parse it
    except:
        return
    title = rss.findall("channel/item/title")[0].text
    price = rss.findall("channel/item/{http://www.woot.com/}price")[0].text
    soldout = rss.findall("channel/item/{http://www.woot.com/}soldoutpercentage")[0].text
    soldout = 100 - (float(soldout) * 100)  # In the feed item, soldout is a decimal percent
    buylink = rss.findall("channel/item/{http://www.woot.com/}purchaseurl")[0].text
    buylink = tiny.tiny_url(url=buylink)

    if latestTitle == title and force != True:  # Don't report the deal if it hasn't changed since last time
        return
    latestTitle = title
    latestPrice = price
    event.reply("Woot! - %s --- %s --- %s%% left! --- Purchase: %s" % (unicode(latestTitle), unicode(latestPrice), unicode(soldout), buylink))
