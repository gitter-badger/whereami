# Whereami

## What, how and why
This would be cooler if I ever went anywhere interesting. See it in operation at <http://tilde.club/~tym/loc/whereami.html>.

`whereami.py` is an abecedarian python script that stitches together APIs from Apple's iCloud (specifically, Find My iPhone location) services and [what3words](http://what3words.com) to allow me to track and share my location.

In particular, I am serving my location data from <http://tilde.club> which by design serves static content only—and anyway I am not interested in collecting these data at exceedingly fine granularity. So the script writes JSON to a file on disk, and I trigger it from cron every 9 minutes. I also have a HTML page (`whereami.html`) with a bit of jQuery code that parses the JSON output in the browser and presents it in a human-readable way, with links to maps.

This is all Apple/Mac/iOS specific, obviously. I'm using Python 2.7.9; I have no idea if it works on other versions, but I know I didn't work in any Python 3 compatibility. :/

## Prerequisites
Whereami depends on [PyiCloud](https://github.com/picklepete/pyicloud) and [w3w-python-wrapper](https://github.com/what3words/w3w-python-wrapper). You'll also need an iCloud account and an Apple device with Find My iPhone enabled. Finally, you'll want to get a what3words API key via <http://developer.what3words.com/api/>.

## Usage
There are a couple of lines to be edited near the top of `whereami.py` to provide your Apple ID and the UUID for your device. (The PyiCloud README explains how to use the iCloud API `devices` method to discover your UUID. Note this is not the same as UDID.)

The script also presumes that your Apple account password and what3words API key are available as environment variables, so set those.

That much should enough to allow the script to be run manually. There is also an `example_crontab` in the repository, that needs envars set properly at the top. Depending on your tastes, you might want to edit the schedule and the path to the script, as well.

`whereami.html` should work as is, but you may want or need to edit inline links, title tag, etc.

## Utility
`gps2pb.py` is small tool that grabs the JSON file and copies coordinates and w3w link to the Mac pasteboard in Markdown format. In my case, handy for providing a quick and dirty geotag to anything I happen to be working on. I keep a symlink to it in ~/bin so I can invoke it easily. You'll want to put your own URL for `gps.json` in here, as indicated in comment inline.

This should also, I hope, serve as an example of the general idea of how having a JSON file with my coordinates on the Internet can be interesting and useful. I also use this to fetch local weather data from <http://forecast.io>, but my coordinates in my bash prompt, etc.

## Note
I'm publishing something here that I whipped up for my own personal use, in case it might be of wider interest. This isn't really tested or otherwise suitable in any way for prime-time or production use. "Alpha" doesn't even begin to cover it. I can't even promise that trying to use this won't injure you, your equipment, your data, or your loved ones in some way, and I can't be responsible if that happens. Also note that I included none of the `rsync` or other steps I use to put the output on a public webserver. Keep in mind that making this sort of data public as I do is not without risks—and again, if you should choose to take similar risks that is not my business.

Finally, I would point out that there is a known issue with the PyiCloud library not handling sessions quite right or something (I don't really quite understand the details). As a result, Apple's systems view each API connection as a login from a previously unknown location/device, and will send you a warning email about it. This is mostly harmless, but kind of annoying, and one of the reasons I don't ping the service more frequently than I do.

I can't really offer any promises in the way of support with this stuff, but feel free to fork and send pull requests, file issues if you notice any, or contact me with any questions or feedback.

Thanks to @what3words for their brilliant invention, and for letting me know they like this sort of integration with their service.

## TODO/Possible roadmap next ideas
- Try for some basic maturity: exception handling and tests
- General refactor for library/module use
- Move account configuration to separate .ini or YAML file
- Integrate with Twitter API to allow regular updates of profile location with w3w address
- "Live" webservice that returns `gps.json` on request, instead of printing to static file (I'd have to host elsewhere than tilde).
