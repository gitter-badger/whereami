#!/usr/bin/env python
# coding: utf-8

import os
from time import strftime
from datetime import datetime
from pyicloud import PyiCloudService
from what3words import What3Words
import what3words
import forecastio
import json

# Mac OS certs: still hard (comment out before linux deploy)
import requests
requests.packages.urllib3.disable_warnings()

# Get envars for config
apple_id = os.getenv('APPLE_ID')
icloudpass = os.getenv('ICLOUDPASSWORD').replace('\"', '')
device_uuid = os.getenv('DEVICE_UUID')
w3wapikey = os.getenv('W3WAPIKEY')
forecastio_key = os.getenv('FORECASTIOKEY')



# Functions to poll remote services
def provision_geo_data():
    # Connect to iCloud API
    icloud = PyiCloudService(apple_id, icloudpass)

    # Get index of device
    d = icloud.devices.keys().index(device_uuid)

    # Request GPS coordinates of device
    lat = icloud.devices[d].location()['latitude']
    lng = icloud.devices[d].location()['longitude']

    # Mark the time
    tim = strftime('%Y-%m-%dT%H:%M:%S')

    # Request what3words address based on lat, lng
    w3w = What3Words(api_key=w3wapikey)
    res = w3w.words(lat=lat, lng=lng)

    # Flatten w3w response, add domain to make URL
    wordlist = res['words']
    words = '.'.join(wordlist)
    w3wurl = 'http://w3w.co/%s' % words

    geotag = {'latitude': lat,
            'longitude': lng,
            'what3words': words,
            'w3w_url': w3wurl,}
    geo = {'as_of': tim,
           'location': geotag}
    return geo

def provision_weather_data():
    # Get weather data
    g = provision_geo_data()
    lat = g['location']['latitude']
    lng = g['location']['longitude']
    forecast = forecastio.load_forecast(forecastio_key, lat, lng)
    point = forecast.currently()
    day = forecast.daily()
    current = {'cur_icon': point.icon,
               'cur_sum': point.summary,
               'cur_temp': point.temperature,
               'cur_chance': point.precipProbability}
    daily = {'day_icon': day.data[0].icon,
             'day_summary': day.data[0].summary,
             'day_high': day.data[0].temperatureMax,
             'day_low': day.data[0].temperatureMin,
             'day_chance': day.data[0].precipProbability}

    # Put it all together
    weather_data = {'currently': current,
            'daily': daily
            }
    data = dict(g.items() + weather_data.items())
    return data

