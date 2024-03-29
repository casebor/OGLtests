#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  vaos.py
#  
#  Copyright 2017 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import ctypes
import numpy as np
import sphere_data as sphd

from OpenGL import GL

def _get_normal(vec1, vec2):
    """ Function doc """
    return (vec1 + vec2) / np.linalg.norm(vec1 + vec2)

def make_dots(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    coords = np.array([[ 1.0, 1.0, 0.0],[ 0.0, 1.0, 0.0],[ 1.0, 0.0, 0.0],
                       [-1.0, 0.0, 0.0],[-1.0, 1.0, 0.0],[-1.0,-1.0, 0.0],
                       [ 0.0,-1.0, 0.0],[ 1.0,-1.0, 0.0],[ 0.0, 0.0, 0.0]],dtype=np.float32)
    colors = np.array([ 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0,
                        0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
                        0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0],dtype=np.float32)
    # coords = coords.flatten()
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords)*3, coords, GL.GL_STATIC_DRAW)
    position = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(position)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, col_vbo), int(len(coords))

def make_diamonds(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    coords = np.array([-1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
                       -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                       -1.0,-1.0, 0.0, 0.0,-1.0, 0.0, 1.0,-1.0, 0.0],dtype=np.float32)
    colors = np.array([ 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
                        1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0,
                        0.5, 0.5, 0.5, 0.2, 0.3, 0.4, 0.9, 0.5, 0.1],dtype=np.float32)
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    position = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(position)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, col_vbo), int(len(coords)/3)

def make_circles(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    coords = np.array([ 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0,
                       -1.0, 0.0, 0.0,-1.0, 1.0, 0.0,-1.0,-1.0, 0.0,
                        0.0,-1.0, 0.0, 1.0,-1.0, 0.0, 0.0, 0.0, 0.0],dtype=np.float32)
    colors = np.array([ 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0,
                        0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
                        0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0],dtype=np.float32)
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    position = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(position)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, col_vbo), int(len(coords)/3)

