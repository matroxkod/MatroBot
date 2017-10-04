#Command Class to house command and args
#import webbrowser
import time
import subprocess
import os
import permissionsmanager as permissionsMgr
import announcementmanager as announceMgr
#Note that this requires VLC 64-bit installed given Python 2.7.x 64-bit is installed
import vlc
import operator

class MatroxCommand:

    def __init__(self, command = "", args = [], commandPermissionLevel = permissionsMgr.PermissionLevel.base):
        self.commandName = command
        self.commandArgs = args
        self.commandPermissionLevel = commandPermissionLevel


#Command Manager
class MatroxCommandManager:
    
    @staticmethod
    def SpotifyPlaySongCommand(command):
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

    @staticmethod
    def PlayGeneric(command):
        print("Playing Generic Clip " + command)
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new("file:///resources/" + command + ".wav")
        player.set_media(media)
        player.play()

    @staticmethod
    def AddAnnouncement(command):
        if(len(command.commandArgs) > 0):
            announceMgr.AnnouncementManager().addAnnouncementMessage(command.commandArgs[0:])

    @staticmethod
    def RunCommand(passedCommand):
        if passedCommand.commandName != "":
            if passedCommand.commandName == "playsong":
               MatroxCommandManager.SpotifyPlaySongCommand(passedCommand)
            if passedCommand.commandName == "generic":
               MatroxCommandManager.PlayGeneric(passedCommand.commandArgs)
            if passedCommand.commandName == "addannouncement":
                MatroxCommandManager.AddAnnouncement(passedCommand)

    # TODO: Make commands driven by map
    commands = {"playsong" : SpotifyPlaySongCommand, 
    }

    @staticmethod
    def isGenericCommand(commandName):
        commandArray = ["scott", "ring", "hype", "wrong"]
        return commandName in commandArray


    @staticmethod
    def getCommandPermissionLevel(commandName):
        modLevelCommands = ["addannouncement"]
        if commandName in modLevelCommands:
            return permissionsMgr.PermissionLevel.mod
        else:
            return permissionsMgr.PermissionLevel.base

