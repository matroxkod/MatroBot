#Utility class for performing actions associated with basic txt files
import os.path

class FileManager:

    ROOT_FILEPATH = "configs"
    ANNOUNCEMENTS_FILENAME = "announcements.txt"

    # Returns an array of known announcements
    def loadAnnouncementFile(self):
        return self.openFile(self.formatPath(self.ROOT_FILEPATH, self.ANNOUNCEMENTS_FILENAME))

    # Opens a generic file for reading
    @staticmethod
    def openFile(filePath):
        try:
            openedFile = open(filePath, 'r')
        except:
            print "Could not find file: " + filePath
            return False, ""
        else:
            return True, openedFile

    # Formats the path name
    @staticmethod
    def formatPath(filePath, fileName):
        path = filePath + '\\' + fileName
        return os.path.relpath(path)