#!/usr/bin/env python
# coding: utf-8
import os
import json
from time import strftime
from datetime import datetime, timedelta

from pyicloud import PyiCloudService
from what3words import what3words


def main():
    # CONFIGURE THIS
    # Put your own Apple ID email below, and UUID of device you wish to track
    # TODO: move this to some external config!
    apple_id = 'yagermadden@gmail.com'
    # pyicloud doc shows how to find device UUIDs
    device_uuid = 'sY3gtg2FLyuE6wmzOgXtgQyYoEoH0bjNwMoQsJnhdFr/PJxj1VsSbhULIAFHmzJI' # <- fake ;)
    # ====================================== #

    # AND PROVISION YOUR ENVIRONMENT
    # Set your iCloud password as environment variable with key 'ICLOUDPASSWORD'
    # (So we don't *have* to add to config, because secret!)
    icloudpass = os.getenv('ICLOUDPASSWORD')
    # Get what3words API key from http://developer.what3words.com and set in envar
    w3wapikey = os.getenv('W3W_KEY')
    # ====================================== #

    # Connect to iCloud API
    icloud = PyiCloudService(apple_id, icloudpass)

    # Get index of device
    d = icloud.devices.keys().index(device_uuid)

    # Request GPS coordinates of device
    lat = icloud.devices[d].location()['latitude']
    lng = icloud.devices[d].location()['longitude']

    # Mark the time
    tim = strftime('%Y-%m-%dT%H:%M:%S')
    nexttim = (datetime.now() + timedelta(minutes = 9)).strftime('%Y-%m-%dT%H:%M:%S')

    # Request what3words address based on lat, lng
    w3w = what3words(apikey=w3wapikey)
    res = w3w.getWords(lat=lat, lng=lng)

    # Flatten w3w response, add domain to make URL
    wordlist = res['words']
    words = '.'.join(wordlist)
    w3wurl = 'http://w3w.co/%s' % words

    # Set up dict w/ data
    location = {'as_of': tim, 'latitude': lat, 'longitude': lng, 'what3words': w3wurl, 'nextupdate':nexttim}

    # write the json data to file
    file_name = 'gps.json'
    with open (file_name, 'w') as outfile:
        json.dump(location, outfile, sort_keys=True, indent=4)

if __name__ == "__main__":
    main()

