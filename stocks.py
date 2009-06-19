import csv
import urllib

def quote(connection=None, event=None, symbol=None):
    page = urllib.urlopen("http://finance.yahoo.com/d/quotes.csv?s=%s&f=l1c1p2jkns" % symbol).read().split("\n")
    quotes = csv.DictReader(page, fieldnames=("last", "change", "changePercent", "52low", "52high", "name", "symbol"), delimiter=",")
    for q in quotes:
        print "%s (%s) || Current price: %s || Change today: %s (%s) || 52-week low/high: %s / %s" % (q["symbol"], q["name"], q["last"], q["change"], q["changePercent"], q["52low"], q["52high"])


#last trade = l1
#change today = c1
#change today percent = k2
#52-week range = j, k
#stock name = n
#symbol = s
