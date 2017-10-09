import filemanager as fileManager
import utility as utilityClass

from threading import Thread
import time
from singleton import Singleton

# Data structure of an annnoncement
class Announcement:

    def __init__(self, announcementid, message = "There is no message"):
        self.announcementid = announcementid
        self.message = message

    def toString(self):
        return str(self.announcementid) + " " + "".join(self.message)

    def messageToString(self):
        try:
            return "".join(self.message)
        except:
            return self.message

# Class responsible for announcement thread, loading announcements
# saving announcements
@Singleton
class AnnouncementManager:
    def __init__(self):
        self.announcements = {}
        self.maxAnnouncementId = 0
        self.loadedFile = False
    
    def startAnnouncementThread(self):
        announcementThread = Thread(target = self.runThread)
        announcementThread.setDaemon(True)
        announcementThread.start()

    def runThread(self):
        attemptsToLoad = 0
        currentAnnounceId = 1
        while True:
            if(self.loadedFile):
                # Check if we actually loaded announcements
                if(len(self.announcements) > 0):
                    #TODO send to chat
                    try:
                        print(self.announcements[currentAnnounceId].messageToString())  
                    except Exception as detail:
                        print "Unexpected exception in announcement thread: ", detail
                        pass
                    currentAnnounceId = currentAnnounceId + 1                                     
                    if(currentAnnounceId > self.maxAnnouncementId):
                        # Start over
                        currentAnnounceId = 1
            else:
                if(attemptsToLoad < 2):
                    # Try to load the file once
                    attemptsToLoad = attemptsToLoad + 1
                    self.loadAnnouncements()
                else:
                    print "Failed to load announcements file after 1 attempt."
                    return
            time.sleep(2)
    
    def loadAnnouncements(self):
        self.loadedFile, fileContents = fileManager.FileManager.Instance().loadAnnouncementFile()
        if(self.loadedFile):
            # Parse file into individual announcements
            for line in fileContents:
                announce = line.split( )
                if (len(announce) > 1):
                    parsed, loadedId = utilityClass.Utility().try_parse_int(announce[0])
                    if (parsed):
                        if (loadedId > self.maxAnnouncementId):
                             self.maxAnnouncementId = loadedId
                        newAnnouncement = Announcement(loadedId, ' '.join(announce[1:]))
                        self.announcements[loadedId] = newAnnouncement
                    else:
                        print "Error parsing announcement id ", announce[0]
                else:
                    print "Invalid announcement format ", announce
        else:
            print "Error loading announcements"

    def addAnnouncementMessage(self, message):
        if(self.loadedFile == False):
            self.loadAnnouncements()
        self.maxAnnouncementId += 1
        newAnnouncement = Announcement(self.maxAnnouncementId, message)
        if(fileManager.FileManager.Instance().addAnnouncement(newAnnouncement)):
            self.announcements[self.maxAnnouncementId] = newAnnouncement
            return "Added announcement " + newAnnouncement.messageToString()
        return "Failed to add announcement " + message + ". Check error logs."

    def reloadAnnouncements(self):
        self.loadAnnouncements()
        if(self.loadedFile):
            return "Reloaded announcements file."
        else:
            return "Could not reload announcements file. Check error log."
      