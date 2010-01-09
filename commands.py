# Brian Cottingham
# 2009-04-14
# Holds the dict of commands for our bot to handle. Also executes them. 

#This file is part of Spiffybot.
#
#Spiffybot is free software, you can redistribute it and/or modify
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
#along with Spiffybot.  If not, see <http,//www.gnu.org/licenses/>.

anyMessage = [
    ("(?P<cmd>^(bai|goodbye|good bye|bye|shalom|farewell))(?P<args>[^a-zA-Z]*)", "misc.farewell"),
]

cmds = [
    ("(?P<cmd>^ask)(?P<args>.*)", "tell.tell"),
    ("(?P<cmd>^calc)(?P<args>.*)", "calc.calc"),
    ("(?P<cmd>^encode)(?P<args>.*)", "mcode.encode"),
    ("(?P<cmd>^decode)(?P<args>.*)", "mcode.decode"),
    ("(?P<cmd>^fact)(?P<args>.*)", "misc.trivia"),
    ("(?P<cmd>^excuse)(?P<args>.*)", "misc.excuse"),
    ("(?P<cmd>^get out)(?P<args>)", "cmdPart"),
    ("(?P<cmd>^help)(?P<args>.*)", "help.help"),
    ("(?P<cmd>^join)(?P<args>.*)", "cmdJoin"),
    ("(?P<cmd>^nick)(?P<args>.*)", "cmdNick"),
    ("(?P<cmd>^quote)(?P<args>.*)", "stocks.quote"),
    ("(?P<cmd>^remind)(?P<args>.*)", "tell.tell"),
    ("(?P<cmd>^roulette)(?P<args>.*)", "roulette.roulette"),
    ("(?P<cmd>^tell)(?P<args>.*)", "tell.tell"),
    ("(?P<cmd>^tiny)(?P<args>.*)", "tiny.tiny_url"),
    ("(?P<cmd>^topics)(?P<args>)", "ircTools.topics"),
    ("(?P<cmd>^weather)(?P<args>.*)", "weather.getWeather"),
    ("(?P<cmd>^woot)(?P<args>)", "wootoff.checkWoot"),
    ("(?P<cmd>^processes)(?P<args>.*)", "sysstats.listProcesses"),
    ("(?P<cmd>^difficulty check)(?P<args>.*)", "misc.difficultyCheck"),
    ("(?P<cmd>^roll)(?P<args>.*)", "misc.roll_dice"),
    ("(?P<cmd>^(bai|goodbye|bye|good bye|shalom))(?P<args>.*)", "misc.farewell"),
    ("(?P<cmd>^load)(?P<args>.*)", "sysstats.load"),
    ("(?P<cmd>^free)(?P<args>.*)", "sysstats.freeSpace"),
]
