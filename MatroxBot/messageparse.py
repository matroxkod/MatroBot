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
            #Check if we need to create a generic
            cm = MatroxCommand.MatroxCommandManager()
            if cm.isGenericCommand(command):
                newCommand = MessageParser.formatGenericPlay(command)
            else:
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

    @staticmethod
    def formatGenericPlay(command):
        #Format as usable generic
        return MatroxCommand.MatroxCommand("generic", command)
