# chatmanager.py
from singleton import Singleton
import cfg
import socket

# This class is designed to be the point of entry for all chat actions
@Singleton
class ChatManager:
    def __init__(self):
        self.s = socket.socket()

    # Open a chat connection
    def openChatConnection(self):
        self.s.connect((cfg.HOST, cfg.PORT))
        self.s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
        self.s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
        self.s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

    # Blocking call to the socket to receive messages
    def receiveMessage(self):
        response = self.s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            self.s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            return "ping"
        else:
            return response

    # Sends a message to everyong in the channel
    def sendMessageToChat(self, message):
        self.s.send("PRIVMSG {} :{}\r\n".format(cfg.CHAN, message).encode("utf-8"))

    # Sends a message to the chat server (not chat channel)
    def sendMessageToChatServer(self):
        self.s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

    # TODO: ban a user
    def ban(user):
        """
        Ban a user from the current channel.
        Keyword arguments:
        sock -- the socket over which to send the ban command
        user -- the user to be banned
        """
        self.sendMessageToChat(".ban {}".format(user))

    # TODO: timeout a user
    def timeout(user, secs=600):
        """
        Time out a user for a set period of time.
        Keyword arguments:
        sock -- the socket over which to send the timeout command
        user -- the user to be timed out
        secs -- the length of the timeout in seconds (default 600)
        """
        self.sendMessageToChat(".timeout {}".format(user, secs))
