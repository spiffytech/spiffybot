# -*- coding: utf-8 -*-

import re
import time
import unittest
from modules import *

class ircEvent:
    '''Dummy class to facilitate testing without actually using IRC'''
    def __init__(self, connection=None, event=None, args=None):
        self.eventType = "privmsg"
        self.nick = "spiffybot"
        self.user = "spiffytech"  # User who instigated an event (join, part, pubmsg, etc.)
        self.sender = "spiffytech"
        self.args = args
        self.channel = "#bottest"

    def reply(self, message):
        self.message = message

    def setNick(self, newNick):
        self.nick = newNick


class Calc(unittest.TestCase):
    def testCalc(self):
        '''Test the basic functionality of the calc module'''
        self.irc = ircEvent(args="2+2")
        calc.calc(self.irc)
        self.assertEqual(self.irc.message, "2 + 2 = 4")

    def testUnitConversion(self):
        self.irc = ircEvent()

        self.irc.args = "1 kilometer in meters"
        calc.calc(self.irc)
        self.assertEqual(self.irc.message, "1 kilometer = 1000 meters")

        self.irc.args = "500 yards * hertz"
        calc.calc(self.irc)
        self.assertEqual(self.irc.message, "500 yards * hertz = 457.2 m / s")

    def testInvalidInput(self):
        self.irc = ircEvent()
        self.irc.args = "I can haz cheezburgur"
        calc.calc(self.irc)
        self.assertEqual(self.irc.message, "Google doesn't think that question is worth answering")

        self.irc.args = "calc 5 herts * sticks of butter"
        calc.calc(self.irc)
        self.assertEqual(self.irc.message, "Google doesn't think that question is worth answering")

    def testHtmlFormatting(self):
        self.irc = ircEvent()
        self.irc.args = "1 stick of butter * hertz"
        calc.calc(self.irc)
        self.assertEqual(self.irc.message, "1 US stick of butter * hertz = 0.000118294118 m<sup>3</sup> / s")

class Help(unittest.TestCase):
    def test_help(self):
        self.irc = ircEvent()
        self.irc.args = ""
        help.help(self.irc)
        self.assertEqual(self.irc.message, "Commands: calc, decode, difficulty check, encode, excuse, fact, quote, roulette, tell, three cheers, tiny, topics, trivia, weather, woot")


class Mcode(unittest.TestCase):
    def testEncoding(self):
        self.irc = ircEvent()
        self.irc.args = "cows"
        mcode.encode(self.irc)
        self.assertEqual(self.irc.message, "-.-. --- .-- ...")

        self.irc.args = "Turtles 1976"
        mcode.encode(self.irc)
        self.assertEqual(self.irc.message, "- ..- .-. - .-.. . ...  .---- ----. --... -....")

        self.irc.args = "asdf$="
        mcode.encode(self.irc)
        self.assertEqual(self.irc.message, ".- ... -.. ..-. ...-..- -...-")

    def testDecoding(self):
        self.irc= ircEvent()
        self.irc.args = "-.-. --- .-- ..."
        mcode.decode(self.irc)
        self.assertEqual(self.irc.message, "cows")

        self.irc.args = "- ..- .-. - .-.. . ...  .---- ----. --... -...."
        mcode.decode(self.irc)
        self.assertEqual(self.irc.message, "turtles 1976")

        self.irc.args = ".- ... -.. ..-. ...-..- -...-"
        mcode.decode(self.irc)
        self.assertEqual(self.irc.message, "asdf$=")

    def testInvalidInput(self):
        self.irc = ircEvent()
        self.irc.args = "*"
        mcode.encode(self.irc)
        self.assertEqual(self.irc.message, "*")

        self.irc.args = "✈".decode("utf-8")
        mcode.encode(self.irc)

        mcode.decode(self.irc)
        self.assertEqual(self.irc.message, "✈".decode("utf-8"))


class TinyUrl(unittest.TestCase):
    def testTinyUrl(self):
        self.irc = ircEvent()
        self.irc.args = "google.com"
        tiny.tiny_url(self.irc)
        self.assertEqual(self.irc.message, "http://tinyurl.com/2tx")


    def testUnicodeURL(self):
        self.irc = ircEvent()
        self.irc.args = "✈".decode("utf-8")
        tiny.tiny_url(self.irc)
        self.assertEqual(self.irc.message, "Can't encode that URL, it contains unicode!")


class Stocks(unittest.TestCase):
    def testStockQuote(self):
        self.irc = ircEvent()
        self.irc.args = "siri"
        stocks.quote(self.irc)

        rematch = re.match("^SIRI \(Sirius XM Radio I\) \|\| Current price: \d+\.\d+ \|\| Change today: [\+-]{0,1}\d+\.\d+ \([\+-]{0,1}\d+\.\d+%\) \|\| 52-week low/high: \d+\.\d+ / \d+\.\d+", self.irc.message)
        self.assertTrue(rematch != None)


class Woot(unittest.TestCase):
    def testGetCurrentWoot(self):
        self.irc = ircEvent()
        wootoff.checkWoot(self.irc)

        rematch = re.match(r"^Woot! - .+ --- \$\d+\.\d{2} --- \d+\.\d+% left! --- Purchase: http://tinyurl.com/\w+$", self.irc.message)
        self.assertTrue(rematch != None)


class Weather(unittest.TestCase):
    def setUp(self):
        self.regexString = """^Weather\ for\ [A-Z][a-z -]*,\   # City
            [A-Z]{2}\                                           # State
            \(as\ of\ [A-Z][a-z]+\                              # Month
            \d{1,2},\                                           # Day
            \d:\d{2}\ [AP]M\                                    # Time
            [A-Z]+\):\                                          # Timezone
            .+                                                  # Forecast summary
        """

    def testWeather(self):
        self.irc = ircEvent()
        self.irc.args = "27607"
        weather.getWeather(self.irc)

#        rematch = re.match(r"""^Weather\ for\ [A-Z][a-z -]*,\   # City
#            [A-Z]{2}\                                           # State
#            \(as\ of\ [A-Z][a-z]+\                              # Month
#            \d{1,2},\                                           # Day
#            \d:\d{2}\ [AP]M\                                    # Time
#            [A-Z]+\):\                                          # Timezone
#            .+                                                  # Forecast summary
#        """, self.irc.message, re.VERBOSE)
        rematch = re.match(self.regexString, self.irc.message, re.VERBOSE)
        self.assertTrue(rematch != None)

    def test_easter_eggs(self):
        self.irc = ircEvent()
        self.irc.args = "1337"
        weather.getWeather(self.irc)
        self.assertEqual(self.irc.message, "f4i1!")

        self.irc.args = "20252"
        weather.getWeather(self.irc)
        self.assertTrue(self.irc.message, "Smokey the Bear says, 'Only YOU can prevent hurricanes!'")


if __name__ == "__main__":
    unittest.main()
