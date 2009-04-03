#!/usr/bin/env python
import xml.etree.cElementTree as ET
import urllib
import tiny


latestTitle = ""
latestPrice = ""
soldout = 1

url = "http://www.woot.com/salerss.aspx"

def checkWoot(irc, channel, args="", force=True):
    global latestTitle
    global latestPrice
    global souldout
    try:
        rss = ET.parse(urllib.urlopen(url)).getroot()
    except:
        return ""
    title = rss.findall("channel/item/title")[0].text
    price = rss.findall("channel/item/{http://www.woot.com/}price")[0].text
    soldout = rss.findall("channel/item/{http://www.woot.com/}soldoutpercentage")[0].text
    soldout = 100 - (float(soldout) * 100)
    buylink = rss.findall("channel/item/{http://www.woot.com/}purchaseurl")[0].text
#    buylink = tiny.tiny_url(url=buylink)

    if latestTitle == title and force != True:
        return ""
    latestTitle = title
    latestPrice = price
    irc.privmsg(channel, "Woot! - %s --- %s --- %s%% left! --- %s" % (latestTitle, str(latestPrice), str(soldout), buylink))

#print checkWoot()
