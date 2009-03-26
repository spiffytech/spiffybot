#This program is licensed under the GNU GPLv3
#Copyright Brian Cottingham <spiffytech@gmail.com>
#Version 0.2- Now uses IRC module

import re
import os
import socket
from optparse import OptionParser

import commands
import weather
import irc
import mcode
import wootoff
import utils


#Connection vars
botNick = "spiffybot"
hostName = "My Machine"
serverName= "BotLand" #Nickname for origin of connection (your house's network)
realName = "Mr. Bot Dude" #Shows up under whois
channelList = ["#ncsulug", "#nilbus", "#bottest"]
#channelList = ["#bottest"] #List of channels to connect to at startup
network = 'irc.freenode.net' #IRC server to connect to
port = 6667 #Connection port



def main():
    #Parse command-line arguments
#    parser = OptionParser(prog='client')
#    parser.add_option("--botnick", dest = "botNick", action="store")
#    options, args = parser.parse_args()
#    print botNick
#    print options
#    print args
    
    chat = irc.irc(botNick, network, 6667, hostName, serverName, realName, channelList[0], debug=0)
#    for channel in range(1, len(channelList)):
#        chat.send("/join %s" % channel)
#    chat.send(channelList[0], "Greetings, mortal.")
    # Message reading loop
    while True:
        data = chat.getMsg()  # Get message from server
        message = data[0]
        nick = data[1]
        destination = data[2]

        # Check woot.com for a change
        woot = wootoff.checkWoot()
        if woot != "" and not (message.startswith(botNick) or message.startswith("!")):  # Only print if woot updates, and this isn't an explicit woot command call
            chat.send(destination, woot, "")

        # Parse command from message
        if message.startswith("!"):  # !calc 2*2
            command = message.partition(" ")[0].partition("!")[2]
            args = message.partition(" ")[2]
        elif message.startswith(botNick):  # Message starts with bot name
            command = message.partition(" ")[2].partition(" ")[0]
            args = message.partition(" ")[2].partition(" ")[2]

        # Run the specified command
        if locals().has_key("command"):
            reply = runCommand(command, args)
        # Send the final reply
        if locals().has_key("reply"):  # Just in case...
            chat.send(destination, reply, nick)
            del reply, command, args

def runCommand(command, args):
    command = command.lower()

    if command == "ip":
        reply = commands.getIP(args)
    elif command == "load":
        reply = commands.getLoad()
    elif command == "who":
        reply = os.popen("who").read()
    elif command == "whois":
        reply = commands.whoIs()
    elif command == "encode":
        reply = mcode.encode(args)
    elif command == "decode":
        reply = mcode.decode(args)
    elif command == "weather":
        reply = weather.getWeather(args)
    elif command == "woot":
        reply = wootoff.checkWoot(force=True)
    
    else:
        reply = "Maybe."

    return reply

try: 
    main()
except KeyboardInterrupt: 
    print "Exiting..."
