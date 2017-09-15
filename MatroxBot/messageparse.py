#messageparse.py
import re
import matroxcommand as MatroxCommand

class MessageParser():
    
    @staticmethod
    def loadCommandMessage(usr, msg):
        user = usr
        isCommand, command, args = MessageParser.tryParseCommand(msg)
        newCommand = MatroxCommand.MatroxCommand()
        if isCommand:
            newCommand = MatroxCommand.MatroxCommand(command, args)
            print("Got a command")
            return True, newCommand
        else:
            return False, newCommand

    @staticmethod
    def tryParseCommand(msg):
        if msg[0] == "!":
            # Split and take everything after !
            command = msg.split()[0][1:]
            # Args are any values after first argument
            args = msg.split()[1:]
            print("Command is " + command )
            #print(*args, sep=' ')
            return True, command, args
        else:
            return False, "", []

