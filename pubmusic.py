import os
import sys
import time
from vlcclient import VLCClient

print ("#######################################################")
print ("#  _____       _                         _      ___   #")
print ("# |  __ \     | |                       (_)    |__ \  #")
print ("# | |__) |   _| |__  _ __ ___  _   _ ___ _  ___   ) | #")
print ("# |  ___/ | | | '_ \| '_ ` _ \| | | / __| |/ __| / /  #")
print ("# | |   | |_| | |_) | | | | | | |_| \__ \ | (__ / /_  #")
print ("# |_|    \__,_|_.__/|_| |_| |_|\__,_|___/_|\___|____| #")
print ("#                                                     #")
print ("#######################################################")

project_version = "0.0.1-alpha1"

os.system("nohup /usr/bin/vlc --intf telnet  --telnet-password admin &>/dev/null &")
#os.spawnl(os.P_NOWAIT, '/usr/bin/vlc --intf telnet  --telnet-password admin')
time.sleep(1)
  
class playerCtl:

   # TODO: Playlist syncronisation with VLC
   # TODO: Notifications on new song event
   # TODO: Checks for empty playlist
   # TODO: Music database
   # TODO: MP3 tag access
   # TODO: onTitleChange Thread
   
   vlc = VLCClient("::1")
   
   currentPlaying = None
   nextPlaying = []

   def __init__(self):
      self.vlc.connect()
            
     
   def add(self, filepath):
      self.vlc.add(filepath)     
      self.currentPlaying = filepath
       
   def enqueue(self, filepath):
      self.vlc.enqueue(filepath)
      self.nextPlaying.append(filepath)
      
   def next(self):
      self.vlc.next()
      
   def volume(self, vol):
      self.vlc.volume(vol)
       
   def volup(self):
      self.vlc.volup()
      
   def voldown(self):
      self.vlc.voldown()
       
   def stop(self):
      self.vlc.stop()
      
   def clear(self):
      self.vlc.clear()
      self.nextPlaying = []
      self.currentPlaying = None
       
   def shutdown(self):
      self.vlc.raw("shutdown")
      self.stopTitleChangeNotifierThread()
      
   def getVlcInternalCurrentTitle(self):
      return self.vlc.raw("get_title")
   
   def getCurrentPlaying(self):
      return self.getCleanTitle(self.currentPlaying)
      
   def getCleanTitle(self, filepath):
      return filepath.split("/")[-1].split(".")[-2].strip()
   
# Initilalizing our media player controller
player = playerCtl()