from threading import Thread

class webSocket:
   # Variables for used objects from pubmusic.py
   # See this file for init
   logger = None
   player = None
   library = None
   
   def __init__(self, logger, player, library):
      # Setting the class variables to our objects
      self.logger = logger
      self.player = player
      self.library = library