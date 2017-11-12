# announcementmanager.py
from filemanager import FileManager
from utility import Utility
from threading import Thread
import time
from singleton import Singleton
from chatmanager import ChatManager
from csvprocessor import CSVFileProcessor

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

# Class responsible for announcement thread and loading announcements
# saving announcements
@Singleton
class AnnouncementManager:
    def __init__(self):
        self.announcements = {}
        self.maxAnnouncementId = 0
        self.loadedFile = False
        self.announcementInterval = 300
        self.currentAnnounceId = 1
    
    # Starts running the announcments thread
    def startAnnouncementThread(self):
        announcementThread = Thread(target = self.runThread)
        announcementThread.setDaemon(True)
        announcementThread.start()

    # Announcements thread that will cycle through memory every x seconds and display to chat
    def runThread(self):
        attemptsToLoad = 0
        currentAnnounceId = 1
        while True:
            if(self.loadedFile):
                # Check if we actually loaded announcements
                if(len(self.announcements) > 0):
                    try:
                        ChatManager.Instance().sendMessageToChat(self.announcements[self.currentAnnounceId].messageToString())  
                    except Exception as detail:
                        print "Unexpected exception in announcement thread: ", detail
                        pass
                    self.currentAnnounceId = self.currentAnnounceId + 1                                     
                    if(self.currentAnnounceId > self.maxAnnouncementId):
                        # Start over
                        self.currentAnnounceId = 1
            else:
                if(attemptsToLoad < 2):
                    # Try to load the file once
                    attemptsToLoad = attemptsToLoad + 1
                    self.loadAnnouncements()
                else:
                    print "Failed to load announcements file after 1 attempt."
                    return
            interval = 300
            # Check if this is an actual integer befor attempting to parse
            if not isinstance(self.announcementInterval, (int, long)):            
                parsed, interval = Utility.try_parse_int(self.announcementInterval)
                if not parsed:
                    print "Failed to parse correct interval. Defaulting to 25 seconds."
            else:
                interval = self.announcementInterval
            _originalInterval = interval
            for i in range (0, interval):
                time.sleep(1)
                interval = _originalInterval
                if not isinstance(self.announcementInterval, (int, long)):            
                    parsed, interval = Utility.try_parse_int(self.announcementInterval)
                else:
                    interval = self.announcementInterval
                # Check to see if the interval changed. If it did, break out of the loop
                if _originalInterval != interval:
                    break
    
    # Loads announcements from file into memory
    def loadAnnouncements(self):
#        self.loadedFile, fileContents = FileManager.Instance().loadAnnouncementFile()
        self.loadedFile, fileContents = CSVFileProcessor.Instance().readAnnouncements()         
        if(self.loadedFile):
            # Clear out announcements
            self.announcements.clear()
            i = 0
            for announce in fileContents:
                try:
                    id = fileContents[i].key
                    message = fileContents[i].value
                    self.announcements[id] = Announcement(id, key)
                    if (id > self.maxAnnouncementId):
                        self.maxAnnouncementId = id
                    i = i + 1
                except:
                    pass
            # Parse file into individual announcements
#            for line in fileContents:
#                announce = line.split( )
#                if (len(announce) > 1):
#                    parsed, loadedId = Utility().try_parse_int(announce[0])
#                    if (parsed):
#                        if (loadedId > self.maxAnnouncementId):
#                             self.maxAnnouncementId = loadedId
#                        newAnnouncement = Announcement(loadedId, ' '.join(announce[1:]))
#                        self.announcements[loadedId] = newAnnouncement
#                    else:
#                        print "Error parsing announcement id ", announce[0]
#                else:
#                    print "Invalid announcement format ", announce
        else:
            print "Error loading announcements"
    
    # Adds an announcement to the announcements file and to memory
    def addAnnouncementMessage(self, message):
        if(self.loadedFile == False):
            self.loadAnnouncements()
        self.maxAnnouncementId += 1
        newAnnouncement = Announcement(self.maxAnnouncementId, message)
        if(FileManager.Instance().addAnnouncement(newAnnouncement)):
            self.announcements[self.maxAnnouncementId] = newAnnouncement
            return "Added announcement " + newAnnouncement.messageToString()
        return "Failed to add announcement " + message + ". Check error logs."

    # Forces a reload of the announcements file into memory
    def reloadAnnouncements(self):
        self.loadAnnouncements()
        if(self.loadedFile):
            return "Reloaded announcements file."
        else:
            return "Could not reload announcements file. Check error log."

    # Help
    @staticmethod  
    def addAnnouncementHelp():
        return "Adds an announcement to the list. Specify the text of what to add. !addannouncement Hello Funny People!"

    @staticmethod
    def setAnnouncementIntervalHelp():
        return "Updates the interval for announcements in seconds. !setannouncementinterval 5"