def make_cylinders(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    coords = np.array([-1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
                       -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                       -1.0,-1.0, 0.0, 0.0,-1.0, 0.0, 1.0,-1.0, 0.0],dtype=np.float32)
    colors = np.array([ 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0,
                        0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
                        0.0, 1.0, 0.0, 0.0, 0.5, 0.5, 0.0, 1.0, 0.0],dtype=np.float32)
    indexes = np.array([0, 1, 1, 2, 3, 4, 4, 5, 6, 7, 7, 8], dtype=np.uint32)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    position = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(position)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (ind_vbo, coord_vbo, col_vbo), int(len(indexes))

def make_lines(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    coords = np.array([-1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
                       -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                       -1.0,-1.0, 0.0, 0.0,-1.0, 0.0, 1.0,-1.0, 0.0],dtype=np.float32)
    colors = np.array([ 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0,
                        0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
                        0.0, 1.0, 0.0, 0.0, 0.5, 0.5, 0.0, 1.0, 0.0],dtype=np.float32)
    indexes = np.array([0, 1, 1, 2, 3, 4, 4, 5, 6, 7, 7, 8], dtype=np.uint32)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    position = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(position)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (ind_vbo, coord_vbo, col_vbo), int(len(indexes))

def make_antialias(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    coords = np.array([-1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
                       -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                       -1.0,-1.0, 0.0, 0.0,-1.0, 0.0, 1.0,-1.0, 0.0],dtype=np.float32)
    colors = np.array([ 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0,
                        0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
                        0.0, 1.0, 0.0, 0.0, 0.5, 0.5, 0.0, 1.0, 0.0],dtype=np.float32)
    indexes = np.array([0, 1, 1, 2, 3, 4, 4, 5, 6, 7, 7, 8], dtype=np.uint32)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    position = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(position)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (ind_vbo, coord_vbo, col_vbo), int(len(indexes))

def make_pseudospheres(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    coords = np.array([-2.0, 2.0, 0.0, 2.0, 2.0, 0.0,
                       -2.0,-2.0, 0.0, 2.0,-2.0, 0.0],dtype=np.float32)
    colors = np.array([ 1.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                        0.0, 0.0, 1.0, 0.5, 0.5, 0.0],dtype=np.float32)
    radios = np.array([2.2, 1.8, 0.9, 1.1], dtype=np.float32)
    indexes = np.array([0, 1, 2, 3], dtype=np.uint32)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_color)
    GL.glVertexAttribPointer(gl_color, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    rad_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, rad_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, radios.itemsize*len(radios), radios, GL.GL_STATIC_DRAW)
    gl_rad = GL.glGetAttribLocation(program, "vert_rad")
    GL.glEnableVertexAttribArray(gl_rad)
    GL.glVertexAttribPointer(gl_rad, 1, GL.GL_FLOAT, GL.GL_FALSE, colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_color)
    GL.glDisableVertexAttribArray(gl_rad)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (ind_vbo, coord_vbo, col_vbo, rad_vbo), int(len(indexes))

def make_non_bonded(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    coords = np.array([-1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
                       -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                       -1.0,-1.0, 0.0, 0.0,-1.0, 0.0, 1.0,-1.0, 0.0],dtype=np.float32)
    colors = np.array([ 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
                        1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0,
                        0.5, 0.5, 0.5, 0.2, 0.3, 0.4, 0.9, 0.5, 0.1],dtype=np.float32)
    indexes = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype=np.uint32)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_color)
    GL.glVertexAttribPointer(gl_color, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_color)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (ind_vbo, coord_vbo, col_vbo), int(len(indexes))

def make_arrow(program):
    """ Function doc """
    points = int(90)
    coords = np.zeros((points+2)*3, dtype=np.float32)
    colors = np.array([0, 1, 0]*(points+2), dtype=np.float32)
    indexes = []
    angle = 0.0
    to_add = 360.0/points
    for i in range(0, points*3, 3):
        coords[i] = np.cos(angle*np.pi/180)
        coords[i+2] = np.sin(angle*np.pi/180)
        angle += to_add
    coords[-6] = 0.0 # Point
    coords[-5] = 1.5 # Point
    coords[-4] = 0.0 # Point
    coords[-3] = 0.0 # Base center
    coords[-2] = 0.0 # Base center
    coords[-1] = 0.0 # Base center
    for i in range(points-1):
        indexes.append(i)
        indexes.append(i+1)
        indexes.append(points)
    indexes.append(points-1)
    indexes.append(0)
    indexes.append(points)
    for i in range(points-1):
        indexes.append(points+1)
        indexes.append(i+1)
        indexes.append(i)
    indexes.append(points+1)
    indexes.append(0)
    indexes.append(points-1)
    indexes = np.array(indexes, dtype=np.uint32)
    
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_color)
    GL.glVertexAttribPointer(gl_color, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_color)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (ind_vbo, coord_vbo, col_vbo), int(len(indexes))

def make_geom_cones(program):
    """ Function doc """
    coords = np.array([ 1.00000, 0.00000, 0.00000, 0.86603, 0.00000, 0.50000, 0.00000, 1.00000, 0.00000,
                        0.86603, 0.00000, 0.50000, 0.50000, 0.00000, 0.86603, 0.00000, 1.00000, 0.00000,
                        0.50000, 0.00000, 0.86603, 0.00000, 0.00000, 1.00000, 0.00000, 1.00000, 0.00000,
                        0.00000, 0.00000, 1.00000,-0.50000, 0.00000, 0.86603, 0.00000, 1.00000, 0.00000,
                       -0.50000, 0.00000, 0.86603,-0.86603, 0.00000, 0.50000, 0.00000, 1.00000, 0.00000,
                       -0.86603, 0.00000, 0.50000,-1.00000, 0.00000, 0.00000, 0.00000, 1.00000, 0.00000,
                       -1.00000, 0.00000, 0.00000,-0.86603, 0.00000,-0.50000, 0.00000, 1.00000, 0.00000,
                       -0.86603, 0.00000,-0.50000,-0.50000, 0.00000,-0.86603, 0.00000, 1.00000, 0.00000,
                       -0.50000, 0.00000,-0.86603,-0.00000, 0.00000,-1.00000, 0.00000, 1.00000, 0.00000,
                       -0.00000, 0.00000,-1.00000, 0.50000, 0.00000,-0.86603, 0.00000, 1.00000, 0.00000,
                        0.50000, 0.00000,-0.86603, 0.86603, 0.00000,-0.50000, 0.00000, 1.00000, 0.00000,
                        0.86603, 0.00000,-0.50000, 1.00000, 0.00000, 0.00000, 0.00000, 1.00000, 0.00000,
                        1.00000, 0.00000, 0.00000, 0.86603, 0.00000, 0.50000, 0.00000, 0.00000, 0.00000,
                        0.86603, 0.00000, 0.50000, 0.50000, 0.00000, 0.86603, 0.00000, 0.00000, 0.00000,
                        0.50000, 0.00000, 0.86603, 0.00000, 0.00000, 1.00000, 0.00000, 0.00000, 0.00000,
                        0.00000, 0.00000, 1.00000,-0.50000, 0.00000, 0.86603, 0.00000, 0.00000, 0.00000,
                       -0.50000, 0.00000, 0.86603,-0.86603, 0.00000, 0.50000, 0.00000, 0.00000, 0.00000,
                       -0.86603, 0.00000, 0.50000,-1.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000,
                       -1.00000, 0.00000, 0.00000,-0.86603, 0.00000,-0.50000, 0.00000, 0.00000, 0.00000,
                       -0.86603, 0.00000,-0.50000,-0.50000, 0.00000,-0.86603, 0.00000, 0.00000, 0.00000,
                       -0.50000, 0.00000,-0.86603,-0.00000, 0.00000,-1.00000, 0.00000, 0.00000, 0.00000,
                       -0.00000, 0.00000,-1.00000, 0.50000, 0.00000,-0.86603, 0.00000, 0.00000, 0.00000,
                        0.50000, 0.00000,-0.86603, 0.86603, 0.00000,-0.50000, 0.00000, 0.00000, 0.00000,
                        0.86603, 0.00000,-0.50000, 1.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000], dtype=np.float32)
    
    #norms = np.array([ 0.69474739, 0.69474739, 0.18615066, 0.69474739, 0.69474739, 0.18615066, 0.69474739, 0.69474739, 0.18615066,
                       #0.50858897, 0.69474775, 0.50858897, 0.50858897, 0.69474775, 0.50858897, 0.50858897, 0.69474775, 0.50858897,
                       #0.18615066, 0.69474739, 0.69474739, 0.18615066, 0.69474739, 0.69474739, 0.18615066, 0.69474739, 0.69474739,
                      #-0.18615066, 0.69474739, 0.69474739,-0.18615066, 0.69474739, 0.69474739,-0.18615066, 0.69474739, 0.69474739,
                      #-0.50858897, 0.69474775, 0.50858897,-0.50858897, 0.69474775, 0.50858897,-0.50858897, 0.69474775, 0.50858897,
                      #-0.69474739, 0.69474739, 0.18615066,-0.69474739, 0.69474739, 0.18615066,-0.69474739, 0.69474739, 0.18615066,
                      #-0.69474739, 0.69474739,-0.18615066,-0.69474739, 0.69474739,-0.18615066,-0.69474739, 0.69474739,-0.18615066,
                      #-0.50858897, 0.69474775,-0.50858897,-0.50858897, 0.69474775,-0.50858897,-0.50858897, 0.69474775,-0.50858897,
                      #-0.18615066, 0.69474739,-0.69474739,-0.18615066, 0.69474739,-0.69474739,-0.18615066, 0.69474739,-0.69474739,
                       #0.18615066, 0.69474739,-0.69474739, 0.18615066, 0.69474739,-0.69474739, 0.18615066, 0.69474739,-0.69474739,
                       #0.50858897, 0.69474775,-0.50858897, 0.50858897, 0.69474775,-0.50858897, 0.50858897, 0.69474775,-0.50858897,
                       #0.69474739, 0.69474739,-0.18615066, 0.69474739, 0.69474739,-0.18615066, 0.69474739, 0.69474739,-0.18615066,
                       #0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       #0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       #0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       #0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       #0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       #0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       #0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       #0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       #0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       #0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       #0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       #0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,], dtype=np.float32)
    
    norms = np.array([ 0.70710677, 0.70710677, 0.00000000, 0.61237276, 0.70710814, 0.35355005, 0.48506978, 0.72760886, 0.48506978,
                       0.61237276, 0.70710814, 0.35355005, 0.35355005, 0.70710814, 0.61237276, 0.17754796, 0.72760725, 0.66261935,
                       0.35355005, 0.70710814, 0.61237276, 0.00000000, 0.70710677, 0.70710677,-0.17754796, 0.72760725, 0.66261935,
                       0.00000000, 0.70710677, 0.70710677,-0.35355005, 0.70710814, 0.61237276,-0.48506978, 0.72760886, 0.48506978,
                      -0.35355005, 0.70710814, 0.61237276,-0.61237276, 0.70710814, 0.35355005,-0.66261935, 0.72760725, 0.17754796,
                      -0.61237276, 0.70710814, 0.35355005,-0.70710677, 0.70710677, 0.00000000,-0.66261935, 0.72760725,-0.17754796,
                      -0.70710677, 0.70710677, 0.00000000,-0.61237276, 0.70710814,-0.35355005,-0.48506978, 0.72760886,-0.48506978,
                      -0.61237276, 0.70710814,-0.35355005,-0.35355005, 0.70710814,-0.61237276,-0.17754796, 0.72760725,-0.66261935,
                      -0.35355005, 0.70710814,-0.61237276, 0.00000000, 0.70710677,-0.70710677, 0.17754796, 0.72760725,-0.66261935,
                       0.00000000, 0.70710677,-0.70710677, 0.35355005, 0.70710814,-0.61237276, 0.48506978, 0.72760886,-0.48506978,
                       0.35355005, 0.70710814,-0.61237276, 0.61237276, 0.70710814,-0.35355005, 0.66261935, 0.72760725,-0.17754796,
                       0.61237276, 0.70710814,-0.35355005, 0.70710677, 0.70710677, 0.00000000, 0.66261935, 0.72760725, 0.17754796,
                       0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000,
                       0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000, 0.00000000,-1.00000000, 0.00000000], dtype=np.float32)
    
    colors = np.array([0, 1, 0]*72, dtype=np.float32)
    
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_color)
    GL.glVertexAttribPointer(gl_color, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    norm_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, norm_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, norms.itemsize*len(norms), norms, GL.GL_STATIC_DRAW)
    gl_norm = GL.glGetAttribLocation(program, "vert_norm")
    GL.glEnableVertexAttribArray(gl_norm)
    GL.glVertexAttribPointer(gl_norm, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*norms.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_color)
    GL.glDisableVertexAttribArray(gl_norm)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, col_vbo, norm_vbo), int(len(coords)/3)

