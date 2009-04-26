# Brian Cottingham
# 2009-04-14
# Simple morse code conversion. Does not handle Unicode (not that morse code does, either)


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
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    " ": "  ",
    "?": "..--..",
    "!": "-.-.--",
    ".": ".-.-.-",
    ",": "--..--",
    "'": ".----.",
    "/": "-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    "&": ".-...",
    ":": "---...",
    ";": "-.-.-.",
    "=": "-...-",
    "+": ".-.-.",
    "-": "-....-",
    "_": "..--.-",
    "\"": ".-..-.",
    "$": "...-..-",
    "@": ".--.-.",
}


def encode(irc, event, s):
    '''Encodes a string into morse code'''
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
    '''Decodes a string from morse code. Relies on standard spacing of characters/words/sentences'''
    channel = event.target()
    s = ""
    codes = m.split()
    for char in codes:  # For every morse-encoded letter we were passed
        for letter in code:  # See if it matches a letter in the code dict
            if code[letter] == char:
                s += letter
                break

    irc.privmsg(channel, s)
