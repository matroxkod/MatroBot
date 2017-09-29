# bot.py
import cfg
import socket
import re
import time
import messageparse as messageParser
import matroxcommand as commandManager
import permissionsmanager as permissionsMgr
import announcementmanager as announceManager

# Make sure you prefix the quotes with an 'r'!
CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

# network functions go here

s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

mp = messageParser.MessageParser()
cm = commandManager.MatroxCommandManager()
pm = permissionsMgr.PermissionsManager()

# start auto message

#announceManager.AnnouncementManager().loadAnnouncements()

while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", response).group(0) # return the entire match
        message = CHAT_MSG.sub("", response)
        print(username + ": " + message)
        # Parse the command
        loadedCommand, command = mp.loadCommandMessage(username, message)
        if loadedCommand:
            allowed, spamMsg = pm.checkSpam(username)
            if allowed:
                print("Running command")
                cm.RunCommand(command)
            else:
                print(spamMsg)
                s.send("PRIVMSG {} :{}\r\n".format(cfg.CHAN, spamMsg).encode("utf-8"))
                #chat(s, spamMsg)
    time.sleep(1 / .5)

@staticmethod
def chat(sock, msg):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    sock.send("PRIVMSG #{} :{}".format(cfg.CHAN, msg))

def ban(sock, user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    sock -- the socket over which to send the ban command
    user -- the user to be banned
    """
    chat(sock, ".ban {}".format(user))

def timeout(sock, user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments:
    sock -- the socket over which to send the timeout command
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    chat(sock, ".timeout {}".format(user, secs))