def make_select_box(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    #coords = np.array([-1.0, 1.0, 0.0,-1.0,-1.0, 0.0, 1.0,-1.0, 0.0,
                        #1.0, 1.0, 0.0,-1.0, 1.0, 0.0],dtype=np.float32)
    coords = np.array([ 0.2, 0.2, 0.0, 0.2, 0.7, 0.0, 0.7, 0.7, 0.0,
                        0.7, 0.2, 0.0, 0.2, 0.2, 0.0],dtype=np.float32)
    colors = np.array([ 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5,
                        0.0, 0.5, 0.5, 0.0, 0.5, 0.5],dtype=np.float32)
    indexes = np.array([0, 1, 2, 3, 4], dtype=np.uint32)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    position = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(position)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (ind_vbo, coord_vbo, col_vbo), int(len(indexes))

def make_edit_mode(program, points):
    """ Function doc """
    amount = int(len(points))
    coords = np.array([], dtype=np.float32)
    colors = np.array([], dtype=np.float32)
    centers = np.array([], dtype=np.float32)
    indexes = np.array([], dtype=np.uint32)
    for i in range(0, amount, 3):
        center = [points[i], points[i+1], points[i+2]]
        verts, inds, cols = sphd.get_sphere(center, 1.1, [0, 1, 0], level="level_2")
        center *= int(verts.size/3)
        to_add = int(verts.size/3) * int(i/3)
        inds += to_add
        coords = np.concatenate((coords,verts))
        colors = np.concatenate((colors,cols))
        centers = np.concatenate((centers,center))
        indexes = np.concatenate((indexes,inds))
    
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    coords = np.array(coords,dtype=np.float32)
    colors = np.array(colors,dtype=np.float32)
    centers = np.array(centers,dtype=np.float32)
    indexes = np.array(indexes, dtype=np.uint32)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    centr_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, centr_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, centers.itemsize*len(centers), centers, GL.GL_STATIC_DRAW)
    gl_center = GL.glGetAttribLocation(program, "vert_centr")
    GL.glEnableVertexAttribArray(gl_center)
    GL.glVertexAttribPointer(gl_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*centers.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_center)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, centr_vbo, col_vbo), int(len(indexes))

