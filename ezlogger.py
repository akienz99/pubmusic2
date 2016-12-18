from __future__ import print_function
import time

class ezLogger:
   
   isCurrentlyRunning = False
   
   def __init__(self, verbose_level):
      # TODO: Add verbosity control
      verbose = verbose_level
      
      # TODO: Add last message
      lastMessage = None;
      
   def dispLogEntry(self, msg_type, msg_value):
      
      while self.isCurrentlyRunning == True:
         time.sleep(0.05)
      
      self.isCurrentlyRunning = True
      if msg_type == "error":
         print ("\033[1;31m[error] ", end="")
         
      elif  msg_type == "warning":
         print ("\033[1;33m[warning] ", end="")
         
      elif  msg_type == "playlist":
         print ("\033[1;32m[playlist] ", end="")
         
      elif  msg_type == "info":
         print ("\033[1;34m[info] ", end="")
         
      else:
         print ("\033[1;34m["+ msg_type +"] ", end="")
         
      print (msg_value + "\033[0m")
      self.isCurrentlyRunning = False
      
   def getLastMessage(self):
      return lastMessage
