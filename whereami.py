#!/usr/bin/env python
# coding: utf-8

from flask import Flask
from flask_restful import Resource, Api
from flask_slack import Slack
import os

from remotes import provision_geo_data, provision_weather_data

# Mac OS certs: still hard (comment out before linux deploy)
import requests
requests.packages.urllib3.disable_warnings()


# Intantiate app
app = Flask(__name__)
api = Api(app)
slack = Slack(app)

slack_token = os.getenv('SLACKTOKEN')
slack_team = os.getenv('SLACKTEAM')
hook_url = os.getenv('HOOKURL')

# API Classes
class WhereAmI(Resource):
    def get(self):
        location = provision_geo_data()
        return location

api.add_resource(WhereAmI,
     '/',
     '/where')

class CurrentWeather(Resource):
    def get(self):
        data = provision_weather_data()
        current_keys = ['as_of', 'currently']

        weather = dict([(i, data[i]) for i in current_keys if i in data])
        return weather

api.add_resource(CurrentWeather,
     '/weather')

class TodayWeather(Resource):
    def get(self):
        data = provision_weather_data()
        daily_keys = ['as_of', 'daily']

        today = dict([(i, data[i]) for i in daily_keys if i in data])
        return today

api.add_resource(TodayWeather,
     '/forecast')

class FullMeta(Resource):
    def get(self):
        meta = provision_weather_data()
        return meta

api.add_resource(FullMeta,
    '/meta')

# Slash commands for Slackbot
@slack.command('where', token=slack_token,
               team_id=slack_team, methods=['POST'])
def whereami(**kwargs):
    geo = provision_geo_data()['location']
    w3w = geo['w3w_url']
    words = geo['what3words']
    lat = geo['latitude']
    lng = geo['longitude']

    locload = '<%s|%s>  \n%s, %s' % (w3w, words, lat, lng)
    payload = {'text': locload}
    r = requests.post(hookurl, data=json.dumps(payload))

app.add_url_rule('/slack-where', view_func=slack.dispatch)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



