import sys
from threading import Thread

class cliInterface:
   
   cliThread = None
   
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
      
      self.cliThread = Thread(target=self.cliThreadClass).start()
   
   
   def cliThreadClass(self):
      global input
      self.logger.dispLogEntry("info","preparing cli environment")
      print("Interactive command line for pubmusic2")
      print("Enter \"help\" for a list of available commands")
      try: input = raw_input
      except NameError: pass

      while True:
         userInput = input("-> ").strip()
         userCommand = userInput.split(" ")[0]
         
         if userCommand == "help":
            # TODO: Extend help
            print("Available commands:")
            print("")
            print("help    - displays this message")
            print("exit    - closes the application")
            print("")
            print("play    - starts the playback")
            print("add     - adds a song by id")
            print("random  - adds a random song")
            print("next    - skips to the next song")
            print("")
            print("current - displays the current playing song")
            print("library - displays the song library")
            print("")
            print("volume  - controls the playback volume")
            
            
            
         elif userCommand == "volume":
            if len(userInput.split(" ")) >= 2:
               if userInput.split(" ")[1] == "up":
                  self.player.volup()
                  
               elif userInput.split(" ")[1] == "down":
                  self.player.voldown()
                  
               elif isinstance(int(userInput.split(" ")[1]), int):
                  # TODO: Check if given value is int
                  self.player.volume(userInput.split(" ")[1])
                  
            else:
               print("Not enough arguments given")
               
         elif userCommand == "next":
            self.player.next()
            
         elif userCommand == "play":
            self.player.raw("play")
            
         elif userCommand == "add":
            try:
               self.player.enqueue(self.library.getSongList()[int(userInput.split(" ")[1])])
            except IndexError:
               self.logger.dispLogEntry("warning", "Title with given id not found")
            
         elif userCommand == "current":
            print(self.player.getCurrentPlaying())
               
         elif userCommand == "exit":
            self.player.shutdown()
            sys.exit()
            
         elif userCommand == "random":
           #player.add(self.library.getRandomSong())
            self.player.enqueue(self.library.getRandomSong())
            
         elif userCommand == "library":
            i = 0
            for song in library.getSongList():
               print(str(i).zfill(4) + " - " + self.player.getCleanTitle(song))
               i = i + 1
            
         else:
            if userCommand == "":
               print("No input was given. Please try again!")
            else:
               print("Command \"" + userCommand + "\" not found!")