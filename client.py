#This program is licensed under the GNU GPLv3
#Copyright Brian Cottingham <spiffytech@gmail.com>
#Version 0.1.1- Basically funtional

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
    parser = OptionParser(prog='client')
    parser.add_option("--botnick", dest = "botNick", action="store")
    options, args = parser.parse_args()
    print botNick
    print options
    print args
    
    connect()
    #Message reading loop
    while True:
        data = irc.recv ( 4096 ) # Get next message from server

        #Occasionally respond to connection check by IRC server
        if data.find ( 'PING' ) != -1: #receive "ping"
            irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' ) #respond "pong"

        #If the server sent us a real message:
        elif data.find ( 'PRIVMSG' ) != -1:
            message = ':'.join ( data.split ( ':' ) [ 2: ] )
            message = message[0:-2] #IRC messages end with \r\n
            if message.startswith("!") or message.startswith(botNick): #Command for bot
                nick = getNick(data) #Get nick of message sender
                destination = getDest(data) #Get channel message came from

                #Parse command from message
                if message.startswith("!"): #!calc 2*2
                    command = message.partition(" ")[0].partition("!")[2]
                    args = message.partition(" ")[2]
                elif message.startswith(botNick): #Message starts with bot name
                    command = message.partition(" ")[2].partition(" ")[0]
                    args = message.partition(" ")[2].partition(" ")[2]


                #Run the specified command
                reply = runCommand(command, args)

                #Send the final reply
                if locals().has_key("reply"): #Just in case...
                    irc.send ( 'PRIVMSG ' +  destination + ' :' + nick + ': ' + reply + '\r\n' )


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



#Parse sending nick from a received message
def getNick(message):
    return message.split ( '!' ) [ 0 ].replace ( ':', '' ) 



#Parse sending channel from received message
def getDest(message):
    return ''.join ( message.split ( ':' ) [ :2 ] ).split ( ' ' ) [ -2 ]



#Connect to server
def connect():
    global irc
    irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    irc.connect ( ( network, port ) )
    irc.recv ( 4096 )
    irc.send ( 'NICK ' + botNick + '\r\n' )
    irc.send ( 'USER ' + botNick + " " + hostName + " " + serverName + " " + ' :' + realName + " " + '\r\n' )
    for channel in channelList:
        irc.send ( 'JOIN ' + channel + '\r\n' )
    #Send entrance banner
    irc.send ( "PRIVMSG " + channelList[0] + " :Greetings, mortal.\r\n" )



try: 
    main()
except KeyboardInterrupt: 
    print "Exiting..."
