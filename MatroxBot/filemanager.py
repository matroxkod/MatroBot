# filemanager.py
# Utility class for performing actions associated with basic txt files
import os.path
import copy
import sys
from singleton import Singleton

@Singleton
class FileManager:
    def __init__(self):
        self.ROOT_FILEPATH = "configs"
        self.ANNOUNCEMENTS_FILENAME = "announcements.txt"
        self.announcementFile = ""

    # Returns an array of known announcements
    def loadAnnouncementFile(self):
        # Try to load the file into memory for reading
        loadedFile =  self.openAnnouncementsFile("read")
        fileBuffer = []
        if(loadedFile):
            # Load each line into memory
            for line in self.announcementFile:
                if(len(line) > 3):
                    fileBuffer.append(line)
        # Close the file for later use
        self.closeAnnouncementsFile()
        # Return loaded flag and the buffer
        return loadedFile, fileBuffer

    # Adds an announcement to the file
    def addAnnouncement(self, announcementToAdd):
        try:
            if(self.announcementFile.closed):
                # Open the announcement file for appending
                self.openAnnouncementsFile("append")
            # Add the announcement with EOL appended
            self.announcementFile.write(announcementToAdd.toString()+"\n")
            # Close the file for later use
            self.closeAnnouncementsFile()
        except Exception as detail:
            print "Unexpected exception: ", detail
            print "Could not write announcement to file " + announcementToAdd.toString()
            return False
        else:
            return True

    # Opens the announcement file in the specified mode
    def openAnnouncementsFile(self, openMode):
        openedFileResult = False
        if(openMode == "write" or openMode == "read"):
            openedFileResult, self.announcementFile = self.openFile(self.formatPath(self.ROOT_FILEPATH, self.ANNOUNCEMENTS_FILENAME))
        elif openMode == "append":
            openedFileResult, self.announcementFile = self.openFileForAppend(self.formatPath(self.ROOT_FILEPATH, self.ANNOUNCEMENTS_FILENAME))
        return openedFileResult

    # Closes an announcement file
    def closeAnnouncementsFile(self):
        return self.closeFile(self.announcementFile)
    
    # Opens a generic file for reading
    @staticmethod
    def openFile(filePath):
        try:
            openedFile = open(filePath, 'r+')
        except:
            print "Could not find file: " + filePath
            return False, ""
        else:
            return True, openedFile
    
    # Opens a generic file for appending
    @staticmethod
    def openFileForAppend(filePath):
        try:
            openedFile = open(filePath, 'a+')
        except:
            print "Could not find file: " + filePath
            return False, ""
        else:
            return True, openedFile

    # Closes a generic file
    @staticmethod
    def closeFile(fileToClose):
        try:
            fileToClose.close()
        except Exception as details:
            print "Could not close the file properly: ", details

    # Formats the path name
    @staticmethod
    def formatPath(filePath, fileName):
        path = filePath + '\\' + fileName
        return os.path.relpath(path)
    
