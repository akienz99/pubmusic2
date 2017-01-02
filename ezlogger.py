import time

class ezLogger:
   """
   Simple console logger
   
   Verbosity levels:
   
   0 -> Don't display any messages
   1 -> Only Errors will be displayed
   2 -> Errors and warnings will be displayed
   3 -> All messages will be displayed
   """
      
   def __init__(self, verbose_level=3):
      self.verbosity = verbose_level
      self.isCurrentlyRunning = False
      
      self.messageList = []
      
   def dispLogEntry(self, msg_type, msg_value):
      """
      Displays a log entry in the console
      """
      
      while self.isCurrentlyRunning == True:
         time.sleep(0.05)
         
      logMessage = ""
      
      self.isCurrentlyRunning = True
      if msg_type == "error" and self.verbosity >= 1:
         logMessage = "\033[1;31m[error] " + msg_value + "\033[0m"
         
      elif msg_type == "warning" and self.verbosity >= 2:
         logMessage = "\033[1;33m[warning] " + msg_value + "\033[0m"
         
      elif msg_type == "playlist" and self.verbosity >= 3:
         logMessage = "\033[1;32m[playlist] " + msg_value + "\033[0m"
         
      elif msg_type == "info" and self.verbosity >= 3:
         logMessage = "\033[1;34m[info] " + msg_value + "\033[0m"
         
      elif self.verbosity >= 3:
         logMessage = "\033[1;34m["+ msg_type +"] " + msg_value + "\033[0m"
         
      if logMessage != "":
         print (logMessage)
         self.messageList.append(logMessage)

      self.isCurrentlyRunning = False
      
   # Short calls for different log types -> future
      
   def error(self, message):
      """
      Displays an error message in the log
      """
      self.dispLogEntry("error", message)
      
   def warning(self, message):
      """
      Displays an warning message in the log
      """
      self.dispLogEntry("warning", message)
      
   def playlist(self, message):
      """
      Displays a playlist info in the log
      """
      self.dispLogEntry("playlist", message)
      
   def info(self, message):
      """
      Displays an info message in the log
      """
      self.dispLogEntry("info", message)
      
   # getters and setters
      
   def getLastMessage(self):
      """
      Gets the last displayed message
      """
      try:
         return self.messageList[-1]
      except IndexError:
         return ""
      
   def getMessageList(self):
      """
      Gets a list of all displayed messages
      """
      return self.messageList
      
   def getVerbosity(self):
      """
      Returns the current verbosity level
      """
      return self.verbosity
      
   def setVerbosity(self, newValue):
      """
      Sets the verbosity level
      """
      self.verbosity = newValue
