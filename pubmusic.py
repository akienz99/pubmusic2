#!/usr/bin/python
""" pubmusic2 """
import os
import sys
import time
from threading import Thread
from vlcclient import VLCClient
from medialib import MediaLib
from ezlogger import EzLogger
from cliinterface import CliInterface


class Config:
    """
    Main configuration, might be moved to a seperate file later

    --- Edit this section to your needs! ---
    """
    # Current version
    project_version = "0.0.1"
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
    # Don't set this to false unless you know what you are doing!
    enableCliInterface = True

    # Set this to true if you want the GTK+ Interface to be enabled
    enableGtkInterface = False

    """
    --- Configuration section ends here! ---
    """


class PlayerCtl:
    """
    VLC Media Player controller. This class contains the logic to interact
    with vlcclient and manage current playlist and status.
    """

    # TODO: play/pause syncronisation with VLC
    # TODO: MP3 tag access

    def __init__(self, startVol=70):

        self.vlc = VLCClient("::1")
        # VLC connection for monitoring thread to avoid multiple telnet send commands
        # at the same time, i.e. when user is changing songs while check is in
        # progress. This scenario would cause a telnet timeout and crash
        self.vlc_monitoring = VLCClient("::1")

        self.current_playing = ""
        self.current_playing_from_vlc = ""
        self.current_vlc_playlist_id = 4 - 1  # The Vlc playlist index starts with 4
        self.vlc_is_playing = ""
        self.next_playing = []
        self.thread_stopper = False

        try:
            self.vlc.connect()  # Esthablishing a connection via VLCClient class
            self.vlc_monitoring.connect()  # Seperate connection for monitoring thread
            logger.disp_log_entry("info", "connected to vlc media player")
        except ConnectionRefusedError:
            # TODO: Further error handling
            logger.error("Connection to vlc could not be established!")

        self.volume(startVol)  # Setting start value from config
        self.start_monitoring_thread()

    def _monitoring_thread(self):

        time.sleep(0.5)
        self.current_playing_from_vlc = self.get_vlc_internal_current_title()
        while not self.thread_stopper:
            try:  # Fixing inconsistency in Vlc playback status
                if self.current_playing_from_vlc != self.get_vlc_internal_current_title() \
                   and int(self.get_vlc_is_currently_playing()) == 1:
                    # Playing title has changed
                    if self.next_playing:  # If Playlist is not empty
                        self.current_playing = self.next_playing.pop(0)
                        self.delete_from_vlc_playlist(
                            self.current_vlc_playlist_id)
                        self.current_vlc_playlist_id = self.current_vlc_playlist_id + 1

                    self.current_playing_from_vlc = self.get_vlc_internal_current_title()
                    logger.disp_log_entry(
                        "playlist", "Now playing: " + self.get_clean_title(self.current_playing))

                if int(self.get_vlc_is_currently_playing()) == 0 and not self.next_playing:
                    # Playback is stopped and playlist is empty
                    self.current_playing = ""
                    self.delete_from_vlc_playlist(self.current_vlc_playlist_id)

            except ValueError:
                # TODO: This might be fixed with second vlc connection thread
                logger.warning("Inconsistency in VLC output detected")
                logger.warning("Playlist might be asynchronous!")

            self.vlc_is_playing = self.get_vlc_is_currently_playing()

            time.sleep(0.1)

    def start_monitoring_thread(self):
        """
        Starts the monitoring thread
        """
        Thread(target=self._monitoring_thread).start()

    def stop_monitoring_thread(self):
        """
        Stops the monitoring thread
        """
        self.thread_stopper = True

    def add(self, filepath):
        """
        Adds and plays the given file to the playlist
        """
        self.vlc.add(filepath)
        self.current_playing = filepath
        self.next_playing.insert(0, self.current_playing)
        self.vlc_is_playing = self.get_vlc_is_currently_playing()

    def enqueue(self, filepath):
        """
        Adds the given file to the end of the playlist
        """
        self.vlc.enqueue(filepath)
        self.next_playing.append(filepath)
        logger.disp_log_entry("playlist", "Added to queue: " +
                              self.get_clean_title(filepath))

    def next(self):
        """
        Plays the next title in the playlist
        """
        self.vlc.next()

    def skip(self, amount):
        """
        Skips a given amount of titles
        """
        for i in range(0, amount):
            self.next()
            time.sleep(0.5)  # FIXME: Direct access to playlist

    def volume(self, vol):
        """
        Sets the volume to the given input
        """
        self.vlc.volume(vol)
        logger.disp_log_entry("info", "setting volume to " + str(vol))

    def volup(self):
        """
        Increases the volume by 10 percent
        """
        self.vlc.volup()
        logger.disp_log_entry("info", "raising volume")

    def voldown(self):
        """
        Lowers the volume by 10 percent
        """
        self.vlc.voldown()
        logger.disp_log_entry("info", "lowering volume")

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
        self.next_playing = []
        self.current_playing = None
        logger.disp_log_entry("warning", "cleared playlist")

    def shutdown(self):
        """
        Terminates VLC and the title monitoring Thread
        """
        self.vlc.raw("shutdown")
        self.stop_monitoring_thread()
        logger.disp_log_entry("info", "Shutting down vlc client")

    def raw(self, command):
        """
        Executes a raw telnet command
        """
        self.vlc.raw(command)

    def get_volume(self):
        """
        Returns the current playback volume
        """
        current_volume = float(
            self.vlc.volume().decode("utf-8").replace(",", "."))
        while current_volume == 1.0:  # Fix for inconsistent vlc output
            current_volume = float(
                self.vlc.volume().decode("utf-8").replace(",", "."))
        return current_volume

    def get_vlc_internal_current_title(self):
        """
        Returns the internal name of the current playing title
        """
        return self.vlc_monitoring.raw("get_title")

    def get_vlc_is_currently_playing(self):
        """
        Returns 1 when playing, 0 when not
        """
        return self.vlc_monitoring.raw("is_playing")

    def delete_from_vlc_playlist(self, trackid):
        """
        Deletes the Song with the given id from VLC internal playlist
        """
        self.vlc_monitoring.raw("delete " + str(trackid))

    def get_current_playing(self):
        """
        Returns the current title in a formatted form
        """
        return self.get_clean_title(self.current_playing)

    def get_playlist(self):
        """
        Returns the current playlist
        """
        returnlist = self.next_playing
        # returnlist.insert(0,self.currentPlaying)
        return returnlist

    def get_clean_title(self, filepath):
        """
        Returns the clean title of a given filepath
        """
        # TODO: Add Mp3-Tag reader instead of using file names
        if filepath != "":
            return filepath.split("/")[-1].split(".")[-2].strip()
        else:
            return ""


