import calc
import ircTools
import mcode
import pranks
import tiny
import weather
import wootoff

cmds = {
    "calc": calc.calc,
    "encode": mcode.encode,
    "decode": mcode.decode,
    "kill": pranks.kill,
    "tiny": tiny.tiny_url,
    "topics": ircTools.topics,
    "weather": weather.getWeather,
    "woot": wootoff.checkWoot,
}
