#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2021 Carlos Eduardo Sequeiros Borja <carseq@amu.edu.pl>
#  

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from sys import argv
from VisMol.libs import gtk_stuff
from VisMol.libs.parsers import parse_pdb

if __name__ == "__main__":
    """ Function doc """
    data = parse_pdb(argv[1])
    test = gtk_stuff.VMWindow(draw_type="points", data=data)
    # test.load_data(data)
    wind = Gtk.Window()
    wind.add(test)

    wind.connect("delete-event", Gtk.main_quit)
    wind.connect("key-press-event", test.key_pressed)
    wind.connect("key-release-event", test.key_released)
    wind.show_all()
    Gtk.main()

