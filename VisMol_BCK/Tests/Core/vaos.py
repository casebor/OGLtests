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

def cubic_hermite_interpolate(p_k1, tan_k1, p_k2, tan_k2, t):
    p = np.zeros(3, dtype=np.float32)
    tt = t * t
    tmt_t = 3.0 - 2.0 * t
    h01 = tt * tmt_t
    h00 = 1.0 - h01
    h10 = tt * (t - 2.0) + t
    h11 = tt * (t - 1.0)
    p[:] = p_k1[:]
    p*= h00
    p += tan_k1 * h10
    p += p_k2 * h01
    p += tan_k2 * h11
    return p

def catmull_rom_spline(points, num_points, subdivs, strength=0.5, circular=False):
    if circular:
        out_len = num_points * subdivs
    else:
        out_len = (num_points - 1) * subdivs + 1
    out = np.zeros([out_len, 3], dtype=np.float32)
    index = 0
    dt = 1.0 / subdivs
    tan_k1 = np.zeros(3, dtype=np.float32)
    tan_k2 = np.zeros(3, dtype=np.float32)
    p_k1 = np.zeros(3, dtype=np.float32)
    p_k2 = np.zeros(3, dtype=np.float32)
    p_k3 = np.zeros(3, dtype=np.float32)
    p_k4 = np.zeros(3, dtype=np.float32)
    p_k2[:] = points[0,:]
    p_k3[:] = points[1,:]
    if circular:
        p_k1[:] = points[-1,:]
        tan_k1[:] = p_k3 - p_k1
        tan_k1 *= strength
    else:
        p_k1[:] = points[0,:]
    i = 1
    e = num_points - 1
    while i < e:
        p_k4[:] = points[i+1,:]
        tan_k2[:] = p_k4 - p_k2
        tan_k2 *= strength
        for j in range(subdivs):
            out[index,:] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
            index += 1
        p_k1[:] = p_k2[:]
        p_k2[:] = p_k3[:]
        p_k3[:] = p_k4[:]
        tan_k1[:] = tan_k2[:]
        i += 1
    if circular:
        p_k4[0] = points[0,0]
        p_k4[1] = points[0,1]
        p_k4[2] = points[1,0]
        tan_k1 = p_k4 - p_k2
        tan_k1 *= strength
    else:
        tan_k1 = np.zeros(3, dtype=np.float32)
    for j in range(subdivs):
        out[index] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
        index += 1
    if not circular:
        out[index] = points[num_points-1:num_points]
        return out
    p_k1[:] = p_k2[:]
    p_k2[:] = p_k3[:]
    p_k3[:] = p_k4[:]
    tan_k1[:] = tan_k2[:]
    p_k4[:] = points[1,:]
    tan_k1 = p_k4 - p_k2
    tan_k1 *= strength
    for j in range(subdivs):
        out[index] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
        index += 1
    return out

def _get_normal(vec1, vec2):
    """ Function doc """
    return (vec1 + vec2) / np.linalg.norm(vec1 + vec2)