def make_text_texture():
    """ Function doc """
    from PIL import Image
    image_a = Image.open("SimSun_ExtB.tga")
    #print("opened file: size=", image_a.size, "format=", image_a.format)
    ix = image_a.size[0]
    iy = image_a.size[1]
    image_a = np.array(list(image_a.getdata()), np.uint8)
    text_texture = GL.glGenTextures(1)
    GL.glActiveTexture(GL.GL_TEXTURE0)
    GL.glBindTexture(GL.GL_TEXTURE_2D, text_texture)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, ix, iy, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image_a)
    return text_texture

def make_text(program):
    """ Function doc """
    phrase = "Hello World!!!"
    text_id = np.zeros(len(phrase),np.uint32)
    indexes = np.zeros(len(phrase),np.uint32)
    for i,letter in enumerate(phrase):
        text_id[i] = ord(letter)
        indexes[i] = i
    coords = np.zeros(len(phrase)*3,np.float32)
    point = [-1, 1, 0]
    for i in range(0, coords.size, 3):
        coords[i] = point[0] + i*0.06
        coords[i+1] = point[1]
        coords[i+2] = point[2]
    
    #coords = np.array([-1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
    #                   -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
    #                   -1.0,-1.0, 0.0, 0.0,-1.0, 0.0, 1.0,-1.0, 0.0],dtype=np.float32)
    #text_id = np.array([33, 34, 35, 56, 111, 122, 87, 90, 666], dtype=np.int32)
    #indexes = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype=np.uint32)
    
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    tex_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, tex_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, text_id.itemsize*len(text_id), text_id, GL.GL_STATIC_DRAW)
    gl_texture = GL.glGetAttribLocation(program, "vert_id")
    GL.glEnableVertexAttribArray(gl_texture)
    GL.glVertexAttribPointer(gl_texture, 1, GL.GL_FLOAT, GL.GL_FALSE, 1*text_id.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_texture)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (ind_vbo, coord_vbo, tex_vbo), int(len(indexes))

def make_texture_texture():
    """ Function doc """
    from PIL import Image
    image_a = Image.open("test.tga")
    #print("opened file: size=", image_a.size, "format=", image_a.format)
    ix = image_a.size[0]
    iy = image_a.size[1]
    image_a = np.array(list(image_a.getdata()),np.uint8)
    tex_texture = GL.glGenTextures(1)
    #tex_texture = GL.glGenTextures(2)
    GL.glActiveTexture(GL.GL_TEXTURE0)
    GL.glBindTexture(GL.GL_TEXTURE_2D, tex_texture)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, ix, iy, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image_a)
    #image_b = img.open("cry.bmp")
    #ix = image_b.size[0]
    #iy = image_b.size[1]
    #image_b = image_b.tobytes("raw", "RGBX", 0, -1)
    #GL.glActiveTexture(GL.GL_TEXTURE1)
    #GL.glBindTexture(GL.GL_TEXTURE_2D, tex_texture[1])
    #GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    #GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    #GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    #GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    #GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, ix, iy, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image_b)
    return tex_texture

def make_texture(program):
    """ Function doc """
    coords = np.array([-1.0, 1.0, 0.0,-1.0,-1.0, 0.0, 1.0,-1.0, 0.0,
                       -1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,-1.0, 0.0,],dtype=np.float32)
    textur = np.array([ 0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
                        0.0, 0.0, 1.0, 0.0, 1.0, 1.0],dtype=np.float32)
    
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    tex_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, tex_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, textur.itemsize*len(textur), textur, GL.GL_STATIC_DRAW)
    gl_texture = GL.glGetAttribLocation(program, "vert_text")
    GL.glEnableVertexAttribArray(gl_texture)
    GL.glVertexAttribPointer(gl_texture, 2, GL.GL_FLOAT, GL.GL_FALSE, 2*textur.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_texture)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, tex_vbo), int(len(coords)/3)

def make_dots_surface(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    coords = np.array([-1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
                       -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                       -1.0,-1.0, 0.0, 0.0,-1.0, 0.0, 1.0,-1.0, 0.0],dtype=np.float32)
    colors = np.array([ 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
                        1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0,
                        0.5, 0.5, 0.5, 0.2, 0.3, 0.4, 0.9, 0.5, 0.1],dtype=np.float32)
    indexes = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype=np.uint32)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_color)
    GL.glVertexAttribPointer(gl_color, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_color)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (ind_vbo, coord_vbo, col_vbo), int(len(indexes))

def make_icosahedron(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    coords = np.array([-1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
                       -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                       -1.0,-1.0, 0.0, 0.0,-1.0, 0.0, 1.0,-1.0, 0.0],dtype=np.float32)
    colors = np.array([ 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
                        1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0,
                        0.5, 0.5, 0.5, 0.2, 0.3, 0.4, 0.9, 0.5, 0.1],dtype=np.float32)
    indexes = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype=np.uint32)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_color)
    GL.glVertexAttribPointer(gl_color, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_color)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (ind_vbo, coord_vbo, col_vbo), int(len(indexes))

