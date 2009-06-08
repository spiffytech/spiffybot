# Brian Cottingham
# 2009-04-14
# holds the dict of commands for our bot to handle. Also executes them. 


import calc
import help
import ircTools
import mcode
import tell
import misc
import pranks
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
    "kill": pranks.kill,
    "roulette": pranks.roulette,
    "tell": tell.tell,
    "tiny": tiny.tiny_url,
    "topics": ircTools.topics,
    "weather": weather.getWeather,
    "woot": wootoff.checkWoot,
}
