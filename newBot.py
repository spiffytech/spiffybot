import irclib

# Connection information
network = 'irc.freenode.net'
port = 6667
channel = '#bottest'
nick = 'spiffybot'
realName = 'spiffybot'

def main():
    # Create an IRC object
    irc = irclib.IRC()
#    irclib.DEBUG = True

    # Create a server object, connect and join the channel
    server = irc.server()
    server.connect(network, port, nick, ircname = realName)
    server.join(channel)

    # Add event handlers
    irc.add_global_handler("pubmsg", gotMessage)
    irc.add_global_handler("privmsg", gotMessage)

    # Jump into an infinite loop
    irc.process_forever()


def gotMessage(connection, event):
    sender = event.source().split("!")[0]
    eventArgs = event.arguments()[0].split()
    if eventArgs[0].startswith(nick):
        command = eventArgs[1]
        args = eventArgs[2:]  # Inexplicably, this will never throw an index-out-of-range error
        print eventArgs
commands = {

}


if __name__ == "__main__":
    main()
