#!/usr/bin/env python

#
#  mensabot
#
#  Copyright (c) 2010, Daniel Gasienica <daniel@gasienica.ch>
#  All rights reserved.
#

from google.appengine.ext import webapp
from waveapi import robot
from waveapi import appengine_robot_runner
from util import credentials
from util import feedparser

FEED = "https://www.gastro-app.ethz.ch/cgi-bin/menuela/feed_2.0_en_11-1.xml"

class CronHandler(webapp.RequestHandler):
    robot = None
    # override the constructor
    def __init__(self, robot):
        self.robot = robot
        webapp.RequestHandler.__init__(self)

    def get(self):
        wave = self.robot.new_wave(domain="googlewave.com", participants=["daniel.gasienica@googlewave.com",
                                                                          "wilee.lai@googlewave.com",
                                                                          "mklausmann5@googlewave.com"])
        d = feedparser.parse(FEED)
        wave.title = d.channel.description
        
        for entry in d.entries:
            wave.reply(entry.title + "\n" + entry.description + "\n\n")
        
        self.robot.submit(wave)

if __name__ == '__main__':
    assisty = robot.Robot('myRobot',
                          image_url='http://wilee-python.appspot.com/icon.png',
                          profile_url='http://wilee-python.appspot.com/')
    assisty.set_verification_token_info(credentials.VERIFICATION_TOKEN, credentials.SECURITY_TOKEN)
    assisty.setup_oauth(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET, server_rpc_base=credentials.RPC_BASE)
    appengine_robot_runner.run(assisty, debug=True, extra_handlers=[("/web/cron",
                                                                     lambda: CronHandler(assisty))])