def make_capsules(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    coords = np.array([-1.0, 1.0, 0.0, 1.0, 1.0, 0.0,
                       -1.0, 1.0, 0.0,-1.0,-1.0, 0.0,
                       -1.0,-1.0, 0.0, 1.0,-1.0, 0.0],dtype=np.float32)
    colors = np.array([ 1.0, 0.0, 0.0, 0.0, 0.0, 1.0,
                        0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
                        1.0, 1.0, 0.0, 1.0, 0.0, 1.0],dtype=np.float32)
    indexes = np.array([0, 1, 2, 3, 4, 5], dtype=np.uint32)
    
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

def make_dots(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    import cartoon as cton
    coords = cton.cartoon()[0]
    colors = [1.0,0.0,0.0] * coords.shape[0]
    colors = np.array(colors, dtype=np.float32)
    colors = colors.flatten()
    coords = coords.flatten()
    
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
    return vertex_array_object, (coord_vbo, col_vbo), coords.shape[0]//3

def make_dots_bck(program):
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
    return vertex_array_object, (coord_vbo, col_vbo), int(len(coords)/3)

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
        verts, inds, cols = sphd.get_sphere(center, 1.1, [0, 1, 0], level='level_2')
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

def make_sphere(program, level='level_2'):
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
    return vertex_array_object, (ind_vbo, coord_vbo, col_vbo), int(len(indexes))

def interpolate_points(p1, p2, p3, p4, s=0.25, pieces=7):
    cmr_mat = np.array([[  -s, 2-s,   s-2,   s],
                        [ 2*s, s-3, 3-2*s,  -s],
                        [  -s, 0.0,     s, 0.0],
                        [ 0.0, 1.0,   0.0, 0.0]], dtype=np.float32)
    parts = np.linspace(0, 1, pieces)
    calphas = np.array([p1, p2, p3, p4], dtype=np.float32)
    coords = np.zeros([pieces, 3], dtype=np.float32)
    mat = np.matmul(cmr_mat, calphas)
    for i, p in enumerate(parts):
        v = np.array([p**3, p**2, p, 1])
        coords[i,:] = np.matmul(v, mat)
    return np.copy(coords[:-1])

def build_spline(calphas, s=0.25, pieces=7):
    ns = (len(calphas)-3) * (pieces-1) + 3
    new_coords = np.zeros([ns,3], dtype=np.float32)
    new_coords[0,:] = calphas[0,:]
    r = 1
    for i in range(0, calphas.shape[0]-3):
        _crds = interpolate_points(calphas[i], calphas[i+1], calphas[i+2],
                                   calphas[i+3], s=s, pieces=pieces)
        for j in range(_crds.shape[0]):
            new_coords[r,:] = _crds[j,:]
            r += 1
    new_coords[-2:,:] = calphas[-2:,:]
    return new_coords

def get_rotmat(angle, dir_vec):
    # vector = np.array(dir_vec, dtype=np.float32)
    assert(np.linalg.norm(dir_vec)>0.0)
    # angle = angle*np.pi/180.0
    # x, y, z = vector/np.linalg.norm(vector)
    x, y, z = dir_vec
    c = np.cos(angle)
    s = np.sin(angle)
    rot_matrix = np.identity(4, dtype=np.float32)
    rot_matrix[0,0] = x*x*(1-c)+c
    rot_matrix[1,0] = y*x*(1-c)+z*s
    rot_matrix[2,0] = x*z*(1-c)-y*s
    rot_matrix[0,1] = x*y*(1-c)-z*s
    rot_matrix[1,1] = y*y*(1-c)+c
    rot_matrix[2,1] = y*z*(1-c)+x*s
    rot_matrix[0,2] = x*z*(1-c)+y*s
    rot_matrix[1,2] = y*z*(1-c)-x*s
    rot_matrix[2,2] = z*z*(1-c)+c
    return rot_matrix

def cartoon(p1, p2, flag=False):
    ellipse = np.array([[[-2.0, 0.00, 0], [-1.6, 0.60, 0], [-1.2, 0.800, 0], [-0.8, 0.917, 0],
                         [-0.4, 0.98, 0], [ 0.0, 1.00, 0], [ 0.4, 0.980, 0], [ 0.8, 0.917, 0],
                         [ 1.2, 0.80, 0], [ 1.6, 0.60, 0], [ 2.0, 0.000, 0],
                         [ 1.6,-0.60, 0], [ 1.2,-0.80, 0], [ 0.8,-0.917, 0], [ 0.4,-0.980, 0],
                         [ 0.0,-1.00, 0], [-0.4,-0.98, 0], [-0.8,-0.917, 0], [-1.2,-0.800, 0],
                         [-1.6,-0.60, 0]],
                        [[-1.8, 0.436, 0], [-1.4, 0.714, 0], [-1.0, 0.866, 0], [-0.6, 0.954, 0],
                         [-0.2, 0.995, 0], [ 0.2, 0.995, 0], [ 0.6, 0.954, 0], [ 1.0, 0.866, 0],
                         [ 1.4, 0.714, 0], [ 1.8, 0.436, 0],
                         [ 1.8,-0.436, 0], [ 1.4,-0.714, 0], [ 1.0,-0.866, 0], [ 0.6,-0.954, 0],
                         [ 0.2,-0.995, 0], [-0.2,-0.995, 0], [-0.6,-0.954, 0], [-1.0,-0.866, 0],
                         [-1.4,-0.714, 0], [-1.8,-0.436, 0]]
        ])
    circle = np.array([[[ 1.000000000000, 0.000000000000, 0.0],
                        [ 0.866025403784,-0.500000000000, 0.0],
                        [ 0.500000000000,-0.866025403784, 0.0],
                        [-0.000000000000,-1.000000000000, 0.0],
                        [-0.500000000000,-0.866025403784, 0.0],
                        [-0.866025403784,-0.500000000000, 0.0],
                        [-1.000000000000, 0.000000000000, 0.0],
                        [-0.866025403784, 0.500000000000, 0.0],
                        [-0.500000000000, 0.866025403784, 0.0],
                        [ 0.000000000000, 1.000000000000, 0.0],
                        [ 0.500000000000, 0.866025403784, 0.0],
                        [ 0.866025403784, 0.500000000000, 0.0]],
                       [[ 0.965925826289,-0.258819045103, 0.0],
                        [ 0.707106781187,-0.707106781187, 0.0],
                        [ 0.258819045103,-0.965925826289, 0.0],
                        [-0.258819045103,-0.965925826289, 0.0],
                        [-0.707106781187,-0.707106781187, 0.0],
                        [-0.965925826289,-0.258819045103, 0.0],
                        [-0.965925826289, 0.258819045103, 0.0],
                        [-0.707106781187, 0.707106781187, 0.0],
                        [-0.258819045103, 0.965925826289, 0.0],
                        [ 0.258819045103, 0.965925826289, 0.0],
                        [ 0.707106781187, 0.707106781187, 0.0],
                        [ 0.965925826289, 0.258819045103, 0.0]]],dtype=np.float32)/2
    # indexes = np.arange(40, dtype=np.uint32)
    vec = p2 - p1
    vec /= np.linalg.norm(vec)
    normal = np.cross([0,0,1], vec)
    normal /= np.linalg.norm(normal)
    angle = np.arccos(np.dot([0,0,1], vec))
    rotmat = get_rotmat(angle, normal)[:3,:3]
    
    disc = np.zeros([circle[int(flag)].shape[0], 3], dtype=np.float32)
    for i, e in enumerate(circle[int(flag)]):
        disc[i,:] = np.matmul(rotmat, e)
    normals = disc - p2
    mods = np.linalg.norm(normals, axis=1)
    for i in range(normals.shape[0]):
        normals[i,:] /= mods[i]
    disc += p2

    return disc, normals
    # # Build the base
    # base = np.zeros([20,3], dtype=np.float32)
    # # for i, e in enumerate(ellipse[0]):
    # for i, e in enumerate(circle[0]):
    #     base[i,:] = np.matmul(rotmat, e)
    # base += p1
    
    # # Build the top
    # top = np.zeros([20,3], dtype=np.float32)
    # # for i, e in enumerate(ellipse[1]):
    # for i, e in enumerate(circle[1]):
    #     top[i,:] = np.matmul(rotmat, e)
    # top += p2
    
    # # Join base and top
    # joined = np.zeros([40,3], dtype=np.float32)
    # for i, b, t in zip(np.arange(20), base, top):
    #     joined[i*2,:] = b
    #     joined[i*2+1,:] = t
    # return joined, indexes

def get_indexes(num_points, pts_per_ring):
    num_rings = num_points // pts_per_ring
    indexes = []
    for i in range(num_rings-1):
        for j in range(pts_per_ring-1):
            indexes.extend([i*pts_per_ring+j, i*pts_per_ring+j+1, (i+1)*pts_per_ring+j])
        indexes.extend([(i+1)*pts_per_ring-j, i*pts_per_ring, (i+2)*pts_per_ring-1])
        for j in range(pts_per_ring-1):
            indexes.extend([(i+1)*pts_per_ring+j, i*pts_per_ring+j+1, (i+1)*pts_per_ring+j+1])
        indexes.extend([(i+2)*pts_per_ring-1, i*pts_per_ring, (i+1)*pts_per_ring])
    return indexes

def get_indexes2(num_points, pts_per_ring):
    num_rings = num_points // pts_per_ring
    a = np.array([[ 0,  1, 12,  1,  2, 13,  2,  3, 14,  3,  4, 15,
                    4,  5, 16,  5,  6, 17,  6,  7, 18,  7,  8, 19,
                    8,  9, 20,  9, 10, 21, 10, 11, 22, 11,  0, 23,
                   12, 13,  1, 13, 14,  2, 14, 15,  3, 15, 16,  4,
                   16, 17,  5, 17, 18,  6, 18, 19,  7, 19, 20,  8,
                   20, 21,  9, 21, 22, 10, 22, 23, 11, 23, 12, 11],
                  [ 0,  1, 13,  1,  2, 14,  2,  3, 15,  3,  4, 16,
                    4,  5, 17,  5,  6, 18,  6,  7, 19,  7,  8, 20,
                    8,  9, 21,  9, 10, 22, 10, 11, 23, 11,  0, 12,
                   12, 13,  0, 13, 14,  1, 14, 15,  2, 15, 16,  3,
                   16, 17,  4, 17, 18,  5, 18, 19,  6, 19, 20,  7,
                   20, 21,  8, 21, 22,  9, 22, 23, 10, 23, 12, 11]], dtype=np.uint32)
    indexes = np.array([], dtype=np.uint32)
    flag = False
    for i in range(num_rings - 1):
        indexes = np.hstack((indexes, a[int(flag)]+i*pts_per_ring))
        flag = not flag
    return indexes

def make_cartoon(program):
    """ Function doc """
    
    import cartoon as cton
    coords, normals, indexes, colors = cton.cartoon()
    # colors = [0.0, 1.0, 0.0] * coords.shape[0]
    # print(coords.shape, len(colors), normals.shape, indexes.shape)
    # print(indexes.reshape((60,3)))
    # np.savetxt("inds.txt", indexes.reshape((2016,3)))
    coords = coords.flatten()
    normals = normals.flatten()
    colors = colors.flatten()
    # colors = np.array(colors, dtype=np.float32)
    # print(coords.shape, colors.shape, normals.shape, indexes.shape)
    
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*len(indexes), indexes, GL.GL_DYNAMIC_DRAW)
    
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
    GL.glBufferData(GL.GL_ARRAY_BUFFER, normals.itemsize*len(normals), normals, GL.GL_STATIC_DRAW)
    gl_norm = GL.glGetAttribLocation(program, 'vert_norm')
    GL.glEnableVertexAttribArray(gl_norm)
    GL.glVertexAttribPointer(gl_norm, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*normals.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_color)
    GL.glDisableVertexAttribArray(gl_norm)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, col_vbo, norm_vbo), indexes.shape[0]

