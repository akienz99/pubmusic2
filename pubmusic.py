#!/usr/bin/python
import os
import sys
import time
from threading import Thread
from vlcclient import VLCClient
from medialib import mediaLib
from ezlogger import ezLogger
from cliinterface import cliInterface

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

# Initializing our logger for use in playerCtl
logger = ezLogger()

logger.dispLogEntry("info", "initializing, please wait...")

# TODO: Make the following line multiplatform
os.system("nohup /usr/bin/vlc --intf telnet  --telnet-password admin &>/dev/null &")
#os.spawnl(os.P_NOWAIT, '/usr/bin/vlc --intf telnet  --telnet-password admin')
time.sleep(1) # Waiting for vlc to launch
# TODO: Check when launched and then continue

logger.dispLogEntry("welcome", "Welcome to Pubmusic2, version " + project_version)
   
class playerCtl:
   """
   VLC Media Player controller. This class contains the logic to interact
   with vlcclient and manage current playlist and status.
   """

   # TODO: Playlist syncronisation with VLC <- partally, pause/play remaining
   # TODO: MP3 tag access
   
   vlc = VLCClient("::1")
   
   currentPlaying = ""
   currentPlayingFromVlc = ""
   currentVlcPlaylistId = 4 - 1 # The Vlc playlist index starts with 4
   vlcIsPlaying = ""
   nextPlaying = []
   # FIXME: Proper Thread termination   
   threadStopper = False

   def __init__(self):
      self.vlc.connect() #Esthablishing a connection via VLCClient class
      logger.dispLogEntry("info", "connected to vlc media player")
      self.startMonitoringThread()
            
   def _monitoringThread(self):      
      # Sind Threds von Methoden einer Klasseninstanz in Python moeglich. Wenn nicht,
      # dann implementierung Ausserhalb der Klasse mit try-Bloeken um Exceptions
      # durch nicht verfuegbare Methoden zu vermeiden
      
      # Vergleiche get_title mit initialem Titelwert (Intervall 1-2 Sektunden)
      # Wenn geaendert dann springe weiter in der Playlist und poppe nextPlaying[0]
      # in currentPlaying. Ausserdem sollte die Aenderung geloggt werden
      # Wenn Ausgabe leer dann gestoppt (oder pausert???), wenn nur gestoppt dann
      # leere currentPlaying und setzte (neue) Statusvariable auf "paused"
      # Bei Aenderung den initialwert auf den des neuen Titels setzen (neue Ausgabe)
      # Startwert wird durch add gesetzt oder wenn status ist "playing" dann ein-
      # fach auf ersten empfangenen Wert setzen
      
      time.sleep(0.5)
      #self.currentPlaying = self.nextPlaying.pop(0) #FIXME
      self.currentPlayingFromVlc = self.getVlcInternalCurrentTitle() 
      while self.threadStopper == False: # FIXME: Proper Thread termination
         try: # Fixing inconsistency in Vlc playback status
            if self.currentPlayingFromVlc != self.getVlcInternalCurrentTitle() and int(self.getVlcIsCurrentlyPlaying()) == 1 :
               # Playing title has changed
               if self.nextPlaying: # If Playlist is not empty
                  self.currentPlaying = self.nextPlaying.pop(0)
                  self.vlc.raw("delete " + str(self.currentVlcPlaylistId))
                  self.currentVlcPlaylistId = self.currentVlcPlaylistId + 1
               self.currentPlayingFromVlc = self.getVlcInternalCurrentTitle()
               logger.dispLogEntry("playlist", "Now playing: " + self.getCleanTitle(self.currentPlaying))
            if int(self.getVlcIsCurrentlyPlaying()) == 0 and not self.nextPlaying:
               # Playback is stopped and playlist is empty
               self.currentPlaying = ""
               self.vlc.raw("delete " + str(self.currentVlcPlaylistId))
         except ValueError:
            pass
            
         self.vlcIsPlaying = self.getVlcIsCurrentlyPlaying()
         
         time.sleep(1)
      
   def startMonitoringThread(self):
      Thread(target=self._monitoringThread).start()
      
   def stopMonitoringThread(self):
      # FIXME: Proper Thread termination  
      self.threadStopper = True
      
   def add(self, filepath):
      """
      Adds and plays the given file to the playlist
      """
      self.vlc.add(filepath)     
      self.currentPlaying = filepath
      self.nextPlaying.insert(0, self.currentPlaying)
      self.vlcIsPlaying = self.getVlcIsCurrentlyPlaying()
      #logger.dispLogEntry("playlist", "Now playing: " + self.getCleanTitle(filepath))
      
   def enqueue(self, filepath):
      """
      Adds the given file to the end of the playlist
      """
      self.vlc.enqueue(filepath)
      self.nextPlaying.append(filepath)
      logger.dispLogEntry("playlist", "Added to queue: " + self.getCleanTitle(filepath))
      
   def next(self):
      """
      Plays thje next title in the playlist
      """
      self.vlc.next()
      
   def volume(self, vol):
      """
      Sets the volume to the given input
      """
      self.vlc.volume(vol)
      logger.dispLogEntry("info","setting volume to " + str(vol))
      
   def volup(self):
      """
      Increases the volume by 10 percent
      """
      self.vlc.volup()
      logger.dispLogEntry("info","raising volume")
      
   def voldown(self):
      """
      Lowers the volume by 10 percent
      """
      self.vlc.voldown()
      logger.dispLogEntry("info","lowering volume")
      
   def stop(self):
      """
      Stops the playback
      """
      self.vlc.stop()
      
   def clear(self):
      """
      Clears the playlist
      """
      self.vlc.clear()
      self.nextPlaying = []
      self.currentPlaying = None
      logger.dispLogEntry("warning","cleared playlist")
      
   def shutdown(self):
      """
      Terminates VLC and the title monitoring Thread
      """
      self.vlc.raw("shutdown")
      self.stopMonitoringThread()
      logger.dispLogEntry("info","Shutting down vlc client")
      
   def raw(self,command):
      """
      Executes a raw telnet command
      """
      self.vlc.raw(command)
      
   def getVlcInternalCurrentTitle(self):
      """
      Returns the internal name of the current playing title
      """
      return self.vlc.raw("get_title")
      
   def getVlcIsCurrentlyPlaying(self):
      """
      Returns 1 when playing, 0 when not
      """
      return self.vlc.raw("is_playing")
   
   def getCurrentPlaying(self):
      """
      Returns the current title in a formatted form
      """
      return self.getCleanTitle(self.currentPlaying)
      
   def getPlaylist(self):
      """
      Returns the current playlist
      """
      returnlist = self.nextPlaying
      returnlist.insert(0,self.currentPlaying)
      return returnlist
      
   def getCleanTitle(self, filepath):
      """
      Returns the clean title of a given filepath
      """
      # TODO: Add Mp3-Tag reader instead of using file names
      if filepath != "":
         return filepath.split("/")[-1].split(".")[-2].strip()
      else:
         return ""
   
# initializing our media library
library = mediaLib()
# initializing our media player controller
player = playerCtl()
# starting the mnain cli interface
cli = cliInterface(logger, player, library)
time.sleep(1)
player.add(library.getRandomSong()) # automatic first song