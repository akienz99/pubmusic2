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
         userCommand = userInput.split(" ")[0].lower()
         
         # General commands
         if userCommand == "help":
            # TODO: Extend help
            print("Available commands:")
            print("")
            print("help     - displays this message")
            print("exit     - closes the application")
            print("")
            print("play     - starts the playback")
            print("add      - adds a song by id")
            print("random   - adds a random song")
            print("autofill - adds 10 random songs")
            print("next     - skips to the next song")
            print("skip     - skips a given amount of songs")
            print("volume   - controls the playback volume")
            print("")
            print("current  - displays the current playing song")
            print("library  - displays the song library")
            print("playlist - displays the current playlist")
            print("")
            
         elif userCommand == "exit":
            self.player.shutdown()
            sys.exit()
            
         # playback control        
         elif userCommand == "play":
            self.player.raw("play")
            
         elif userCommand == "add":
            try:
               self.player.enqueue(self.library.getSongList()[int(userInput.split(" ")[1])])
            except IndexError:
               self.logger.dispLogEntry("warning", "Title with given id not found")
 
         elif userCommand == "random":
            self.player.enqueue(self.library.getRandomSong())
             
         elif userCommand == "autofill":
            for x in range(0,10):
               self.player.enqueue(self.library.getRandomSong())
         
         elif userCommand == "next":
            self.player.next()
            
         elif userCommand == "skip":
            self.player.skip(int(userInput.split(" ")[1]))
     
         elif userCommand == "volume":
            if len(userInput.split(" ")) >= 2:
               if userInput.split(" ")[1] == "up":
                  self.player.volup()
                  
               elif userInput.split(" ")[1] == "down":
                  self.player.voldown()
                  
               else:
                  try:
                     if isinstance(int(userInput.split(" ")[1]), int):
                        # parameter is a integer
                        self.player.volume(userInput.split(" ")[1])
                  except ValueError:
                     print("given argument has to be \"up\", \"down\" or a number")
                  
            else:
               print("Not enough arguments given")
         
         # Informative commands
         elif userCommand == "current":
            print(self.player.getCurrentPlaying())
            
         elif userCommand == "playlist":
            for songs in self.player.getPlaylist():
               print (self.player.getCleanTitle(songs))
           
         elif userCommand == "library":
            for i, song in enumerate(self.library.getSongList()):
               print(str(i).zfill(4) + " - " + self.player.getCleanTitle(song))
         
         # No input given
         else:
            if userCommand == "":
               print("No input was given. Please try again!")
            else:
               print("Command \"" + userCommand + "\" not found!")