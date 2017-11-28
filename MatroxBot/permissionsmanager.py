#permissionsmanager.py
# Keeps track of users sending commands to ensure no user is spamming bot
# Keeps track of user permissions
import datetime

class PermissionLevel:
    mod = 0
    base = 1
    override = 2
    allowOnce = 3

class User:

    def __init__(self, name = "", nextReplyTime = datetime.datetime.now().time(), permissionlevel = PermissionLevel.base):
        self.name = name
        self.nextReplyTime = nextReplyTime
        self.permissionLevel = permissionlevel
        self.allowOnceCommands = {}

class PermissionsManager:

    knownUsers = {}
    modUsers = {"matroxkod"}

    # Check if the user can run the command
    def canUserRunCommand(self, usrName, command):
        # Check if user is spamming
        notSpam, spamMsg = self.checkSpam(usrName, command)
        if (notSpam):
            # Check if user has permission to run the command
            if(self.checkCommandPermissions(usrName, command)):
                return True, ""
            else:
                return False, usrName + " is not allowed to run that command."
        else:
            return False, spamMsg

    # Checks if the user is allowed to run the command
    def checkCommandPermissions(self, usrName, command):
        # Check if command is a mod level command
        if(command.commandPermissionLevel == PermissionLevel.mod):
            return self.isModUser(usrName)
        else:
            return True

    def checkSpam(self, usrName, command):
        # Store when command was received
        receivedTime = datetime.datetime.now().time()
        
        # Check if we have the user already
        if usrName not in self.knownUsers:
            # Create the user and store it
            newUsr = User(usrName, datetime.datetime.now().time())
            if(self.isModUser(usrName)):
                newUsr.permissionLevel = PermissionLevel.mod
            self.updateUserTime(usrName, newUsr, 2)
            if(command.commandPermissionLevel == PermissionLevel.allowOnce):
                newUsr.allowOnceCommands[command.commandName] = True
            print("Added new user " + newUsr.name)
            return True, ""
        else:
            user = self.knownUsers[usrName]
            print(u"Pulled user " + user.name + " nextReply:" + str(user.nextReplyTime) + " received:" + str(receivedTime) )
            # Check is user has used allow once commands already
            if command.commandPermissionLevel == PermissionLevel.allowOnce:
                if command.commandName not in user.allowOnceCommands:
                    # User has not used the command
                    user.allowOnceCommands[command.commandName] = True
                    return True, ""
                else:
                    return not user.allowOnceCommands[command.commandName], ""

            # Check if the user is allowed to post
            if receivedTime > user.nextReplyTime:
                self.updateUserTime(usrName, user, 4)
                return True, ""
            else:
                self.updateUserTime(usrName, user, 8)
                return False, usrName + ": Please wait several seconds before attempting to issue another command."

    def addSecs(self, time, second):
        date = datetime.datetime(100, 1, 1, time.hour, time.minute, time.second)
        date = date + datetime.timedelta(seconds=second)
        return date.time()

    def updateUserTime(self, userName, user, timeToAdd):
        user.nextReplyTime = self.addSecs(datetime.datetime.now().time(), timeToAdd)
        self.knownUsers[userName] = user 

    def isModUser(self, userName):    
        if(userName in self.modUsers):
            return True
        else:
            return False