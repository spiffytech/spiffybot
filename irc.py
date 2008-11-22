import socket

class irc():
    def __init__(self, nick, network, port, hostName, serverName, realName, channel):
        self.nick = nick
        global chat
        chat = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        chat.connect (( network, port ))
        chat.recv ( 4096 )
        chat.send ( 'NICK ' + nick + '\r\n' )
        chat.send ( 'USER ' + nick + " " + hostName + " " + serverName + " " + ' :' + realName + " " + '\r\n' )
        self.join(channel)



    def send(self, destination, reply, nick=""):
        print "self.nick = " + self.nick
        if not nick == "": #Default is no nick to respond to. If for some reason we should respond to a specific nick...
            chat.send ( 'PRIVMSG ' +  destination + ' :' + nick + ': ' + reply + '\r\n' )
        else:
            chat.send ( 'PRIVMSG ' +  destination + ' :' + reply + '\r\n' )



    #Join a channel
    def join(self, channel):
        chat.send ( 'JOIN ' + channel + '\r\n' ) 



    #Get the next message from the server
    def getMsg(self):
        while not locals().has_key("message"):
            print "waiting..."
            data = chat.recv(4096) #Get message from the server
            print "got data"

            #Occasionally respond to connection check by IRC server
            if data.find ( 'PING' ) != -1: #receive "ping"
                chat.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' ) #respond "pong"

            #If the server sends us a "real" message:
            elif data.find ( 'PRIVMSG' ) != -1:
                message = ':'.join ( data.split ( ':' ) [ 2: ] )
                message = message[0:-2] #IRC messages end with \r\n

                sender = data.split ( '!' ) [ 0 ].replace ( ':', '' ) #Nick that sent the message
                destination = ''.join ( data.split ( ':' ) [ :2 ] ).split ( ' ' ) [ -2 ] #Message the channel came from

        if message.find("VERSION"):
            print "data = " + data
        return [message, sender, destination]
