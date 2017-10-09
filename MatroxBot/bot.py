# bot.py
import re
import time
from messageparse import MessageParser
from matroxcommand import MatroxCommandManager
from permissionsmanager import PermissionsManager
from announcementmanager import AnnouncementManager
from chatmanager import ChatManager

# Make sure you prefix the quotes with an 'r'!
CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

# network functions go here
ChatManager.Instance().openChatConnection()

messageParser = MessageParser()
commandManager = MatroxCommandManager()
permissionsManager = PermissionsManager()

# start auto message
AnnouncementManager.Instance().startAnnouncementThread()

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
        loadedCommand, command = messageParser.loadCommandMessage(username, message)
        if loadedCommand:
            allowed, finalMessage = permissionsManager.canUserRunCommand(username, command)
            if allowed:
                print("Running command")
                finalMessage = commandManager.runCommand(command)

        if(len(finalMessage) > 0):
            print(finalMessage)
            ChatManager.Instance().sendMessageToChat(finalMessage)
    time.sleep(1 / .5)