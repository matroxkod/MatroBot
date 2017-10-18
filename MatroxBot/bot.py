# Starting point of MatroxBot
import re
import time
from messageparse import MessageParser
from matroxcommand import MatroxCommandManager
from permissionsmanager import PermissionsManager
from announcementmanager import AnnouncementManager
from chatmanager import ChatManager
from filewatcher import FileWatcher

# Make sure you prefix the quotes with an 'r'!
CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

# Start File Monitoring
FileWatcher.Instance().startFileWatcherThread()

# Open connection to the target chat
ChatManager.Instance().openChatConnection()

messageParser = MessageParser()
commandManager = MatroxCommandManager()
permissionsManager = PermissionsManager()

# Start auto announcements
AnnouncementManager.Instance().startAnnouncementThread()

while True:
    # Blocking socket receive call
    response = ChatManager.Instance().receiveMessage()
    if response == "ping":
        # We don't do anything with pings
        pass
    else:
        # Separate out username and message for further parsing
        username = re.search(r"\w+", response).group(0) # return the entire match
        message = CHAT_MSG.sub("", response)
        print(username + ": " + message)
        finalMessage = ""
        # Parse the command
        loadedCommand, command = messageParser.loadCommandMessage(username, message)
        if loadedCommand:
            # Check for permissions on commands
            allowed, finalMessage = permissionsManager.canUserRunCommand(username, command)
            if allowed:
                # Run the command
                finalMessage = commandManager.runCommand(command)
        # Display any response messages from running the command
        if(len(finalMessage) > 0):
            ChatManager.Instance().sendMessageToChat(finalMessage)
    time.sleep(1 / .5)
