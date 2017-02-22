import sys
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
      builder.connect_signals(gtkEventHandler(self.logger, self.player, self.library))
      
      window_main = builder.get_object("window_main")
      window_main.set_title("Pubmusic2")
      
      # Volume init
      volSlider = builder.get_object("slider_volume")
      volSlider.set_value(self.player.getVolume())
      #unset(volSlider)

      # Display the main window
      window_main.show_all()
      self.gtkThread = Thread(target=self._gtkThread).start()
         
   def _gtkThread (self):
      """
      Thread for managing GTK+
      """
      Gtk.main()
   
class gtkEventHandler(object):
   
   def __init__ (self, logger, player, library):
      
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
         print (str(i) + " - " +self.player.getCleanTitle(song))
      
   def on_btn_close_clicked(self, *args):
      Gtk.main_quit()
      self.player.shutdown()
      sys.exit()
      
   def on_slider_volume_value_changed(self, slider, *args):
      #print(dir(slider))
      self.player.volume(slider.get_value() * 100)
      
   def on_btn_autofill_clicked(self, *args):
      for x in range(0,10):
         self.player.enqueue(self.library.getRandomSong())