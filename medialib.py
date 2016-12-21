import os
import random

class mediaLib:
   """
   This Class manages all available media files and displays them in a
   simple database
   """
   songList = []
   
   def __init__(self, libPath = os.getcwd() + "/media/"):
      self.scanDir(libPath)
      
      
   def scanDir(self, directory = "."):
      for root, dirs, files in os.walk(directory, topdown=False):
       for name in files:
           self.songList.append(os.path.join(root, name))
           print(os.path.join(root, name))
       #for name in dirs:
      #   print(os.path.join(root, name))
      
   def getSongList(self):
      return self.songList
      
   def getRandomSong(self):
      return random.choice(self.songList)