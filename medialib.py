import os
import random

class mediaLib:
   """
   This Class manages all available media files and displays them in a
   simple database
   """
   songList = []
   libPath = "."
   
   def __init__(self, filePath = os.getcwd() + "/media/"):
      self.libPath = filePath
      self.scanDir(self.libPath)
           
   def scanDir(self, directory = "."):
      for root, dirs, files in os.walk(directory, topdown=False):
       for name in files:
           self.songList.append(os.path.join(root, name))
   
   def rescanLibrary(self):
      self.scanDir(self.libPath)
 
   def getSongList(self):
      return self.songList
      
   def getRandomSong(self):
      return random.choice(self.songList)