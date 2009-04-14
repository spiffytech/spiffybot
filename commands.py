# Brian Cottingham
# 2009-04-14
# holds the dict of commands for our bot to handle. Also executes them. 


import calc
import ircTools
import mcode
import misc
import pranks
import tiny
import weather
import wootoff

cmds = {
    "calc": calc.calc,
    "encode": mcode.encode,
    "decode": mcode.decode,
    "fact": misc.trivia,
    "kill": pranks.kill,
    "roulette": pranks.roulette,
    "tiny": tiny.tiny_url,
    "topics": ircTools.topics,
    "weather": weather.getWeather,
    "woot": wootoff.checkWoot,
}