def make_sphere(program, level="level_2"):
    """ Function doc """
    nucleus = [-1.0, 1.0, 0.0, 1.0, 1.0, 0.0,-1.0,-1.0, 0.0, 1.0,-1.0, 0.0]
    colores = [ 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.5, 0.5]
    qtty = int(len(nucleus)/3)
    coords = np.array([], dtype=np.float32)
    centers = np.array([], dtype=np.float32)
    colors = np.array([], dtype=np.float32)
    indexes = np.array([], dtype=np.uint32)
    for i in range(qtty):
        crds = np.copy(sphd.sphere_vertices[level])
        inds = np.copy(sphd.sphere_triangles[level])
        offset = int(len(crds)/3)
        cols = np.array(colores[i*3:(i+1)*3]*offset, dtype=np.float32)
        cnts = np.array(nucleus[i*3:(i+1)*3]*offset, dtype=np.float32)
        for j in range(offset):
            crds[j*3] = crds[j*3] + nucleus[i*3]
            crds[j*3+1] = crds[j*3+1] + nucleus[i*3+1]
            crds[j*3+2] = crds[j*3+2] + nucleus[i*3+2]
        inds += i*offset
        coords = np.concatenate((coords, crds))
        centers = np.concatenate((centers, cnts))
        colors = np.concatenate((colors, cols))
        indexes = np.concatenate((indexes, inds))
    #coords = np.array(coords, dtype=np.float32)
    #indexes = np.array(indexes, dtype=np.uint32)
    #colors = np.array(colors, dtype=np.float32)
    
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    centr_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, centr_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, centers.itemsize*len(centers), centers, GL.GL_STATIC_DRAW)
    gl_center = GL.glGetAttribLocation(program, "vert_centr")
    GL.glEnableVertexAttribArray(gl_center)
    GL.glVertexAttribPointer(gl_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*centers.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_center)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (ind_vbo, coord_vbo, col_vbo), int(len(indexes))


#------------------------------------------------------------------------------#

def make_impostor_sph(program):
    """ Function doc """
    box = np.array([[-1.0,-1.0,-1.0], [-1.0, 1.0,-1.0], [-1.0,-1.0, 1.0],
                    [-1.0, 1.0,-1.0], [-1.0,-1.0, 1.0], [-1.0, 1.0, 1.0],
                    [-1.0,-1.0, 1.0], [-1.0, 1.0, 1.0], [ 1.0,-1.0, 1.0],
                    [-1.0, 1.0, 1.0], [ 1.0,-1.0, 1.0], [ 1.0, 1.0, 1.0],
                    [ 1.0,-1.0, 1.0], [ 1.0, 1.0, 1.0], [ 1.0,-1.0,-1.0],
                    [ 1.0, 1.0, 1.0], [ 1.0,-1.0,-1.0], [ 1.0, 1.0,-1.0],
                    [ 1.0,-1.0, 1.0], [ 1.0, 1.0,-1.0], [-1.0,-1.0,-1.0],
                    [ 1.0, 1.0,-1.0], [-1.0,-1.0,-1.0], [-1.0, 1.0,-1.0],
                    [-1.0,-1.0,-1.0], [-1.0,-1.0, 1.0], [ 1.0,-1.0,-1.0],
                    [-1.0,-1.0, 1.0], [ 1.0,-1.0,-1.0], [ 1.0,-1.0, 1.0],
                    [-1.0, 1.0,-1.0], [-1.0, 1.0, 1.0], [ 1.0, 1.0,-1.0],
                    [-1.0, 1.0, 1.0], [ 1.0, 1.0,-1.0], [ 1.0, 1.0, 1.0]], dtype=np.float32)
    
    # box = np.array([[-1.0,-1.0,-1.0], [-1.0,-1.0, 1.0], [ 1.0,-1.0, 1.0],
    #                 [ 1.0,-1.0,-1.0], [-1.0, 1.0,-1.0], [-1.0, 1.0, 1.0],
    #                 [ 1.0, 1.0, 1.0], [ 1.0, 1.0,-1.0]], dtype=np.float32)
    
    # indexes = np.array([0,1,2], dtype=np.uint32)
    centers = np.random.rand(20,3).astype(np.float32)*5 - 2.5
    colors = np.random.rand(20,3).astype(np.float32)
    radii = np.random.rand(20).astype(np.float32)
    
    coords = np.array([box*r + c for r,c in zip(radii, centers)]).reshape(20*36,3).astype(np.float32)
    colors = np.tile(colors, 36).flatten().reshape(20*36,3)
    radii = np.repeat(radii, 36).astype(np.float32)
    indexes = np.array(36, dtype=np.uint32)
    centers = np.tile(centers, 36).flatten().reshape(20*36,3)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.nbytes, indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
    gl_coords = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coords)
    GL.glVertexAttribPointer(gl_coords, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    cent_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, cent_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, centers.nbytes, centers, GL.GL_STATIC_DRAW)
    gl_cent = GL.glGetAttribLocation(program, "vert_center")
    GL.glEnableVertexAttribArray(gl_cent)
    GL.glVertexAttribPointer(gl_cent, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*centers.itemsize, ctypes.c_void_p(0))
    
    rad_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, rad_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, radii.nbytes, radii, GL.GL_STATIC_DRAW)
    gl_rads = GL.glGetAttribLocation(program, "vert_radius")
    GL.glEnableVertexAttribArray(gl_rads)
    GL.glVertexAttribPointer(gl_rads, 1, GL.GL_FLOAT, GL.GL_FALSE, radii.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coords)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glDisableVertexAttribArray(gl_cent)
    GL.glDisableVertexAttribArray(gl_rads)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vao, (ind_vbo, coord_vbo, col_vbo, cent_vbo, rad_vbo), np.uint32(coords.shape[0])

def make_cubes(program):
    """ Function doc """
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    indexes = np.array([0,1,2],dtype=np.uint32)
    coords = np.array([[ 1.0, 1.0, 1.0],[ 0.0, 0.0, 0.0],[-1.0, 1.0, 0.0]],dtype=np.float32)
    colors = np.array([[ 1.0, 0.0, 0.0],[ 0.0, 1.0, 0.0],[ 0.0, 0.0, 1.0]],dtype=np.float32)
    radii = np.array([ 0.5, 0.5, 0.1],dtype=np.float32)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.nbytes, indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
    gl_coords = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coords)
    GL.glVertexAttribPointer(gl_coords, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    rad_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, rad_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, radii.nbytes, radii, GL.GL_STATIC_DRAW)
    gl_rads = GL.glGetAttribLocation(program, "vert_radius")
    GL.glEnableVertexAttribArray(gl_rads)
    GL.glVertexAttribPointer(gl_rads, 1, GL.GL_FLOAT, GL.GL_FALSE, radii.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coords)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glDisableVertexAttribArray(gl_rads)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vao, (ind_vbo, coord_vbo, col_vbo, rad_vbo), np.uint32(coords.shape[0])

