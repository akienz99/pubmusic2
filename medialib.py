""" media library """
import os
import random


class MediaLib:
    """
    This Class manages all available media files and displays them in a
    simple database
    """

    def __init__(self, filepath=os.getcwd() + "/media/"):

        self.song_list = []
        self.libpath = "."
        # File types that should be allowed to be in the library
        self.allowed_file_types = ["mp3", "aac",
                                   "flac", "m4a", "ogg", "wav", "wma"]

        self.libpath = filepath
        self.scan_dir(self.libpath)

    def scan_dir(self, directory="."):
        """
        Scans a given directory
        """
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                for filetype in self.allowed_file_types:
                    if name.split(".")[-1] == filetype:
                        self.song_list.append(os.path.join(root, name))

    def rescan_library(self):
        """
        Rescans the directory given as initial file path
        """
        self.scan_dir(self.libpath)

    def get_song_list(self):
        """
        Returns a list of all songs
        """
        return self.song_list

    def get_random_song(self):
        """
        Returns a random song form the library
        """
        return random.choice(self.song_list)

    def get_allowed_file_types(self):
        """
        Returns a list of all allowed file types
        """
        return self.allowed_file_types
