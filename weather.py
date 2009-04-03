import urllib, re
from xml.dom import minidom

def getWeather(irc, channel, place):
    city = place.partition(", ")[0].replace(" ", "%20")
    state = place.partition(", ")[2]

    content = urllib.urlopen("http://www.rssweather.com/wx/us/" + state + "/" + city + "/rss.php")
    xmldoc = minidom.parse(content)
    
    try:
        pubDate = xmldoc.getElementsByTagName("pubDate")[0].firstChild.data
    except: 
        return "I don't know that city"
    pubDate = pubDate.split(" ")[4] + " GMT " + pubDate.split(" ")[5]
    summary = xmldoc.getElementsByTagName("description")[1].firstChild.data
    reply = summary + " (" + pubDate + ")"

    irc.privmsg(channel, reply)
