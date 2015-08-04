#!/usr/bin/env
#coding: utf-8

import os
from pyicloud import PyiCloudService
from argparse import ArgumentParser

# FU requests and your vended urllib3
import requests
requests.packages.urllib3.disable_warnings()

apple_id = os.getenv('APPLE_ID')
icloudpass = os.getenv('ICLOUDPASSWORD').replace('\"', '')

def main():
    parser = ArgumentParser()

    parser.add_argument(
            'devicename',
            help='The name of your iPhone (in Settings->\
                General->About-> Name)'
        )
    args = parser.parse_args()

    api = PyiCloudService(apple_id, icloudpass)
    dev = args.devicename
    dev_id = ''
    for d in api.devices:
        n = d['name']
        if n == dev:
            dev_id = d['id']

    if dev_id:
        print "The UUID of your device is: %s" % dev_id
    else:
        print "No device by that name found. Please check the spelling and try again."

if __name__ == '__main__':
    main()