#Command Class to house command and args
#import webbrowser
import time
import subprocess
import os
from permissionsmanager import PermissionLevel
from announcementmanager import AnnouncementManager
from utility import Utility
#Note that this requires VLC 64-bit installed given Python 2.7.x 64-bit is installed
import vlc
import operator

class MatroxCommand:

    def __init__(self, command = "", args = [], commandPermissionLevel = PermissionLevel.base):
        self.commandName = command
        self.commandArgs = args
        self.commandPermissionLevel = commandPermissionLevel


#Command Manager
class MatroxCommandManager:
    
    @staticmethod
    def spotifyPlaySongCommand(command):
        print("Opening " + command.commandArgs[0])
        #browserApp = 'chrome.exe'
        browserApp = 'firefox.exe'
        #browserAppPath = 'C:\Program Files (x86)\Google\Chrome\Application'
        browserAppPath = 'C:\Program Files\Mozilla Firefox'
        #webbrowser.open(command.commandArgs[0])
        #commandLine = [browserApp, '--new-window', command.commandArgs[0]]
        commandLine = [browserApp, '-new-window', command.commandArgs[0]]
        os.chdir(browserAppPath)
        process = subprocess.Popen(commandLine, executable=browserApp)
        time.sleep(10)
        process.kill()
        os.system("taskkill /f /im "+browserApp)
        return "Opened " + command.commandArgs[0]

    @staticmethod
    def playGeneric(command):
        print("Playing Generic Clip " + command)
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new("file:///resources/" + command + ".wav")
        player.set_media(media)
        player.play()
        return ""

    @staticmethod
    def addAnnouncement(command):
        if(len(command.commandArgs) > 0):
            flattenMessage = " ".join(command.commandArgs[0:])
            return AnnouncementManager.Instance().addAnnouncementMessage(flattenMessage)
    @staticmethod
    def reloadAnnouncements(command):
        return AnnouncementManager.Instance().reloadAnnouncements()

    @staticmethod
    def setAnnouncementInterval(command):
        parsed, interval = Utility.try_parse_int(command.commandArgs[0])
        if parsed:
            AnnouncementManager.Instance().announcementInterval = command.commandArgs[0]
            return u"Updated announcement interval to " + str(interval) + " seconds."
        else:
            return "Could not parse integer. Please try again."

    def runCommand(self, passedCommand):
        if passedCommand.commandName != "":
            #Get command from commands map
            #command = command[passedCommand]
            #return invoke command

            if passedCommand.commandName == "playsong":
              return self.spotifyPlaySongCommand(passedCommand)
            if passedCommand.commandName == "generic":
               return self.playGeneric(passedCommand.commandArgs)
            if passedCommand.commandName == "addannouncement":
               return self.addAnnouncement(passedCommand)
            if passedCommand.commandName == "reloadannouncements":
                return self.reloadAnnouncements(passedCommand)
            if passedCommand.commandName == "setannouncementinterval":
                return self.setAnnouncementInterval(passedCommand) 
                

    # TODO: Make commands driven by map
    commands = {"playsong" : spotifyPlaySongCommand, 
    }

    @staticmethod
    def isGenericCommand(commandName):
        commandArray = ["scott", "ring", "hype", "wrong"]
        return commandName in commandArray


    @staticmethod
    def getCommandPermissionLevel(commandName):
        modLevelCommands = ["addannouncement", "reloadannouncements", "setannouncementinterval"]
        if commandName in modLevelCommands:
            return PermissionLevel.mod
        else:
            return PermissionLevel.base

