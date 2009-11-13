# Brian Cottingham
# 2009-04-14
# Converts a long URL into a TinyURL
# http://snipplr.com/view/7604/python-make-url-address-to-tinyurl/

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

import urllib

def tiny_url(event=None):
    '''Converts a long url to a tinyurl'''
    if event.args == None:
        event.reply("Give me a url!")
        return
    else:
        url = event.args
    # URL must start with HTTP!
    if not url.startswith("http://"):
        url = "http://" + url
    apiurl = "http://tinyurl.com/api-create.php?url="
    try:
        tinyurl = urllib.urlopen(apiurl + url).read()
    except UnicodeError:
        event.reply("Can't encode that URL, it contains unicode!")
        return
    if event != None:
        event.reply(tinyurl)
    else:
        return tinyurl
