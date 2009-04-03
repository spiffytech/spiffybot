# Brian Cottingham
# spiffytech@gmail.com
# 2009-04-02
# Performs calculations with Google Calculator. Should be able to perform any calculation the Goog can.

from BeautifulSoup import BeautifulSoup
from urllib import FancyURLopener

def calc(irc, channel, equation):
    '''Core calculator function'''
    page = myOpener.open("http://www.google.com/search?num=1&q=%s" % urllib.quote(equation).read()  # Get the page from Google
    page = "".join(page.split("\n"))  # URLlib returns a printable page, with newlines! Bad for Beautiful Soup. This fixes that problem.
    page = BeautifulSoup(page)  # Finally, we can parse the page. 


class myOpener(FancyURLopener):  # Google doesn't like the urllib "urllib_version" useragent. Subclass it to override the useragent.
    version = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko/2009032713 Fedora/3.0.8-1.fc10 Firefox/3.0.8"
