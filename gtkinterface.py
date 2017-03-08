import sys
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from threading import Thread


class gtkInterface(object):
    """
    GTK+ interface for Pubmusic2
    """

    def __init__(self, logger, player, library):

        self.logger = logger
        self.player = player
        self.library = library

        builder = Gtk.Builder()
        builder.add_from_file("pubmusic_gtk.glade")
        builder.connect_signals(gtkEventHandler(
            self.logger, self.player, self.library))

        window_main = builder.get_object("window_main")
        window_main.set_title("Pubmusic2")

        # Volume init
        self.volSlider = builder.get_object("slider_volume")
        self.headerBar = builder.get_object("header_bar")

        # Display the main window
        window_main.show_all()
        self.gtkThread = Thread(target=self._gtkThread).start()

        self.startGuiUpdaterThread()

    def _gtkThread(self):
        """
        Thread for managing GTK+
        """
        try:
            Gtk.main()
        except Exception:
            logger.error("Gui has crashed!")

    def _guiUpdaterThread(self):
        """
        Thread that synchronizes the gui with values from the player
        """
        # TODO: Independent thread stopping mechanism
        time.sleep(2)

        while not self.player.threadStopper:
            # update window subtitle
            # FIXME: This causes random crashes
            # self.headerBar.set_title(self.player.getCurrentPlaying())

            # Set volume slider to actual volume
            try:
                self.volSlider.set_value(self.player.getVolume() / 100)
            except ValueError:
                self.logger.error("Could not recieve volume level for gui")

            time.sleep(1)  # Should be a good interval (for now)

    def startGuiUpdaterThread(self):
        self.guiUpdaterThread = Thread(target=self._guiUpdaterThread).start()


class gtkEventHandler(object):
    """
    Handlers for all GUI elements
    """

    def __init__(self, logger, player, library):

        self.logger = logger
        self.player = player
        self.library = library

    def on_btn_next_clicked(self, *args):
        self.player.next()

    def on_btn_library_clicked(self, *args):
        for i, song in enumerate(self.library.getSongList()):
            print(str(i).zfill(4) + " - " + self.player.getCleanTitle(song))

    def on_btn_playlist_clicked(self, *args):
        for i, song in enumerate(self.player.getPlaylist()):
            print(str(i) + " - " + self.player.getCleanTitle(song))

    def on_btn_close_clicked(self, *args):
        Gtk.main_quit()
        self.player.shutdown()
        sys.exit()

    def on_slider_volume_value_changed(self, slider, *args):
        # print(dir(slider))
        self.player.volume(slider.get_value() * 100)

    def on_btn_autofill_clicked(self, *args):
        for x in range(0, 10):
            self.player.enqueue(self.library.getRandomSong())

    def on_window_main_destroy(self, *args):
        self.on_btn_close_clicked()
