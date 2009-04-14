#!/usr/bin/env python
import xml.etree.cElementTree as ET
import urllib
import tiny


latestTitle = ""
latestPrice = ""
soldout = 1

url = "http://www.woot.com/salerss.aspx"

def checkWoot(irc, event, args="", force=True):
    '''Checks woot.com for the latest deal. force says whether to report the deal if it hasn't changed since the last check.'''
    channel = event.target()
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
#    buylink = tiny.tiny_url(url=buylink)

    if latestTitle == title and force != True:  # Don't report the deal if it hasn't changed since last time
        return
    latestTitle = title
    latestPrice = price
    irc.privmsg(channel, "Woot! - %s --- %s --- %s%% left! --- %s" % (latestTitle, str(latestPrice), str(soldout), buylink))
