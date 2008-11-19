import os
import socket

#Connection vars
botNick = "spiffybot"
hostName = "My Machine"
serverName= "BotLand"
realName = "Mr. Bot Dude"
#channelList = ["#bottest", "#ncsulug", "#nilbus"]
channelList = ["#bottest"]
network = 'irc.freenode.net'
port = 6667


def getNick(message):
    return message.split ( '!' ) [ 0 ].replace ( ':', '' ) 



def getDest(message):
    return ''.join ( message.split ( ':' ) [ :2 ] ).split ( ' ' ) [ -2 ]



def connect(): #Connect to server
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



def main():
    connect()
    #Message reading loop
    while True:
        data = irc.recv ( 4096 ) # Get data from server

        #Occasionally respond to connection check
        if data.find ( 'PING' ) != -1: 
            irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )

        #Real message!
        elif data.find ( 'PRIVMSG' ) != -1:
            message = ':'.join ( data.split ( ':' ) [ 2: ] )
            message = message[0:-2] #IRC messages end with \r\n
            if message[0] == "!" or message[0:len(botNick)] == botNick: #Command for bot
                nick = getNick(data)
                destination = getDest(data)

                #Parse command from message
                if message[0] == "!": #!calc 2*2
                    command = message.partition(" ")[0].partition("!")[2]
                    args = message.partition(" ")[2]
                elif message[0:len(botNick)] == botNick: #spiffybot, calc 2*2
                    if message[len(botNick)] == ",":
                        splitter = ", "
                    elif message[len(botNick)] == "-": #spiffybot- calc 2*2
                        splitter = "- "
                    elif message[len(botNick)] == " ": #spiffybot calc 2*2
                        splitter = " "
                    elif message[len(botNick)] == ":": #spiffybot: calc 2*2
                        splitter = ":"

                    command = message.partition(splitter)[2].partition(" ")[0]
                    args = message.partition(splitter)[2].partition(" ")[2]


                #Run the specified command
                reply = runCommand(command, args)

                #Send the final reply
                if not locals().has_key("reply"):
                    reply = "whatever"
                irc.send ( 'PRIVMSG ' +  destination + ' :' + nick + ': ' + reply + '\r\n' )


def runCommand(command, args):
    if command == "help":
        reply = "No commands"

    elif command == "ip":
        reply = socket.gethostbyname(socket.gethostname())
        
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
