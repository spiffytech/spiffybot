import urllib, re
from xml.dom import minidom  # Yeah, I wrote this before I found out about ElementTree and BeautifulSoup/

def getWeather(irc, event, place):
    '''Returns the current weather for a given city and state'''
    # TODO: Find a way to let the user input a zip code instead of city/state
    channel = event.target()
    city = place.partition(", ")[0].replace(" ", "%20")
    state = place.partition(", ")[2]

    content = urllib.urlopen("http://www.rssweather.com/wx/us/" + state + "/" + city + "/rss.php")  # Grab the rssweather.com page for this location
    xmldoc = minidom.parse(content)

    try:
        pubDate = xmldoc.getElementsByTagName("pubDate")[0].firstChild.data  # Try to find the weather on the page
    except: 
        return "I don't know that city"
    pubDate = pubDate.split(" ")[4] + " GMT " + pubDate.split(" ")[5]
    summary = xmldoc.getElementsByTagName("description")[1].firstChild.data
    reply = summary + " (" + pubDate + ")"

    irc.privmsg(channel, reply)
