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


# Weather courtesy Weather Underground, Inc.
import re
import urllib
from BeautifulSoup import BeautifulStoneSoup

def getWeather(event):
    place = event.args
    '''Returns the current weather for a given city and state'''

    # Start off with the forecast data
    page = urllib.urlopen("http://api.wunderground.com/auto/wui/geo/ForecastXML/index.xml?query=%s" % urllib.quote(place))
    page = page.read()
    soup = BeautifulStoneSoup(page)

    if len(soup.findAll("forecastday")) == 0:  # This seems to be a reliable identifier of places wunderground doesn't recognize
        event.reply("No such place")
        return

    forecast = soup.findAll(name="fcttext")
    if len(forecast) >= 1:  # Some places, especially those outside America, don't have forecasts available.
        forecast = stripTags(forecast[0])
    else:
        del forecast  # Allows us to check it's existence later in the function, and it's useless without data anyway
    dayHigh = stripTags(soup.findAll(name="high")[0].findAll(name="fahrenheit")[0])
    dayLow = stripTags(soup.findAll(name="low")[0].findAll(name="fahrenheit")[0])

    # Now get the current weather data
    page = urllib.urlopen("http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query=%s" % urllib.quote(place))
    page = page.read()
    soup = BeautifulStoneSoup(page)
    temperature = stripTags(soup.findAll(name="temp_f")[0])
    sampleTime = stripTags(soup.findAll(name="observation_time")[0])
    sampleTime = " ".join(sampleTime.split()[3:])
    weatherType = stripTags(soup.findAll(name="weather")[0])
    location = stripTags(soup.findAll(name="full")[0])

    reply = "Weather for %s (as of %s): %sF and %s. High/low: %s/%sF. " % (location, sampleTime, temperature, weatherType.lower(), dayHigh, dayLow)
    if "forecast" in locals():
        reply += "Forecast: %s" % forecast
    event.reply(reply)


def stripTags(text):
    '''Strips the XML tags from data. I can't believe BeautifulSoup doesn't do this already.'''
    return ''.join(BeautifulStoneSoup(str(text)).findAll(text=True))
