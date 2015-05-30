#!/usr/bin/env python
# coding: utf-8

import subprocess
import requests
from requests.exceptions import HTTPError
import json


"""
Simple script to get the gps.json output
and send w3w address and lat/lng to Mac OS pasteboard as markdown.
"""

def main():
    # Set url if publishing to web
    url = 'http://example.com/gps.json'
    locreq = requests.get(url)
    try:
        locdata = locreq.json()
    # In case gps.json not on web, get it as local file
    except:
        with open('gps.json') as f:
            locreq = f.read()
            locdata = json.loads(locreq)
    print locdata


    lat = locdata['latitude']
    lng = locdata['longitude']
    w3w = locdata['what3words']
    words = w3w.replace('http://w3w.co/', '')

    locload = '[%s](%s)  \n%s, %s' % (words, w3w, lat, lng)

    # This here is Mac OS X specific, nerds
    subprocess.call("echo '%s' | pbcopy" % locload, shell=True)

if __name__ == "__main__":
    main()