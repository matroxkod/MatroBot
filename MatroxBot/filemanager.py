#Utility class for performing actions associated with basic txt files
import os.path
import copy

class FileManager:

    ROOT_FILEPATH = "configs"
    ANNOUNCEMENTS_FILENAME = "announcements.txt"
    announcementFile = ""

    # Returns an array of known announcements
    def loadAnnouncementFile(self):
        self.announcementFile = self.openFile(self.formatPath(self.ROOT_FILEPATH, self.ANNOUNCEMENTS_FILENAME))
        return self.announcementFile

    # Adds an announcement to the file
    def addAnnouncement(self, announcementToAdd):
        try:
            self.announcementFile.write(announcementToAdd.toString())
        except:
            print "Could not write announcement to file " + announcementToAdd.toString()
            return False
        else:
            return True

    # Closes an announcement file
    def closeAnnouncementsFile(self):
        self.closeFile(self.announcementFile)
    
    # Opens a generic file for reading
    @staticmethod
    def openFile(filePath):
        try:
            openedFile = open(filePath, 'wr')
        except:
            print "Could not find file: " + filePath
            return False, ""
        else:
            return True, openedFile
    
    # Closes a generic file
    @staticmethod
    def closeFile(fileToClose):
        try:
            close(announcementFile)
        except:
            print "Could not close the file properly"

    # Formats the path name
    @staticmethod
    def formatPath(filePath, fileName):
        path = filePath + '\\' + fileName
        return os.path.relpath(path)