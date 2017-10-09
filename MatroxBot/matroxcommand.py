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
        return "Opened " + command.commandArgs[0]

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
            flattenMessage = " ".join(command.commandArgs[0:])
            return announceMgr.AnnouncementManager.Instance().addAnnouncementMessage(flattenMessage)

    @staticmethod
    def RunCommand(passedCommand):
        if passedCommand.commandName != "":
            #Get command from commands map
            #command = command[passedCommand]
            #return invoke command

            if passedCommand.commandName == "playsong":
              return MatroxCommandManager.SpotifyPlaySongCommand(passedCommand)
            if passedCommand.commandName == "generic":
               return MatroxCommandManager.PlayGeneric(passedCommand.commandArgs)
            if passedCommand.commandName == "addannouncement":
               return MatroxCommandManager.AddAnnouncement(passedCommand)

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

