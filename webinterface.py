import cherrypy
<<<<<<< HEAD
from threading import Thread

class webInterface:
   
   webThread = None
   
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
      
      self.webThread = Thread(target=self.webInterfaceThread).start()

      
   def webInterfaceThread(self):
      cherrypy.config.update({'log.screen': False})
      cherrypy.quickstart(webApplication(self.logger, self.player, self.library), '/')
      
   def getPlayerObject(self):
      return self.player

class webApplication(object):
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
   
   @cherrypy.expose
   def index(self):
      return self.player.getCurrentPlaying()
        
=======

class webInterface:
   
   def __init__(self):
      cherrypy.quickstart(webContent())

class webContent(object):
   def index(self):
      return "Hello World!"
   
>>>>>>> added webinterface.py