def make_test(program):
    """ Function doc """
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    coords = np.array([ 1.0, 1.0, 0.0,-1.0,-1.0, 0.0, 0.0, 0.0, 0.0],dtype=np.float32)
    colors = np.array([ 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0],dtype=np.float32)
    coords = np.array([ 1.0, 1.0, 0.0],dtype=np.float32)
    colors = np.array([ 1.0, 0.0, 0.0],dtype=np.float32)


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
    return vertex_array_object, (coord_vbo, col_vbo), int(len(coords)/3)

def make_bonds_impostor(program):
    """ Function doc """
    n, p = -1, 1
    cube = [n, n, n,  n, n, p,  n, p, p,  n, n, n,  n, p, p,  n, p, n, # -X
            p, n, p,  p, n, n,  p, p, n,  p, n, p,  p, p, n,  p, p, p, # +X
            n, n, n,  p, n, n,  p, n, p,  n, n, n,  p, n, p,  n, n, p, # -Y
            n, p, p,  p, p, p,  p, p, n,  n, p, p,  p, p, n,  n, p, n, # +Y
            p, n, n,  n, n, n,  n, p, n,  p, n, n,  n, p, n,  p, p, n, # -Z
            n, n, p,  p, n, p,  p, p, p,  n, n, p,  p, p, p,  n, p, p] # +Z
    cubes = np.array(cube*9, dtype=np.float32).flatten()
    points = [[ 1.0, 1.0, 0.5], [ 0.0, 1.0, -0.5], [ 1.0, 0.0, 0.0],
              [-1.0, 0.0, 0.5], [-1.0, 1.0, -0.5], [-1.0,-1.0, 0.0],
              [ 0.0,-1.0, 0.5], [ 1.0,-1.0, -0.5], [ 0.0, 0.0, 0.0]]
    # points = [[ 1.0, 1.0, 0.0]]
    coords = [p*36 for p in points]
    coords = np.array(coords, dtype=np.float32).flatten()
    col_pt = [[ 1.0, 0.0, 0.0], [ 1.0, 1.0, 0.0], [ 1.0, 0.0, 1.0],
              [ 0.0, 0.0, 1.0], [ 0.0, 1.0, 0.0], [ 0.0, 1.0, 1.0],
              [ 0.0, 1.0, 0.0], [ 0.0, 1.0, 0.0], [ 0.0, 1.0, 0.0]]
    # col_pt = [[ 1.0, 0.0, 0.0]]
    colors = [c*36 for c in col_pt]
    colors = np.array(colors, dtype=np.float32).flatten()
    # coords = coords[:216]
    # colors = colors[:216]
    # cubes = cubes[:216]
    # print(cubes.shape, coords.shape, colors.shape)

    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    cube_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, cube_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, cubes.itemsize*len(cubes), cubes, GL.GL_STATIC_DRAW)
    gl_cube = GL.glGetAttribLocation(program, 'cube_coord')
    GL.glEnableVertexAttribArray(gl_cube)
    GL.glVertexAttribPointer(gl_cube, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*cubes.itemsize, ctypes.c_void_p(0))
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(gl_position)
    GL.glVertexAttribPointer(gl_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_cube)
    GL.glDisableVertexAttribArray(gl_position)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, col_vbo), int(len(coords)/3)

