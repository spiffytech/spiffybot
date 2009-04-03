import mcode
import tiny
import weather
import wootoff

cmds = {
    "encode": mcode.encode,
    "decode": mcode.decode,
    "tiny": tiny.tiny_url,
    "weather": weather.getWeather,
    "woot": wootoff.checkWoot,
}
