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

import csv
import urllib

def quote(connection=None, event=None, symbol=None):
    page = urllib.urlopen("http://finance.yahoo.com/d/quotes.csv?s=%s&f=l1c1p2jkns" % symbol).read().split("\n")
    quotes = csv.DictReader(page, fieldnames=("last", "change", "changePercent", "52low", "52high", "name", "symbol"), delimiter=",")
    for q in quotes:
        connection.privmsg(event.target(), "%s (%s) || Current price: %s || Change today: %s (%s) || 52-week low/high: %s / %s" % (q["symbol"], q["name"], q["last"], q["change"], q["changePercent"], q["52low"], q["52high"]))


# Query formatter
#last trade = l1
#change today = c1
#change today percent = k2
#52-week range = j, k
#stock name = n
#symbol = s