if __name__ == '__main__':

    logger = EzLogger(Config.logger_verbosity)

    logger.disp_log_entry("info", "initializing, please wait...")

    # Sets window title
    sys.stdout.write('\33]0;Pubmusic2\a')

    if Config.autostart_vlc:
        user_os = sys.platform.lower()
        logger.info("attempting to start vlc automatically")
        if user_os == "linux" or user_os == "linux2":
            os.system(
                "nohup vlc --intf telnet  --telnet-password admin &>/dev/null &")
            time.sleep(1)  # Waiting for vlc to launch

        elif user_os == "win32" or user_os == "cygwin":
            # TODO: Only works for default vlc path, other way to get vlc.exe???
            # This took literally two hours for me to figure out
            os.spawnl(os.P_NOWAIT, 'C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe',
                      'vlc.exe --intf telnet --telnet-password admin')
            time.sleep(1)

        else:
            logger.warning(
                "You are running a currently unsupported system. Autostart is disabled")
            try:
                input = raw_input
            except NameError:
                pass

            input("Start VLC manually and press Enter to continue")

    logger.disp_log_entry(
        "welcome", "Welcome to Pubmusic2, version " + Config.project_version)

    # initializing our media library
    library = MediaLib(Config.media_dir)
    # initializing our media player controller
    player = PlayerCtl(Config.startVolume)

    if Config.enableCliInterface:
        # starting the main cli interface
        cli = CliInterface(logger, player, library)

    if Config.enableGtkInterface:
        # Late import of gtk, so it doesn't become a dependency
        from gtkinterface import GtkInterface
        gtkIf = GtkInterface(logger, player, library)

    if Config.autostart_playback:
        time.sleep(1)
        player.add(library.get_random_song())  # automatic first song

    while not player.thread_stopper:
        # TODO: Testing
        time.sleep(1)