def make_impostor_cyl(program):
    """ Function doc """
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    indexes = np.array([0,1,2],dtype=np.uint32)
    coords = np.array([[-1.0,-1.0,-1.0],[-1.0, 1.0,-1.0],
                       [ 1.0,-1.0, 0.0],[ 1.0, 1.0, 0.0]],dtype=np.float32)
    colors = np.array([[ 1.0, 0.0, 0.0],[ 0.0, 1.0, 0.0],
                       [ 1.0, 1.0, 0.0],[ 0.0, 1.0, 1.0]],dtype=np.float32)
    radii = np.array([ 0.5, 0.5, 0.5, 0.5],dtype=np.float32)
    indexes = np.array([0, 1, 2, 3], dtype=np.uint32)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.nbytes, indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
    gl_coords = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coords)
    GL.glVertexAttribPointer(gl_coords, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    rad_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, rad_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, radii.nbytes, radii, GL.GL_STATIC_DRAW)
    gl_rads = GL.glGetAttribLocation(program, "vert_radius")
    GL.glEnableVertexAttribArray(gl_rads)
    GL.glVertexAttribPointer(gl_rads, 1, GL.GL_FLOAT, GL.GL_FALSE, radii.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coords)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glDisableVertexAttribArray(gl_rads)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vao, (ind_vbo, coord_vbo, col_vbo, rad_vbo), np.uint32(coords.shape[0])

def make_glumpy(program):
    """ Function doc """
    # import cartoon
    # coords = np.empty([108, 3], dtype=np.float32)
    # calphas = np.empty([27, 3], dtype=np.float32)
    # with open("test_cartoon.pdb") as pdbin:
    #     i = 0
    #     j = 0
    #     for line in pdbin:
    #         x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
    #         coords[i,:] = x, y, z
    #         i += 1
    #         if " CA " in line:
    #             calphas[j,:] = x, y, z
    #             j += 1
    # coords = cartoon.cartoon(coords, calphas, spline_detail=3)
    # radii = np.repeat(1, coords.shape[0]).astype(np.float32)
    # colors = np.tile([0, 1, 0], coords.shape[0]).reshape([coords.shape[0], 3]).astype(np.float32)
    # indexes = np.arange(coords.shape[0], dtype=np.uint32)
    coords = np.random.rand(500000,3).astype(np.float32)*500 - 250
    colors = np.random.rand(500000,3).astype(np.float32)
    radii = np.random.rand(500000).astype(np.float32)*8
    indexes = np.arange(coords.shape[0], dtype=np.uint32)
    print("coords", coords.shape)
    # print("calphas", calphas.shape)
    print("indexes", indexes.shape)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.nbytes, indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
    gl_coords = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coords)
    GL.glVertexAttribPointer(gl_coords, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    rad_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, rad_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, radii.nbytes, radii, GL.GL_STATIC_DRAW)
    gl_rads = GL.glGetAttribLocation(program, "vert_radius")
    GL.glEnableVertexAttribArray(gl_rads)
    GL.glVertexAttribPointer(gl_rads, 1, GL.GL_FLOAT, GL.GL_FALSE, radii.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coords)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glDisableVertexAttribArray(gl_rads)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vao, (ind_vbo, coord_vbo, col_vbo, rad_vbo), indexes.shape[0]

def _get_backbone(pdbfile):
    with open(pdbfile, "r") as pdbin:
        coords = []
        for line in pdbin:
            x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
            coords.append([x, y, z])
    return np.array(coords, dtype=np.float32)

def make_cartoon(program):
    import cartoon_b
    coords = []
    calphas = []
    with open("test_inha.pdb") as pdbin:
        for line in pdbin:
            x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
            coords.append([x, y, z])
            if " CA " in line:
                calphas.append([x, y, z])
    coords = np.array(coords, dtype=np.float32)
    calphas = np.array(calphas,dtype=np.float32)
    ss_seq = cartoon_b.calculate_ss(coords)
    secstruc_i = cartoon_b.get_secstruct_indexes(ss_seq)
    print(secstruc_i)
    secstruc = cartoon_b.get_secstruct_vectors(coords, secstruc_i)
    print(secstruc)
    # secstruc = [(0,0,2), (1,2,13), (0,13,16), (2,16,20,np.array([[ 0.38114753, 0.544680, -0.7470276],
    #                                                              [-0.01111542, 0.848985, -0.5283006]], dtype=np.float32)),
    #             (0,20,22), (2,22,26,np.array([[-0.32741186,-0.94466716, 0.02013549],
    #                                           [0.831728,0.5514877,0.06395128]], dtype=np.float32)), (0,26,27)]
    
    coords, norms, indexes, colors = cartoon_b.cartoon(coords, calphas, ss_assigned=secstruc,
        spline_detail=6, strand_rad=0.8, helix_rad=0.3, coil_rad=.2, spline_strength=.9)
    # indexes = np.arange(coords.shape[0], dtype=np.uint32)
    # ss = cartoon.calculate_secondary_structure(calphas)
    
    # colors = np.tile([0, 1, 0], coords.shape[0]).reshape([coords.shape[0], 3]).astype(np.float32)
    
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.nbytes, indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_color)
    GL.glVertexAttribPointer(gl_color, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    norm_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, norm_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, norms.nbytes, norms, GL.GL_STATIC_DRAW)
    gl_norm = GL.glGetAttribLocation(program, "vert_norm")
    GL.glEnableVertexAttribArray(gl_norm)
    GL.glVertexAttribPointer(gl_norm, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*norms.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_color)
    GL.glDisableVertexAttribArray(gl_norm)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, col_vbo, norm_vbo), len(indexes)

