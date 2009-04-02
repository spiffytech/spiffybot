import mcode
import tiny
import weather
import wootoff

commands = {
    "encode": mcode.encode,
    "decode": mcode.decode,
    "weather": weather.getWeather,
    "woot": wootoff.checkWoot,
}
