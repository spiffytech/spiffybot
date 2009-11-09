# Brian Cottingham
# Originally created 2009-04-14
# Simple morse code conversion. Does not handle Unicode (not that morse code does, either)

#This file is part of Spiffybot.
#
#Spiffybot is free software: you can redistribute it and/or modify
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
#along with Spiffybot.  If not, see <http://www.gnu.org/licenses/>.


code = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
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
    " ": "",  # Official Morse Code for a space is two spaces, but that's hard to program with
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


def encode(event):
    '''Encodes a string into morse code'''
    encoded = ""
    for letter in event.args: 
        if letter.isalpha():  # Spaces and symbols shouldn't be lowered
            letter = letter.lower()  
        try:
            encoded += code[letter] + " "
        except:
            encoded += letter

    encoded = encoded.strip()  # Strip the space off the end from the last iteration of the conversion loop
    event.reply(encoded)



def decode(event):
    '''Decodes a string from morse code. Relies on standard spacing of characters/words/sentences'''
    decoded = ""
    codes = event.args.split(" ")  # Must specify a space to convert back spaces between words
    for char in codes:  # For every morse-encoded letter we were passed
        for letter in code:  # See if it matches a letter in the code dict
            if char == "":  # Space between words splits to empty string
                decoded += " "                
                break
            elif code[letter] == char:
                decoded += letter
                break
    event.reply(decoded)
