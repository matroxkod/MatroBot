# cfg.py
import secrets

HOST = "irc.twitch.tv"              # the Twitch IRC server
PORT = 6667                         # always use port 6667!
NICK = secrets.NICK                 # your Twitch username, lowercase
PASS = secrets.PASS                 # your Twitch OAuth token
CHAN = secrets.CHAN                 # the channel you want to join
RATE = (20/30) # messages per second

# Secrets file should be of the following format:
# NICK = "NAMEOFBOT"
# PASS = "OATH:KEY"
# CHAN = "#YOUCHANNELNAME" 
