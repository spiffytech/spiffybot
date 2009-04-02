import socket

class irc():
    def __init__(self, nick, network, port, hostName, serverName, realName, channel, debug=0):
        self.nick = nick
        self.debug = debug
        global chat
        chat = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        chat.connect (( network, port ))
        chat.recv ( 4096 )
        chat.send ( 'NICK ' + nick + '\r\n' )
        chat.send ( 'USER ' + nick + " " + hostName + " " + serverName + " " + ' :' + realName + " " + '\r\n' )
        self.join(channel)

    def send(self, destination, reply, nick=""):
        '''Sends a message to the server, optionally triggering a nick highlight'''
        if not nick == "":  # Default is no nick to respond to. If for some reason we should respond to a specific nick...
            chat.send ( 'PRIVMSG ' +  destination + ' :' + nick + ': ' + reply + '\r\n' )
        else:
            chat.send ( 'PRIVMSG ' +  destination + ' :' + reply + '\r\n' )

    def printData(self):
        print self.nick, self.debug

    def join(self, channel):
        ''' Join a channel'''
        chat.send ( 'JOIN ' + channel + '\r\n' ) 

    def part(self, channel):
        '''Leave a channel'''
        chat.send( "PART " + channel + "\r\n")

    # Get the next message from the server
    def getMsg(self):
        '''Gets the next message from the server'''
        while not locals().has_key("message"):
            if self.debug == 1:
                print "waiting..."
            data = chat.recv(4096)  # Get message from the server
            if self.debug == 1:
                print "got data"

            # Occasionally respond to connection check by IRC server
            if data.find ( 'PING' ) != -1:  # receive "ping"
                chat.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' ) #respond "pong"

            # If the server sends us a "real" message:
            elif data.find ( 'PRIVMSG' ) != -1:
                message = ':'.join ( data.split ( ':' ) [ 2: ] )
                message = message[0:-2]  # IRC messages end with \r\n

                sender = data.split ( '!' ) [ 0 ].replace ( ':', '' )  # Nick that sent the message
                destination = ''.join ( data.split ( ':' ) [ :2 ] ).split ( ' ' ) [ -2 ]  # Message the channel came from

        return [message, sender, destination]
