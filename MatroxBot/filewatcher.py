# Classes used for monitoring files

from threading import Thread
import time
import os.path
from singleton import Singleton
from filemanager import FileManager
from matroxcommand import MatroxCommandManager

class WatchedFile:

    def __init__(self, commandToRun, filePath = "", lastModTime = 0):
        self.filePath = filePath
        self.commandToRun = commandToRun
        self.lastModTime = lastModTime

    def defaultFunction(self):
        print("Ran default function. Nothing has been specified.")

@Singleton
class FileWatcher:
    def __init__(self):
        self.filesToWatch = [
            WatchedFile(MatroxCommandManager.reloadAnnouncements, FileManager.Instance().formatPath(FileManager.Instance().ROOT_FILEPATH, FileManager.Instance().ANNOUNCEMENTS_FILENAME))                            
        ]

    def startFileWatcherThread(self):
        fileWatcherThread = Thread(target = self.runThread)
        fileWatcherThread.setDaemon(True)
        fileWatcherThread.start()

    def runThread(self):
        while True:
            for watched in self.filesToWatch:
                # Check the last mod (UNIX timestamp) on file
                lastMod = os.path.getmtime(watched.filePath)
                if lastMod > watched.lastModTime:
                    print('Updating time and running command')
                    # File has been modded since we last saw it
                    watched.lastModTime = lastMod
                    watched.commandToRun("")
            time.sleep(10)