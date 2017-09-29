#permissionsmanager.py
# Keeps track of users sending commands to ensure no user is spamming bot
import datetime

class User:

    def __init__(self, name = "", nextReplyTime = datetime.datetime.now().time()):
        self.name = name
        self.nextReplyTime = nextReplyTime

class PermissionsManager:

    knownUsers = {}

    def checkSpam(self, usrName):
        # Store when command was received
        receivedTime = datetime.datetime.now().time()
        
        # Check if we have the user already
        if usrName not in self.knownUsers:
            # Create the user and store it
            newUsr = User(usrName, datetime.datetime.now().time())
            self.updateUserTime(usrName, newUsr, 2)
            print("Added new user " + newUsr.name)
            return True, ""
        else:
            user = self.knownUsers[usrName]
            print(u"Pulled user " + user.name + " nextReply:" + str(user.nextReplyTime) + " received:" + str(receivedTime) )
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
