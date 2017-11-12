#csv.py
# This is the module used for reading and writing CVS entries

import csv
from filemanager import FileManager
from singleton import Singleton

@Singleton
class CSVFileProcessor:

    @staticmethod
    def readAnnouncements():
        announcements = {}
        with open(FileManager.Instance().formatPath(FileManager.Instance().ROOT_FILEPATH, FileManager.Instance().ANNOUNCEMENTS_FILENAME)) as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                announcements[row['Id']] = row['Message']
        return True, announcements