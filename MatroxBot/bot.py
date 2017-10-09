# bot.py
import re
import time
import messageparse as messageParser
import matroxcommand as commandManager
import permissionsmanager as permissionsMgr
import announcementmanager as announceManager
from chatmanager import ChatManager

# Make sure you prefix the quotes with an 'r'!
CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

# network functions go here
ChatManager.Instance().openChatConnection()

mp = messageParser.MessageParser()
cm = commandManager.MatroxCommandManager()
pm = permissionsMgr.PermissionsManager()

# start auto message
announceManager.AnnouncementManager.Instance().startAnnouncementThread()

while True:
    response = ChatManager.Instance().receiveMessage()
    if response == "ping":
        pass
    else:
        username = re.search(r"\w+", response).group(0) # return the entire match
        message = CHAT_MSG.sub("", response)
        print(username + ": " + message)
        finalMessage = ""
        # Parse the command
        loadedCommand, command = mp.loadCommandMessage(username, message)
        if loadedCommand:
            allowed, finalMessage = pm.canUserRunCommand(username, command)
            if allowed:
                print("Running command")
                finalMessage = cm.runCommand(command)

        if(len(finalMessage) > 0):
            print(finalMessage)
            ChatManager.Instance().sendMessageToChat(finalMessage)
    time.sleep(1 / .5)