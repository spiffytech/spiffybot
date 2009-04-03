import mcode
import pranks
import tiny
import weather
import wootoff

cmds = {
    "encode": mcode.encode,
    "decode": mcode.decode,
    "kill": pranks.kill,
    "tiny": tiny.tiny_url,
    "weather": weather.getWeather,
    "woot": wootoff.checkWoot,
}
