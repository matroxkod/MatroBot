import filemanager as fileManager
import utility as utilityClass

# Data structure of an annnoncement
class Announcement:

    def __init__(self, announcementid, message = "There is no message"):
        self.announcementid = announcementid
        self.message = message

    def toString(self):
        return self.announcementid + " " + self.message

# Class responsible for announcement thread, loading announcements
# saving announcements
class AnnouncementManager:
    fm = fileManager.FileManager()
    util = utilityClass.Utility()

    announcements = {}
    maxAnnouncementId = 0
    loadedFile = False

    def loadAnnouncements(self):
        self.loadedFile, fileContents = self.fm.loadAnnouncementFile()
        if(self.loadedFile):
            # Parse file into individual announcements
            for line in fileContents:
                announce = line.split( )
                if (announce.count > 1):
                    parsed, loadedId = self.util.try_parse_int(announce[0])
                    if (parsed):
                        if (loadedId > self.maxAnnouncementId):
                             maxAnnouncementId = loadedId
                        newAnnouncement = Announcement(loadedId, ' '.join(announce[1:]))
                        self.announcements[loadedId] = newAnnouncement
                    else:
                        print "Error parsing announcement id " + announce[0]
                else:
                    print "Invalid announcement format " + announce
        else:
            print "Error loading announcements"

    def addAnnouncementMessage(self, message):
        if(self.loadedFile == False):
            self.loadAnnouncements()
        self.maxAnnouncementId += 1
        newAnnouncement = Announcement(self.maxAnnouncementId, message)
        if(self.fm.addAnnouncement(newAnnouncement)):
            self.announcements[self.maxAnnouncementId] = newAnnouncement

        
