""" cli interface """
import sys
from threading import Thread


class CliInterface:
    """
    Command line interface for Pubmusic2
    """

    def __init__(self, logger, player, library):

        self.clithread = None
        # Variables for used objects from pubmusic.py
        # See this file for init
        self.logger = None
        self.player = None
        self.library = None

        # Setting the class variables to our objects
        self.logger = logger
        self.player = player
        self.library = library

        self.clithread = Thread(target=self.cli_thread_class).start()

    def cli_thread_class(self):
        """
        Thread that runs in an endless-loop for recieving and processing
        user input.
        """
        global input
        self.logger.disp_log_entry("info", "preparing cli environment")
        print("Interactive command line for pubmusic2")
        print("Enter \"help\" for a list of available commands")
        try:
            input = raw_input
        except NameError:
            pass

        while True:
            user_input = input("-> ").strip()
            user_command = user_input.split(" ")[0].lower()

            # General commands
            if user_command == "help":
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

            elif user_command == "exit":
                self.player.shutdown()
                sys.exit()

            # playback control
            elif user_command == "play":
                self.player.raw("play")

            elif user_command == "add":
                try:
                    self.player.enqueue(self.library.getSongList()[
                        int(user_input.split(" ")[1])])
                except IndexError:
                    self.logger.dispLogEntry(
                        "warning", "Title with given id not found")

            elif user_command == "random":
                self.player.enqueue(self.library.get_random_song())

            elif user_command == "autofill":
                for x in range(0, 10):
                    self.player.enqueue(self.library.get_random_song())

            elif user_command == "next":
                self.player.next()

            elif user_command == "skip":
                try:
                    self.player.skip(int(user_input.split(" ")[1]))
                except IndexError:
                    print("Please enter the amount of titles to skip")

            elif user_command == "volume":
                if len(user_input.split(" ")) >= 2:
                    if user_input.split(" ")[1] == "up":
                        self.player.volup()

                    elif user_input.split(" ")[1] == "down":
                        self.player.voldown()

                    else:
                        try:
                            if isinstance(int(user_input.split(" ")[1]), int):
                                # parameter is a integer
                                self.player.volume(user_input.split(" ")[1])
                        except ValueError:
                            print(
                                """given argument has to be \"up\", \"down\" or
                                a number""")

                else:
                    print("Current volume: " + str(self.player.getVolume()))

            # Informative commands
            elif user_command == "current":
                print(self.player.getCurrentPlaying())

            elif user_command == "playlist":
                for i, song in enumerate(self.player.getPlaylist()):
                    print(str(i) + " - " + self.player.getCleanTitle(song))

            elif user_command == "library":
                for i, song in enumerate(self.library.getSongList()):
                    print(str(i).zfill(4) + " - " +
                          self.player.getCleanTitle(song))

            # No input given
            else:
                if user_command == "":
                    print("No input was given. Please try again!")
                else:
                    print("Command \"" + user_command + "\" not found!")
