# Brian Cottingham
# spiffytech@gmail.com
# 2009-04-02
# Performs calculations with Google Calculator. Should be able to perform any calculation the Goog can.

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


def calc(irc, event, equation):
    '''Uses Google Calculator to perform calculations'''
    channel = event.target()
    opener = myOpener()  # Good ol' useragent spoofing
    page = opener.open("http://www.google.com/search?num=1&q=%s" % urllib.quote(equation)).read()  # Get the page from Google
    try:
        reply = re.search("<h2 class=r style=\"font-size:\d+%\"><b>(?P<answer>.*)</b></h2>", page).groups()[0]  # Grab the calc output
    except:  # Couldn't find the calc output (note that calc (presently) only does actual calculations- not time zones, etc.
        reply = "Google doesn't think that question is worth answering"

    irc.privmsg(channel, reply)



class myOpener(urllib.FancyURLopener):  # Google doesn't like the urllib "urllib_version" useragent. Subclass it to override the useragent.
    version = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko/2009032713 Fedora/3.0.8-1.fc10 Firefox/3.0.8"
