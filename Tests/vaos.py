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
import sphere_data as spd

from OpenGL import GL

def _get_normal(vec1, vec2):
    """ Function doc """
    return (vec1 + vec2) / np.linalg.norm(vec1 + vec2)

def make_dots(program):
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
    position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, 'vert_color')
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
    position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(position)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, col_vbo), int(len(coords))

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
    position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(position)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, col_vbo), int(len(coords))

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
    position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, 'vert_color')
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
    position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, 'vert_color')
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
    position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(position)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (ind_vbo, coord_vbo, col_vbo), int(len(coords))

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
    gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(gl_color)
    GL.glVertexAttribPointer(gl_color, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    rad_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, rad_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, radios.itemsize*len(radios), radios, GL.GL_STATIC_DRAW)
    gl_rad = GL.glGetAttribLocation(program, 'vert_rad')
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
    gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, 'vert_color')
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
    gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, 'vert_color')
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
    gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(gl_color)
    GL.glVertexAttribPointer(gl_color, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    norm_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, norm_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, norms.itemsize*len(norms), norms, GL.GL_STATIC_DRAW)
    gl_norm = GL.glGetAttribLocation(program, 'vert_norm')
    GL.glEnableVertexAttribArray(gl_norm)
    GL.glVertexAttribPointer(gl_norm, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*norms.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_color)
    GL.glDisableVertexAttribArray(gl_norm)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, col_vbo, norm_vbo), int(len(coords))

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
    position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(position)
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, 'vert_color')
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
        verts, inds, cols = spd.get_sphere(center, 1.1, [0, 1, 0], level='level_2')
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
    gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    centr_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, centr_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, centers.itemsize*len(centers), centers, GL.GL_STATIC_DRAW)
    gl_center = GL.glGetAttribLocation(program, 'vert_centr')
    GL.glEnableVertexAttribArray(gl_center)
    GL.glVertexAttribPointer(gl_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*centers.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, 'vert_color')
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
    #print('opened file: size=', image_a.size, 'format=', image_a.format)
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
    gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    tex_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, tex_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, text_id.itemsize*len(text_id), text_id, GL.GL_STATIC_DRAW)
    gl_texture = GL.glGetAttribLocation(program, 'vert_id')
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
    #print('opened file: size=', image_a.size, 'format=', image_a.format)
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
    textur = np.array([ 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                        0.0, 1.0, 1.0, 1.0, 1.0, 0.0],dtype=np.float32)
    
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    tex_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, tex_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, textur.itemsize*len(textur), textur, GL.GL_STATIC_DRAW)
    gl_texture = GL.glGetAttribLocation(program, 'vert_text')
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
    gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, 'vert_color')
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
    gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_color = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(gl_color)
    GL.glVertexAttribPointer(gl_color, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_color)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (ind_vbo, coord_vbo, col_vbo), int(len(indexes))
