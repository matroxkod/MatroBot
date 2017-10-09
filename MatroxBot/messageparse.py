#messageparse.py
import re
from matroxcommand import MatroxCommand
from matroxcommand import MatroxCommandManager
class MessageParser():
    
    def loadCommandMessage(self, usr, msg):
        user = usr
        isCommand, command, args = MessageParser.tryParseCommand(msg)
        newCommand = MatroxCommand()
        if isCommand:
            #Check if we need to create a generic
            cm = MatroxCommandManager()
            if cm.isGenericCommand(command):
                newCommand = self.formatGenericPlay(command)
            else:
                newCommand = MatroxCommand(command, args)
            newCommand.commandPermissionLevel = cm.getCommandPermissionLevel(newCommand.commandName)
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
        return MatroxCommand("generic", command)