def make_texture_OGL(program):
    """ Function doc """
    from PIL import Image
    # image_a = Image.open("fonts/ArialBig.png")
    # image_a = Image.open("fonts/Jokerman.png")
    image_a = Image.open("fonts/Jokerman.png")
    ix = image_a.size[0]
    iy = image_a.size[1]
    image_a = np.array(list(image_a.getdata()),np.uint8)
    tex_texture = GL.glGenTextures(1)
    GL.glActiveTexture(GL.GL_TEXTURE0)
    GL.glBindTexture(GL.GL_TEXTURE_2D, tex_texture)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, ix, iy, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image_a)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    coords = np.zeros(3, dtype=np.float32)
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    textur = np.zeros(2, dtype=np.float32)
    tex_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, tex_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, textur.itemsize*len(textur), textur, GL.GL_STATIC_DRAW)
    gl_texture = GL.glGetAttribLocation(program, "vert_uv")
    GL.glEnableVertexAttribArray(gl_texture)
    GL.glVertexAttribPointer(gl_texture, 2, GL.GL_FLOAT, GL.GL_FALSE, 2*textur.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_texture)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return tex_texture, vao, (coord_vbo, tex_vbo)

def make_texture_coords(program):
    """ Function doc """
    coords = np.array([-1.0, 1.0, 0.0,-1.0,-1.0, 0.0, 1.0,-1.0, 0.0,
                       -1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,-1.0, 0.0,],dtype=np.float32)*2
    textur = np.array([ 0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
                        0.0, 0.0, 1.0, 0.0, 1.0, 1.0],dtype=np.float32)
    
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    tex_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, tex_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, textur.itemsize*len(textur), textur, GL.GL_STATIC_DRAW)
    gl_texture = GL.glGetAttribLocation(program, "vert_uv")
    GL.glEnableVertexAttribArray(gl_texture)
    GL.glVertexAttribPointer(gl_texture, 2, GL.GL_FLOAT, GL.GL_FALSE, 2*textur.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_texture)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, tex_vbo), int(len(coords)/3)

def fill_texture_buffers(program, vbos):
    """ Function doc """
    coords = np.array([-1.0, 1.0, 0.0,-1.0,-1.0, 0.0, 1.0,-1.0, 0.0,
                       -1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,-1.0, 0.0,],dtype=np.float32)*2
    # textur = np.array([ 0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
    #                     0.0, 0.0, 1.0, 0.0, 1.0, 1.0],dtype=np.float32)
    uvsx = 246.0/512.0
    uvex = (246.0+37.0)/512.0
    uvsy = 187.0/512.0
    uvey = (187.0+56.0)/512.0
    textur = np.array([ uvsx, uvsy, uvsx, uvey, uvex, uvey,
                        uvsx, uvsy, uvex, uvsy, uvex, uvey],dtype=np.float32)
    
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbos[0])
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
    
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbos[1])
    GL.glBufferData(GL.GL_ARRAY_BUFFER, textur.nbytes, textur, GL.GL_STATIC_DRAW)

def make_instances(program):
    coords, indexes, colors = sphd.get_sphere([1,1,1], 1.0, [0, 1, 0], level="level_1")
    radii = np.ones(1, dtype=np.float32)
    instances = np.zeros(3,dtype=np.float32)
    coords = coords.reshape(42,3)
    # print(coords.shape)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.nbytes, indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    GL.glVertexAttribDivisor(gl_colors, 1)
    
    rad_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, rad_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, radii.nbytes, radii, GL.GL_STATIC_DRAW)
    gl_rads = GL.glGetAttribLocation(program, "vert_radius")
    GL.glEnableVertexAttribArray(gl_rads)
    GL.glVertexAttribPointer(gl_rads, 1, GL.GL_FLOAT, GL.GL_FALSE, radii.itemsize, ctypes.c_void_p(0))
    GL.glVertexAttribDivisor(gl_rads, 1)
    
    insta_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, insta_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, instances.nbytes, instances, GL.GL_STATIC_DRAW)
    gl_insta = GL.glGetAttribLocation(program, "vert_instance")
    GL.glEnableVertexAttribArray(gl_insta)
    GL.glVertexAttribPointer(gl_insta, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, ctypes.c_void_p(0))
    GL.glVertexAttribDivisor(gl_insta, 1)
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glDisableVertexAttribArray(gl_rads)
    GL.glDisableVertexAttribArray(gl_insta)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    
    return vao, (coord_vbo, col_vbo, rad_vbo, insta_vbo), int(len(indexes))

def make_billboard(program):
    indexes = np.array([0,1,2],dtype=np.uint32)
    coords = np.array([[ 0.0, 1.0, 1.0],[-1.0, 0.0, 0.0],[ 0.0,-1.0,-1.0]],dtype=np.float32)
    colors = np.array([[ 1.0, 0.0, 0.0],[ 0.0, 1.0, 0.0],[ 0.0, 0.0, 1.0]],dtype=np.float32)
    radii = np.array([ 0.5, 0.8, 1.0],dtype=np.float32)
    
    coords = np.random.rand(500000,3).astype(np.float32) * 500 - 250
    colors = np.random.rand(500000,3).astype(np.float32)
    radii = np.random.rand(500000).astype(np.float32) + .5
    indexes = np.arange(coords.shape[0], dtype=np.uint32)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.nbytes, indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
    gl_coords = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coords)
    GL.glVertexAttribPointer(gl_coords, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    rad_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, rad_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, radii.nbytes, radii, GL.GL_STATIC_DRAW)
    gl_rads = GL.glGetAttribLocation(program, "vert_radius")
    GL.glEnableVertexAttribArray(gl_rads)
    GL.glVertexAttribPointer(gl_rads, 1, GL.GL_FLOAT, GL.GL_FALSE, radii.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coords)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glDisableVertexAttribArray(gl_rads)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vao, (ind_vbo, coord_vbo, col_vbo, rad_vbo), np.uint32(coords.shape[0])

