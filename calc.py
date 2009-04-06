# Brian Cottingham
# spiffytech@gmail.com
# 2009-04-02
# Performs calculations with Google Calculator. Should be able to perform any calculation the Goog can.

import re
import urllib


def calc(irc, event, equation):
    '''Core calculator function'''
    channel = event.target()
    opener = myOpener()
    page = opener.open("http://www.google.com/search?num=1&q=%s" % urllib.quote(equation)).read()  # Get the page from Google
    try:
        reply = re.search("<h2 class=r style=\"font-size:\d+%\"><b>(?P<answer>.*)</b></h2>", page).groups()[0]
    except:
        reply = "Google doesn't think that question is worth answering"

    irc.privmsg(channel, reply)



class myOpener(urllib.FancyURLopener):  # Google doesn't like the urllib "urllib_version" useragent. Subclass it to override the useragent.
    version = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko/2009032713 Fedora/3.0.8-1.fc10 Firefox/3.0.8"
