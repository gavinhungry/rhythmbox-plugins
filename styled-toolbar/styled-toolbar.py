#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Peas, GObject, RB

class StyledToolbar(GObject.Object, Peas.Activatable):
  object = GObject.property(type=GObject.Object)

  def do_activate(self):
    self.shell = self.object

    css = """
      .primary-toolbar {
        padding: 0 6px;
      }

      .primary-toolbar > separator {
        opacity: 0;
      }

      .primary-toolbar scale {
        min-width: 640px;
      }
    """

    provider = Gtk.CssProvider.new()
    provider.load_from_data(css.encode())

    context = Gtk.StyleContext()
    context.add_provider_for_screen(
      self.shell.props.window.props.screen,
      provider,
      Gtk.STYLE_PROVIDER_PRIORITY_USER
    )