def make_simple(program):
    a, b = 1, -1
    cube_coords = np.array([[a,a,a], [a,a,b], [a,b,b], [a,a,a], [a,b,b], [a,b,a],
                            [b,a,a], [a,a,a], [a,b,a], [b,a,a], [a,b,a], [b,b,a],
                            [b,a,b], [b,a,a], [b,b,a], [b,a,b], [b,b,a], [b,b,b],
                            [a,a,b], [b,a,b], [b,b,b], [a,a,b], [b,b,b], [a,b,b],
                            [b,a,b], [a,a,b], [a,a,a], [b,a,b], [a,a,a], [b,a,a],
                            [b,b,a], [a,b,a], [a,b,b], [b,b,a], [a,b,b], [b,b,b]], dtype=np.float32)
    cube_normals = np.array([[a,0,0], [a,0,0], [a,0,0], [a,0,0], [a,0,0], [a,0,0],
                             [0,0,a], [0,0,a], [0,0,a], [0,0,a], [0,0,a], [0,0,a],
                             [b,0,0], [b,0,0], [b,0,0], [b,0,0], [b,0,0], [b,0,0],
                             [0,0,b], [0,0,b], [0,0,b], [0,0,b], [0,0,b], [0,0,b],
                             [0,a,0], [0,a,0], [0,a,0], [0,a,0], [0,a,0], [0,a,0],
                             [0,b,0], [0,b,0], [0,b,0], [0,b,0], [0,b,0], [0,b,0]], dtype=np.float32)
    centers = np.array([[0,0,0], [2,2,0], [-2,0,1]], dtype=np.float32)
    cols = np.array([[1,0,0], [0,1,0], [0,0,1]])
    coords = np.array([cube_coords + c for c in centers]).reshape(centers.shape[0]*cube_coords.shape[0], 3).astype(np.float32)
    normals = np.array([cube_normals + 0 for c in centers]).reshape(centers.shape[0]*cube_coords.shape[0], 3).astype(np.float32)
    colors = np.tile(cols, 36).reshape(centers.shape[0]*cube_coords.shape[0], 3).astype(np.float32)
    indexes = np.arange(coords.shape[0], dtype=np.uint32)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.nbytes, indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
    gl_coords = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coords)
    GL.glVertexAttribPointer(gl_coords, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    norm_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, norm_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, normals.nbytes, normals, GL.GL_STATIC_DRAW)
    gl_norms = GL.glGetAttribLocation(program, "vert_norm")
    GL.glEnableVertexAttribArray(gl_norms)
    GL.glVertexAttribPointer(gl_norms, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*normals.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coords)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glDisableVertexAttribArray(gl_norms)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vao, (ind_vbo, coord_vbo, col_vbo, norm_vbo), indexes.shape[0]

def make_ribbon(program):
    import cartoon_b
    calphas = np.array([[ 7.565, 1.393,-3.330],[ 5.905, 4.313,-1.470],[ 3.905, 3.338, 1.657],
                        [ 1.472, 6.312, 1.565],[ 0.839, 5.844,-2.192],[ 0.727, 2.024,-1.853],
                        [-1.685, 2.311, 1.122],[-3.948, 4.672,-0.892],[-4.162, 2.074,-3.715],
                        [-5.005,-0.679,-1.180],[-7.378, 1.658, 0.729],[-9.450, 2.165,-2.471],
                        [-9.829,-1.650,-2.627],[-10.50,-1.769, 1.154],[-7.272,-3.432, 2.410],
                        [-3.968,-2.547, 4.132],[-1.080,-1.652, 1.768],[ 2.411,-3.047, 2.493],
                        [ 5.501,-2.266, 0.369],[ 7.915,-5.193,-0.169],[11.235,-3.905,-1.592],
                        [ 9.890,-1.961,-4.606],[ 6.470,-3.689,-5.031],[ 3.119,-2.524,-3.570],
                        [ 0.715,-5.246,-2.334],[-2.541,-5.227,-0.302],[-3.079,-7.540, 2.715]], dtype=np.float32)
    sd = 5
    coords, rib_inds = cartoon_b.ribbon(calphas, spline_detail=sd)
    rib_cols = cartoon_b.get_rainbow_colors(calphas.shape[0])
    colors = np.empty(coords.shape, dtype=np.float32)
    pos = 0
    for i, ri in enumerate(rib_inds):
        colors[pos:pos+len(ri),:] = np.tile(rib_cols[i], len(ri)).reshape(len(ri), 3)
        pos += len(ri)
    indexes = np.arange(coords.shape[0], dtype=np.uint32)
    # indexes = []
    # for i in range(coords.shape[0]-1):
    #     indexes.append(i)
    #     indexes.append(i+1)
    # indexes = np.array(indexes, dtype=np.uint32)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.nbytes, indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
    gl_coords = GL.glGetAttribLocation(program, "vert_coord")
    GL.glEnableVertexAttribArray(gl_coords)
    GL.glVertexAttribPointer(gl_coords, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, "vert_color")
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coords)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vao, (ind_vbo, coord_vbo, col_vbo), indexes.shape[0]
