import mcode
import tiny
import weather
import wootoff

cmds = {
    "encode": mcode.encode,
    "decode": mcode.decode,
    "weather": weather.getWeather,
    "woot": wootoff.checkWoot,
}
