""" GTK interface """
import sys
import time
from threading import Thread

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GtkInterface(object):
    """
    GTK+ interface for Pubmusic2
    """

    def __init__(self, logger, player, library):

        self.logger = logger
        self.player = player
        self.library = library

        builder = Gtk.Builder()
        builder.add_from_file("pubmusic_gtk.glade")
        builder.connect_signals(GtkEventHandler(
            self.logger, self.player, self.library))

        window_main = builder.get_object("window_main")
        window_main.set_title("Pubmusic2")

        # Volume init
        self.vol_slider = builder.get_object("slider_volume")
        self.header_bar = builder.get_object("header_bar")

        # Display the main window
        window_main.show_all()
        self.gtk_thread = Thread(target=self._gtk_thread).start()

        self.start_gui_updater_thread()

    def _gtk_thread(self):
        """
        Thread for managing GTK+
        """
        try:
            Gtk.main()
        except Exception:
            logger.error("Gui has crashed!")

    def _gui_updater_thread(self):
        """
        Thread that synchronizes the gui with values from the player
        """
        # TODO: Independent thread stopping mechanism
        time.sleep(2)

        while not self.player.thread_stopper:
            # update window subtitle
            # FIXME: This causes random crashes
            # self.headerBar.set_title(self.player.get_current_playing())

            # Set volume slider to actual volume
            try:
                self.vol_slider.set_value(self.player.get_volume() / 100)
            except ValueError:
                self.logger.error("Could not recieve volume level for gui")

            time.sleep(1)  # Should be a good interval (for now)

    def start_gui_updater_thread(self):
        self.gui_updateder_thread = Thread(target=self._gui_updater_thread).start()


class GtkEventHandler(object):
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
        for i, song in enumerate(self.library.get_song_list()):
            print(str(i).zfill(4) + " - " + self.player.get_clean_title(song))

    def on_btn_playlist_clicked(self, *args):
        for i, song in enumerate(self.player.get_playlist()):
            print(str(i) + " - " + self.player.get_clean_title(song))

    def on_btn_close_clicked(self, *args):
        Gtk.main_quit()
        self.player.shutdown()
        sys.exit()

    def on_slider_volume_value_changed(self, slider, *args):
        # print(dir(slider))
        self.player.volume(slider.get_value() * 100)

    def on_btn_autofill_clicked(self, *args):
        for x in range(0, 10):
            self.player.enqueue(self.library.get_random_song())

    def on_window_main_destroy(self, *args):
        self.on_btn_close_clicked()
