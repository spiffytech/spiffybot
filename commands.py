# Brian Cottingham
# 2009-04-14
# Holds the dict of commands for our bot to handle. Also executes them. 

#This file is part of Spiffybot.
#
#Spiffybot is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Spiffybot is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Spiffybot.  If not, see <http://www.gnu.org/licenses/>.

import calc
import help
import ircTools
import mcode
import tell
import misc
import roulette
import stocks
import tiny
import weather
import wootoff

cmds = {
    "ask": tell.tell,
    "calc": calc.calc,
    "encode": mcode.encode,
    "decode": mcode.decode,
    "fact": misc.trivia,
    "help": help.help,
    "quote": stocks.quote,
    "remind": tell.tell,
    "roulette": roulette.roulette,
    "tell": tell.tell,
    "tiny": tiny.tiny_url,
    "topics": ircTools.topics,
    "weather": weather.getWeather,
    "woot": wootoff.checkWoot,
}
