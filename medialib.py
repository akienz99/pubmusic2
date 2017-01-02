import os
import random

class mediaLib:
   """
   This Class manages all available media files and displays them in a
   simple database
   """
   songList = []
   libPath = "."
   # File types that should be allowed to be in the library
   allowedFileTypes = ["mp3", "aac", "flac", "m4a", "ogg", "wav", "wma"]
   
   def __init__(self, filePath = os.getcwd() + "/media/"):
      self.libPath = filePath
      self.scanDir(self.libPath)
           
   def scanDir(self, directory = "."):
      for root, dirs, files in os.walk(directory, topdown=False):
         for name in files:
            for fileType in self.allowedFileTypes:
               if name.split(".")[-1] == fileType:
                  self.songList.append(os.path.join(root, name))
   
   def rescanLibrary(self):
      self.scanDir(self.libPath)
 
   def getSongList(self):
      return self.songList
      
   def getRandomSong(self):
      return random.choice(self.songList)
      
   def getAllowedFileTypes(self):
      return self.allowedFileTypes