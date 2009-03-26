#!/usr/bin/env python
import xml.etree.cElementTree as ET
import urllib
import tiny


latestTitle = ""
latestPrice = ""
soldout = 1

url = "http://www.woot.com/salerss.aspx"

def checkWoot(force=False):
    global latestTitle
    global latestPrice
    global souldout
    rss = ET.parse(urllib.urlopen(url)).getroot()
    title = rss.findall("channel/item/title")[0].text
    price = rss.findall("channel/item/{http://www.woot.com/}price")[0].text
    soldout = rss.findall("channel/item/{http://www.woot.com/}soldoutpercentage")[0].text
    soldout = 100 - (float(soldout) * 100)
    buylink = rss.findall("channel/item/{http://www.woot.com/}purchaseurl")[0].text
    buylink = tiny.tiny_url(buylink)

    if latestTitle == title and force != True:
        return ""
    latestTitle = title
    latestPrice = price
    return "Woot! - %s --- %s --- %s%% left! --- %s" % (latestTitle, str(latestPrice), str(soldout), buylink)

#print checkWoot()
