# Converts a long URL into a TinyURL
# http://snipplr.com/view/7604/python-make-url-address-to-tinyurl/

import urllib

def tiny_url(url):
    # URL must start with HTTP!
    if not url.startswith("http://"):
        url = "http://" + url
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.urlopen(apiurl + url).read()
    return tinyurl

def content_tiny_url(content):
    regex_url = r'http:\/\/([\w.]+\/?)\S*'
    for match in re.finditer(regex_url, content):
        url = match.group(0)
        content = content.replace(url,tiny_url(url))

    return content
