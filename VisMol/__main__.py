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
from VisMol.libs.parsers import parse_pdb, parse_obj
# from VisMol.libs.shaders.shaders import vertex_shader_glumpy, fragment_shader_glumpy
import VisMol.libs.shaders.shaders as vms

if __name__ == "__main__":
    """ Function doc """
    if argv[1].endswith("pdb"):
        data = parse_pdb(argv[1])
    elif argv[1].endswith("obj"):
        data = parse_obj(argv[1])
    test = gtk_stuff.VMWindow(draw_type="points")
    # test = gtk_stuff.VMWindow(vertex_shader=vms.vertex_shader_glumpy,
    #        fragment_shader = vms.fragment_shader_glumpy, draw_type="points")
    test.load_data(data)
    wind = Gtk.Window()
    wind.add(test)

    wind.connect("delete-event", Gtk.main_quit)
    wind.connect("key-press-event", test.key_pressed)
    wind.connect("key-release-event", test.key_released)
    wind.show_all()
    Gtk.main()

