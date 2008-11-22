#This program is licensed under the GNU GPLv3
#Copyright Brian Cottingham <spiffytech@gmail.com>
#Version 0.2- Now uses IRC module

import irc
import re
import os
import socket
from optparse import OptionParser

#Connection vars
botNick = "spiffybot"
hostName = "My Machine"
serverName= "BotLand" #Nickname for origin of connection (your house's network)
realName = "Mr. Bot Dude" #Shows up under whois
#channelList = ["#bottest", "#ncsulug", "#nilbus"]
channelList = ["#bottest"] #List of channels to connect to at startup
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
    
    chat = irc.irc("spiffybot", "irc.freenode.net", 6667, "here", "place", "me", "#bottest", debug=1)
    chat.send("#bottest", "Greetings, mortal.")
    #Message reading loop
    while True:
        data = chat.getMsg() #Get message from server
        message = data[0]
        nick = data[1]
        destination = data[2]

        #Parse command from message
        if message.startswith("!"): #!calc 2*2
            command = message.partition(" ")[0].partition("!")[2]
            args = message.partition(" ")[2]
        elif message.startswith(botNick): #Message starts with bot name
            command = message.partition(" ")[2].partition(" ")[0]
            args = message.partition(" ")[2].partition(" ")[2]

        #Run the specified command
        if locals().has_key("command"):
            reply = runCommand(command, args)

        #Send the final reply
        if locals().has_key("reply"): #Just in case...
            chat.send(destination, reply, nick)
            del reply, command, args


def runCommand(command, args):
    if command == "help":
        reply = "No commands"

    elif command == "ip":
        interface = args

        ifconfig = os.popen("/sbin/ifconfig").read().split("\n")

        found = 0
        for line in range(0, len(ifconfig)):
            if ifconfig[line].find(interface) != -1:
                found = 1
                break

        if found == 0:
            reply = "no such interface"
            print "args =", args
        else:
            ip = re.findall("addr:\d+.\d+.\d+.\d+", ifconfig[line+1])
            print "ip = " + str(ip)
            if len(ip) != 0:
                reply = ip[0].partition(":")[2] 
                print "reply = " + reply
            else:
                reply = "No IP on that interface"
        
    elif command == "load":
        uptime = os.popen("uptime").read()
        reply = " ".join(uptime.split(" ")[9:])

    elif command == "who":
        reply = os.popen("who").read().split(" ")[0]

    else:
        reply = "no such command"
    return reply



try: 
    main()
except KeyboardInterrupt: 
    print "Exiting..."
