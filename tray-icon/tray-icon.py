#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Peas, GObject, RB

class TrayIcon(GObject.Object, Peas.Activatable):
  object = GObject.property(type=GObject.Object)

  def on_quit(self, menuitem):
    self.shell.quit()

  def on_hide(self, widget, event):
    self.win.hide()
    return True

  def on_change(self, player, is_playing):
    if not is_playing:
      self.icon.set_tooltip_text('Rhythmbox')
      return

    entry = self.player.get_playing_entry()

    self.icon.set_tooltip_text("%s - %s" % (
      entry.get_string(RB.RhythmDBPropType.ARTIST),
      entry.get_string(RB.RhythmDBPropType.TITLE)
    ))

  def on_icon_click(self, icon):
    self.win.present()

  def on_icon_context(self, icon, button, time):
    quit = Gtk.MenuItem()
    quit.set_label('Quit Rhythmbox')
    quit.connect('activate', self.on_quit)

    menu = Gtk.Menu()
    menu.append(quit)
    menu.show_all()

    menu.popup(None, None, None, Gtk.StatusIcon.position_menu, button, time)

  def do_activate(self):
    self.shell = self.object
    self.player = self.shell.props.shell_player
    self.win = self.shell.get_property('window')

    self.icon = Gtk.StatusIcon()
    self.icon.set_visible(False)

    self.icon.set_from_icon_name('rhythmbox-panel')
    self.icon.set_tooltip_text('Rhythmbox')

    self.icon.connect('activate', self.on_icon_click)
    self.icon.connect('popup-menu', self.on_icon_context)

    self.icon.set_visible(True)

    self.change_handler = self.player.connect('playing-changed', self.on_change)
    self.hide_handler = self.win.connect('delete-event', self.on_hide)

  def do_deactivate(self):
    self.icon.set_visible(False)
    self.player.disconnect(self.change_handler)
    self.win.disconnect(self.hide_handler)
