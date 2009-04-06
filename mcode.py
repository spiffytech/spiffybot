code = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..=.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-", 
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    " ": "  ",
    ".": "   ",
}
def encode(irc, event, s):
    channel = event.target()
    encoded = ""
    for letter in s: 
        letter = letter.lower()
        try:
            encoded += code[letter] + " "
        except:
            encoded += letter
    irc.privmsg(channel, encoded)



def decode(irc, event, m):
    channel = event.target()
    s = ""
    codes = m.split()
    for char in codes:  # For every morse-encoded letter we were passed
        for letter in code:  # See if it matches a letter in the code dict
            if code[letter] == char:
                s += letter
                break

    irc.privmsg(channel, s)
