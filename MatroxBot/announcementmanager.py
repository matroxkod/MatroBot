import filemanager as fileManager
import utility as utilityClass

# Data structure of an annnoncement
class Announcement:

    def __init__(self, announcementid, message = "There is no message"):
        self.announcementid = announcementid
        self.message = message

# Class responsible for announcement thread, loading announcements
# saving announcements
class AnnouncementManager:
    fm = fileManager.FileManager()
    util = utilityClass.Utility()

    announcements = {}
    maxAnnouncementId = 0

    def loadAnnouncements(self):
        loadedFile, fileContents = self.fm.loadAnnouncementFile()
        if(loadedFile):
            # Parse file into individual announcements
            for line in fileContents:
                announce = line.split( )
                if (announce.count > 1):
                    loadedId = self.util.try_parse_int(announce[0])
                    newAnnouncement = Announcement(loadedId, ' '.join(announce[1:]))
                    self.announcements[loadedId] = newAnnouncement
                else:
                    pass
        else:
            print "Error loading announcements"

