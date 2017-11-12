#messageparse.py
import re
from matroxcommand import MatroxCommand
from matroxcommand import MatroxCommandManager
class MessageParser():
    
    def loadCommandMessage(self, usr, msg):
        cm = MatroxCommandManager()
        user = usr
        isCommand, command, args = self.tryParseCommand(msg)
        if not isCommand:
            isParsedWord, command = self.tryStringMatch(msg)
        newCommand = MatroxCommand()
        if isCommand:
            #Check if we need to create a generic
            if cm.isGenericCommand(command):
                newCommand = cm.formatGenericPlay(command)
            else:
                newCommand = MatroxCommand(command, args)
            newCommand.commandPermissionLevel = cm.getCommandPermissionLevel(newCommand.commandName)
            print("Got a command")
            return True, newCommand
        else:
            if isParsedWord:
                #TODO Update for better handling
                if cm.isAllowOnceCommand(command):
                    newCommand = MatroxCommand(command, "")
                newCommand.commandPermissionLevel = cm.getCommandPermissionLevel(newCommand.commandName)
                return True, newCommand
            return False, newCommand

    @staticmethod
    def tryParseCommand(msg):
        if msg[0] == "!":
            # Split and take everything after !
            command = msg.split()[0][1:].lower()
            # Args are any values after first argument
            args = msg.split()[1:]
            print("Command is " + command.lower() )
            #print(*args, sep=' ')
            return True, command, args
        else:
            return False, "", []

    @staticmethod
    def tryStringMatch(msg):
        helloArray = ["hi", "hello", "hey", "howdy", "yo"]
        for word in msg.split():
            word = word.lower()
            if(word in helloArray):
                # Match the command
                return True, "hellofriendonce"
            else:
                return False, ""

