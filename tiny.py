# Brian Cottingham
# 2009-04-14
# Converts a long URL into a TinyURL
# http://snipplr.com/view/7604/python-make-url-address-to-tinyurl/

import urllib

def tiny_url(irc=None, event=None, url=None):
    if event != None:
        channel = event.target()
    '''Converts a long url to a tinyurl'''
    # URL must start with HTTP!
    if not url.startswith("http://"):
        url = "http://" + url
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.urlopen(apiurl + url).read()
    if event != None:
        irc.privmsg(channel, tinyurl)
    else:
        return tinyurl
