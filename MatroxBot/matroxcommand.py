#Command Class to house command and args
#import webbrowser
import time
import subprocess
import os
from permissionsmanager import PermissionLevel
from announcementmanager import AnnouncementManager
from utility import Utility
from mqtt import ColorManager
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

    def __init__(self):
        self.genericCommandArray = ["scott", "ring", "hype", "wrong"]
        self.commands = {'playsong' : self.spotifyPlaySongCommand, 'generic' : self.playGeneric,
        'addannouncement' : self.addAnnouncement , 'reloadannouncements' : self.reloadAnnouncements, 'setannouncementinterval' : self.setAnnouncementInterval,
        'commands' : self.listCommands, 'help' : self.listCommands, 'changecolor' : self.changeColor 
         }
        self.helpCommands = {'default' : self.runCommand, 'changecolor' : ColorManager.Instance().help, 'addannouncement' : AnnouncementManager.Instance().addAnnouncementHelp,
        'setannouncementinterval' : AnnouncementManager.Instance().setAnnouncementIntervalHelp }
    
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
        print("Playing Generic Clip " + command.commandArgs)
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new("file:///resources/" + command.commandArgs + ".wav")
        player.set_media(media)
        player.play()
        return ""

# Color Changing
    @staticmethod
    def changeColor(command):
        # Determine what kind of color change we're doing        
        if(command.commandArgs[0] in ColorManager.Instance().pulseEffectTranslations or
        command.commandArgs[0] in ColorManager.Instance().colorRotateEffectTranslations):
            # Effect?
            ColorManager.Instance().changeColorEffect(command.commandArgs[0])
        elif(command.commandArgs[0][0] == "#"):
            # Hex?
            try:
                ColorManager.Instance().changeColorHex(command.commandArgs[0])
            except KeyError:
                return "Invalid hex color code enter. Please use only values 0-9 and a-f."
        else:
            # Color name
            ColorManager.Instance().changeColor(command.commandArgs[0])
        return "Changed color to "+ command.commandArgs[0]

# Announcement commands
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

# List commands    
    def listCommands(self, command):
        commandList = ""
        for individual in self.commands.keys():
            if str(individual) != 'generic':
                commandList = commandList + '!' + str(individual) + ' '
        
        for generic in self.genericCommandArray:
            commandList = commandList + '!' + str(generic) + ' '

        return commandList

    def runCommand(self, passedCommand):
        if passedCommand.commandName != "":
            #Get command from commands map
            if self.commands.has_key(passedCommand.commandName):
                # Check if the command has proper args
                needsHelp, helpCommand = self.checkHelpCommand(passedCommand)
                if(needsHelp):
                    return helpCommand()
                else:                    
                    return self.commands[passedCommand.commandName](passedCommand)
            else:
                return "I don't know that command. Type !commands for a list of available commands."           
                    
    def isGenericCommand(self, commandName):        
        return commandName in self.genericCommandArray

    @staticmethod
    def getCommandPermissionLevel(commandName):
        modLevelCommands = ["addannouncement", "reloadannouncements", "setannouncementinterval"]
        if commandName in modLevelCommands:
            return PermissionLevel.mod
        else:
            return PermissionLevel.base

    def checkHelpCommand(self, command):
        if(self.helpCommands.has_key(command.commandName) and len(command.commandArgs) == 0):
            return True, self.helpCommands[command.commandName]
        else:
            #TODO - This is bad programming
            return False, self.helpCommands['default']
