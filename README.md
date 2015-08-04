# Whereami

## What, how and why
This would be cooler if I ever went anywhere interesting.

`whereami.py` is a simple Flask (and Flask-RESTful) app that stitches together APIs from Apple's iCloud (specifically, Find My iPhone location) services and [what3words](http://what3words.com) to allow me to track and share my location, along with [Forecast.io](http://forecast.io) for weather data.

This is somewhat Apple/iOS specific, obviously. (Although the app itself runs on Linux, it is connecting to iCloud API.) I'm using Python 2.7.9; I have no idea if it works on other versions, but I know I didn't work in any Python 3 compatibility. :/

## Prerequisites
Whereami depends on [PyiCloud](https://github.com/picklepete/pyicloud) and [w3w-python-wrapper](https://github.com/what3words/w3w-python-wrapper). You'll also need an iCloud account and an Apple device with Find My iPhone enabled. Finally, you'll want to get API keys via <http://developer.what3words.com/api/> and <https://developer.forecast.io/>.

## Usage
Edit the `env.sample` to provide your relevant secret infos. This can be the basis of a `.env` file for Heroku (using the included Procfile) or passed to Docker at runtime if you prefer to roll your own container (Dockerfile included as well).

Note: In order to fetch the Find My iPhone location, you need to know your iPhone's iCloud UUID. A script `device-uuid-lookup.py` is included here for discovering that via the API. With your Apple ID and password set up in your local environment, you can pass a device name to this script and it will tell you the UUID to use.

## Note
I'm publishing something here that I whipped up for my own personal use, in case it might be of wider interest. This isn't really tested or otherwise suitable in any way for prime-time or production use. "Alpha" doesn't even begin to cover it. I can't even promise that trying to use this won't injure you, your equipment, your data, or your loved ones in some way, and I can't be responsible if that happens. Also note that I included none of the `rsync` or other steps I use to put the output on a public webserver. Keep in mind that making this sort of data public as I do is not without risks—and again, if you should choose to take similar risks that is not my business.

~~Finally, I would point out that there is a known issue with the PyiCloud library not handling sessions quite right or something (I don't really quite understand the details). As a result, Apple's systems view each API connection as a login from a previously unknown location/device, and will send you a warning email about it. This is mostly harmless, but kind of annoying, and one of the reasons I don't ping the service more frequently than I do.~~ This appears fixed in more recent version of PyiCloud (YAY)!

I can't really offer any promises in the way of support with this stuff, but feel free to fork and send pull requests, file issues if you notice any, or contact me with any questions or feedback.

Thanks to @what3words for their brilliant invention, and for letting me know they like this sort of integration with their service.

## TODO/Possible roadmap next ideas
- Try for some basic maturity: exception handling and tests
- Integrate with Twitter API to allow regular updates of profile location with w3w address
- ~~"Live" webservice that returns `gps.json` on request, instead of printing to static file (I'd have to host elsewhere than tilde).~~ Done!
- ~~Leverage this to automate geotagging in [Jot](https://github.com/yagermadden/jot)~~ Done!
- Create a template to render an HTML version
- CLI version