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

class config:
   """
   Main configuration, might be moved to a seperate file later
   
   --- Edit this section to your needs! ---
   """
   # Sets the amount of logging messages, lower number means less output
   logger_verbosity = 3
   # If True, VLC media player wil be started automatically
   autostart_vlc = True
   # If True, a random song will be automatically queued and played
   autostart_playback = True
   # The volume with which the player starts playback
   startVolume = 70
   # Location of the used audio files, relative paths are supported
   media_dir = "./media/"
   
   """
   --- Configuration section ends here! ---
   """
   
project_version = "0.0.1-alpha1"

# Initializing our logger for use in playerCtl
logger = ezLogger( config.logger_verbosity )

logger.dispLogEntry("info", "initializing, please wait...")

sys.stdout.write('\33]0;Pubmusic2\a')
if config.autostart_vlc:
   user_os = sys.platform.lower()
   if user_os == "linux" or user_os == "linux2": 
      os.system("nohup vlc --intf telnet  --telnet-password admin &>/dev/null &")
      time.sleep(1) # Waiting for vlc to launch
      
   elif user_os == "win32" or user_os == "cygwin":
      # TODO: This section needs testing
      # This took literally two hours for me to figure out 
      os.spawnl(os.P_NOWAIT,'C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe','vlc.exe --intf telnet --telnet-password admin')
      time.sleep(1)
        
   else:
      logger.warning("You are running a currently unsupported system. Autostart is disabled")
      try: 
         input = raw_input
      except NameError:
         pass
         
      input("Start VLC manually and press Enter to continue")

logger.dispLogEntry("welcome", "Welcome to Pubmusic2, version " + project_version)
   
class playerCtl:
   """
   VLC Media Player controller. This class contains the logic to interact
   with vlcclient and manage current playlist and status.
   """

   # TODO: play/pause syncronisation with VLC
   # TODO: MP3 tag access

   def __init__(self, startVol = 70):
      
      self.vlc = VLCClient("::1")
      # VLC connection for monitoring thread to avoid multiple telnet send commands
      # at the same time, i.e. when user is changing songs while check is in 
      # progress. This scenario would cause a telnet timeout and crash
      self.vlcMonitoring = VLCClient("::1")
      
      self.currentPlaying = ""
      self.currentPlayingFromVlc = ""
      self.currentVlcPlaylistId = 4 - 1 # The Vlc playlist index starts with 4
      self.vlcIsPlaying = ""
      self.nextPlaying = []
      self.threadStopper = False
 
      try:
         self.vlc.connect() #Esthablishing a connection via VLCClient class
      except ConnectionRefusedError:
         logger.error("Connection to vlc could not be established!")
      self.vlcMonitoring.connect() # Seperate connection for monitoring thread
      logger.dispLogEntry("info", "connected to vlc media player")
      self.volume( startVol ) # Setting start value from config
      self.startMonitoringThread()
            
   def _monitoringThread(self):      
      
      time.sleep(0.5)
      self.currentPlayingFromVlc = self.getVlcInternalCurrentTitle() 
      while self.threadStopper == False:
         try: # Fixing inconsistency in Vlc playback status
            if self.currentPlayingFromVlc != self.getVlcInternalCurrentTitle() and int(self.getVlcIsCurrentlyPlaying()) == 1 :
               # Playing title has changed
               if self.nextPlaying: # If Playlist is not empty
                  self.currentPlaying = self.nextPlaying.pop(0)
                  self.deleteFromVlcPlaylist(self.currentVlcPlaylistId)
                  self.currentVlcPlaylistId = self.currentVlcPlaylistId + 1
                  
               self.currentPlayingFromVlc = self.getVlcInternalCurrentTitle()
               logger.dispLogEntry("playlist", "Now playing: " + self.getCleanTitle(self.currentPlaying))
               
            if int(self.getVlcIsCurrentlyPlaying()) == 0 and not self.nextPlaying:
               # Playback is stopped and playlist is empty
               self.currentPlaying = ""
               self.deleteFromVlcPlaylist(self.currentVlcPlaylistId)
               
         except ValueError:
            # TODO: This might be fixed with second vlc connection thread
            logger.warn("Inconsistency in VLC output detected")
            logger.warn("Playlist might be asynchronous!")
            
         self.vlcIsPlaying = self.getVlcIsCurrentlyPlaying()
         
         time.sleep(0.1)
      
   def startMonitoringThread(self):
      Thread(target=self._monitoringThread).start()
      
   def stopMonitoringThread(self):
      self.threadStopper = True
      
   def add(self, filepath):
      """
      Adds and plays the given file to the playlist
      """
      self.vlc.add(filepath)     
      self.currentPlaying = filepath
      self.nextPlaying.insert(0, self.currentPlaying)
      self.vlcIsPlaying = self.getVlcIsCurrentlyPlaying()
      
   def enqueue(self, filepath):
      """
      Adds the given file to the end of the playlist
      """
      self.vlc.enqueue(filepath)
      self.nextPlaying.append(filepath)
      logger.dispLogEntry("playlist", "Added to queue: " + self.getCleanTitle(filepath))
      
   def next(self):
      """
      Plays the next title in the playlist
      """
      self.vlc.next()
      
   def skip(self, n):
      """
      Skips a given amount of titles
      """
      for i in range(0, n):
         self.next()
         time.sleep(0.5) # FIXME Direct access to playlist
      
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
   
   def getVolume(self):
      """
      Returns the current playback volume
      """
      currentVolume = float(self.vlc.volume().decode("utf-8").replace(",", "."))
      while currentVolume == 1.0: # Fix for inconsistent vlc output
         currentVolume = float(self.vlc.volume().decode("utf-8").replace(",", "."))
      return currentVolume
      
   def getVlcInternalCurrentTitle(self):
      """
      Returns the internal name of the current playing title
      """
      return self.vlcMonitoring.raw("get_title")
      
   def getVlcIsCurrentlyPlaying(self):
      """
      Returns 1 when playing, 0 when not
      """
      return self.vlcMonitoring.raw("is_playing")
      
   def deleteFromVlcPlaylist(self, pID):
      """
      Deletes the Song with the given id from VLC internal playlist
      """
      self.vlcMonitoring.raw("delete " + str(pID))
   
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
library = mediaLib( config.media_dir )
# initializing our media player controller
player = playerCtl( config.startVolume )
# starting the main cli interface
cli = cliInterface(logger, player, library)
time.sleep(1)
if config.autostart_playback:
   player.add(library.getRandomSong()) # automatic first song