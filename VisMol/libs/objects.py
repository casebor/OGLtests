#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2021 Carlos Eduardo Sequeiros Borja <carseq@amu.edu.pl>
#  

import numpy as np

class VMNode():
    """docstring for VMAtom"""
    
    def __init__ (self, nid, x, y, z):
        self.id = nid
        self.x = x
        self.y = y
        self.z = z
        self.pos = np.array([x, y, z], dtype=np.float32)
        self.bonds = []
    
    def set_pos(self, new_pos: np.array):
        """ Function doc """
        assert new_pos.shape[0] == 3
        self.pos = new_pos
    
    def add_bond(self, other_node):
        """ Function doc """
        if other_node not in self.bonds:
            self.bonds.append(other_node)
    
    def del_bond(self, other_node):
        """ Function doc """
        if other_node in self.bonds:
            self.bonds.remove(other_node)

class VMAtom(VMNode):
    """docstring for VMAtom"""
    def __init__(self, nid, x, y, z, name="UNK", radius=1.0, element="X",
                 parent=None, color=None):
        super().__init__(nid, x, y, z)
        self.rad = radius
        self.name = name
        self.element = element
        self.parent = parent
        if color is None:
            self.color = np.array([0,1,0], dtype=np.float32)
        else:
            self.color = np.array(color)

class GLContainer():
    """docstring for GLContainer"""
    def __init__(self, obj_list: list):
        self.xyz = np.zeros((len(obj_list), 3), dtype=np.float32)
        self.colors = np.zeros((len(obj_list), 3), dtype=np.float32)
        self.radii = np.zeros(len(obj_list), dtype=np.float32)
        for i, obj in enumerate(obj_list):
            self.xyz[i,:] = obj.pos
            self.colors[i,:] = obj.color
            self.radii[i] = obj.rad