def make_impostor(program):
    """ Function doc """
    points = [[ 1.0, 1.0, 0.5], [ 0.0, 1.0, -0.5], [ 1.0, 0.0, 0.0],
              [-1.0, 0.0, 0.5], [-1.0, 1.0, -0.5], [-1.0,-1.0, 0.0],
              [ 0.0,-1.0, 0.5], [ 1.0,-1.0, -0.5], [ 0.0, 0.0, 0.0]]
    coords = np.array(points, dtype=np.float32).flatten()
    col_pt = [[ 1.0, 0.0, 0.0], [ 1.0, 1.0, 0.0], [ 1.0, 0.0, 1.0],
              [ 0.0, 0.0, 1.0], [ 0.0, 1.0, 0.0], [ 0.0, 1.0, 1.0],
              [ 0.0, 1.0, 0.0], [ 0.0, 1.0, 0.0], [ 0.0, 1.0, 0.0]]
    colors = np.array(col_pt, dtype=np.float32).flatten()
    radii = np.array([1.2, 1.0, 0.8, 0.2, 1.0, 0.4, 0.8, 1.1, 0.7], dtype=np.float32)
    # coords = coords[:216]
    # colors = colors[:216]
    # cubes = cubes[:216]
    # print(coords.shape, colors.shape)
    
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(gl_position)
    GL.glVertexAttribPointer(gl_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    rad_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, rad_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, radii.itemsize*len(radii), radii, GL.GL_STATIC_DRAW)
    gl_radius = GL.glGetAttribLocation(program, 'vert_rad')
    GL.glEnableVertexAttribArray(gl_radius)
    GL.glVertexAttribPointer(gl_radius, 1, GL.GL_FLOAT, GL.GL_FALSE, 1*radii.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_position)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glDisableVertexAttribArray(gl_radius)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, col_vbo, rad_vbo), int(len(coords)/3)