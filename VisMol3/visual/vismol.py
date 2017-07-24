#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  VisMol.py
#  
#  Copyright 2016 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
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

import math
import numpy as np
import ctypes
import visual.glcamera as cam
import visual.matrix_operations as mop
import visual.shapes as shapes
import visual.sphere_data as sph_d

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import OpenGL
from OpenGL import GLU
from OpenGL import GL
from OpenGL.GL import shaders

class MyGLProgram(Gtk.GLArea):
    """ Object that contains the GLArea from GTK3+.
        It needs a vertex and shader to be created, maybe later I'll
        add a function to change the shaders.
    """
    
    def __init__(self, data=None, width=640, height=420):
        """ Constructor of the class, needs two String objects,
            the vertex and fragment shaders.
            
            Keyword arguments:
            vertex -- The vertex shader to be used (REQUIRED)
            fragment -- The fragment shader to be used (REQUIRED)
            
            Returns:
            A MyGLProgram object.
        """
        super(MyGLProgram, self).__init__()
        self.connect("realize", self.initialize)
        self.connect("render", self.render)
        self.connect("resize", self.reshape)
        self.connect("key-press-event", self.key_press)
        self.connect("button-press-event", self.mouse_pressed)
        self.connect("button-release-event", self.mouse_released)
        self.connect("motion-notify-event", self.mouse_motion)
        self.connect("scroll-event", self.mouse_scroll)
        #self.set_size_request(width, height)
        self.grab_focus()
        self.set_events( self.get_events() | Gdk.EventMask.SCROLL_MASK
                       | Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK
                       | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.POINTER_MOTION_HINT_MASK
                       | Gdk.EventMask.KEY_PRESS_MASK | Gdk.EventMask.KEY_RELEASE_MASK )
        self.data = data
        
    def initialize(self, widget):
        """ Enables the buffers and other charasteristics of the OpenGL context.
            sets the initial projection and view matrix
            
            self.flag -- Needed to only create one OpenGL program, otherwise a bunch of
                         programs will be created and use system resources. If the OpenGL
                         program will be changed change this value to True
        """
        if self.get_error()!=None:
            print(self.get_error().args)
            print(self.get_error().code)
            print(self.get_error().domain)
            print(self.get_error().message)
            Gtk.main_quit()
        self.model_mat = np.identity(4, dtype=np.float32)
        self.normal_mat = np.identity(3, dtype=np.float32)
        self.glcamera = cam.GLCamera()
        self.set_has_depth_buffer(True)
        self.set_has_alpha(True)
        self.frame_i = 0
        aloc = self.get_allocation()
        w = np.float32(aloc.width)
        h = np.float32(aloc.height)
        self.shader_flag = True
        self.modified_data = False
        self.scroll = 0.3
        self.glcamera.field_of_view = 25.0
        self.glcamera.z_near = 0.1
        self.glcamera.z_far = 15
        self.glcamera.viewport_aspect_ratio = float(w)/h
        self.right = float(w)/h
        self.left = -self.right
        self.top = 1
        self.bottom = -1
        self.mouse_x = self.mouse_y = 0
        self.mouse_rotate = self.mouse_zoom = self.mouse_pan = False
        self.bckgrnd_color = np.array([0.0,0.0,0.0,1.0],dtype=np.float32)
        #self.bckgrnd_color = np.array([1.0,1.0,1.0,1.0],dtype=np.float32)
        self.light_position = np.array([2.5,2.5,3.0],dtype=np.float32)
        self.light_color = np.array([1.0,1.0,1.0,1.0],dtype=np.float32)
        self.light_ambient_coef = 0.5
        self.light_shininess = 5.5
        self.light_intensity = np.array([0.6,0.6,0.6],dtype=np.float32)
        self.light_specular_color = np.array([1.0,1.0,1.0],dtype=np.float32)
        self.LINES = False
        self.SPHERES = False
        self.DOTS = False
        self.DOTS_SURFACE = False
        self.VDW = False
        self.CRYSTAL = False
        self.RIBBON = False
        self.BALL_STICK = False
        self.create_vaos()
        self.zero_pt_ref = np.array([0.0, 0.0, 0.0],dtype=np.float32)
    
    def reshape(self, widget, width, height):
        """ Resizing function, takes the widht and height of the widget
            and modifies the view in the camera acording to the new values
        
            Keyword arguments:
            widget -- The widget that is performing resizing
            width -- Actual width of the window
            height -- Actual height of the window
        """
        self.left = -float(width)/height
        self.right = -self.left
        self.width = width
        self.height = height
        self.center_x = width/2
        self.center_y = height/2
        print(width)
        print(height)
        self.glcamera.viewport_aspect_ratio = float(width)/height
        self.queue_draw()
        return True
    
    def create_gl_programs(self):
        """ Function doc
        """
        import visual.vismol_shaders as vm_shader
        self.sphere_program = self.load_shaders(vm_shader.vertex_shader_sphere, vm_shader.fragment_shader_sphere)
        self.ribbon_program = self.load_shaders(vm_shader.vertex_shader_sphere, vm_shader.fragment_shader_sphere)
        self.ball_stick_program = self.load_shaders(vm_shader.vertex_shader_sphere, vm_shader.fragment_shader_sphere)
        self.crystal_program = self.load_shaders(vm_shader.vertex_shader_crystal, vm_shader.fragment_shader_crystal)
        self.dot_surface_program = self.load_shaders(vm_shader.vertex_shader_dot_surface, vm_shader.fragment_shader_dot_surface)
        self.dots_program = self.load_shaders(vm_shader.vertex_shader_dots, vm_shader.fragment_shader_dots)
        self.lines_program = self.load_shaders(vm_shader.vertex_shader_lines, vm_shader.fragment_shader_lines)
    
    def create_vaos(self):
        """ Function doc
        """
        # Ball-Stick representation
        self.ball_stick_vao = []
        self.bond_stick_vao = []
        # Ribbon representation
        self.ribbons_vao = []
        # Covalent radius representation
        self.spheres_vao = []
        # Dots representation
        self.dots_surf_vao = []
        # Dotted surface representation
        self.dots_vao = []
        # Lines representation
        self.lines_vao = []
        # Van der Waals representation
        self.vdw_vao = []
        # Transparent Representataion
        self.inner_cryst_vao = []
        self.bond_cryst_vao = []
        self.outer_cryst_vao = []
    
    def load_shaders(self, vertex, fragment):
        """ Here the shaders are loaded and compiled to an OpenGL program. By default
            the constructor shaders will be used, if you want to change the shaders
            use this function. The flag is used to create only one OpenGL program.
            
            Keyword arguments:
            vertex -- The vertex shader to be used
            fragment -- The fragment shader to be used
        """
        my_vertex_shader = self.create_shader(vertex, GL.GL_VERTEX_SHADER)
        my_fragment_shader = self.create_shader(fragment, GL.GL_FRAGMENT_SHADER)
        program = GL.glCreateProgram()
        GL.glAttachShader(program, my_vertex_shader)
        GL.glAttachShader(program, my_fragment_shader)
        GL.glLinkProgram(program)
        #print 'OpenGL version: ',GL.glGetString(GL.GL_VERSION)
        #try:
            #print 'OpenGL major version: ',GL.glGetDoublev(GL.GL_MAJOR_VERSION)
            #print 'OpenGL minor version: ',GL.glGetDoublev(GL.GL_MINOR_VERSION)
        #except:
            #print 'OpenGL major version not found'
        return program
        
    def create_shader(self, shader_prog, shader_type):
        """ Creates, links to a source, compiles and returns a shader.
            
            Keyword arguments:
            shader -- The shader text to use
            shader_type -- The OpenGL enum type of shader, it can be:
                           GL.GL_VERTEX_SHADER, GL.GL_GEOMETRY_SHADER or GL.GL_FRAGMENT_SHADER
            
            Returns:
            A shader object identifier or pops out an error
        """
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, shader_prog)
        GL.glCompileShader(shader)
        if GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", shader_type)
            raise RuntimeError(GL.glGetShaderInfoLog(shader))
        return shader
    
    def render(self, area, context):
        """ This is the function that will be called everytime the window
            needs to be re-drawed.
        """
        if self.shader_flag:
            self.create_gl_programs()
            self.shader_flag = False
        if self.data is not None:
            if self.modified_data:
                self.delete_vaos()
                self.load_data()
            GL.glClearColor(self.bckgrnd_color[0],self.bckgrnd_color[1],
                            self.bckgrnd_color[2],self.bckgrnd_color[3])
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            
            if self.CRYSTAL:
                GL.glUseProgram(self.ball_stick_program)
                self.load_matrices(self.ball_stick_program)
                self.load_lights(self.ball_stick_program)
                self.draw_ball_stick()
                GL.glUseProgram(0)
                GL.glUseProgram(self.crystal_program)
                self.load_matrices(self.crystal_program)
                self.load_lights(self.crystal_program)
                self.draw_crystal()
                GL.glUseProgram(0)
            if self.BALL_STICK:
                GL.glUseProgram(self.ball_stick_program)
                self.load_matrices(self.ball_stick_program)
                self.load_lights(self.ball_stick_program)
                self.draw_ball_stick()
                GL.glUseProgram(0)
            if self.SPHERES:
                GL.glUseProgram(self.sphere_program)
                self.load_matrices(self.sphere_program)
                self.load_lights(self.sphere_program)
                self.draw_spheres()
                GL.glUseProgram(0)
            if self.RIBBON:
                GL.glUseProgram(self.ribbon_program)
                self.load_matrices(self.ribbon_program)
                self.load_lights(self.ribbon_program)
                self.draw_ribbons()
                GL.glUseProgram(0)
            if self.DOTS_SURFACE:
                GL.glUseProgram(self.dot_surface_program)
                self.load_matrices(self.dot_surface_program)
                self.draw_dots_surface()
                GL.glUseProgram(0)
            if self.LINES:
                GL.glUseProgram(self.lines_program)
                #GL.glLineWidth(50/self.glcamera.z_far)
                self.load_matrices(self.lines_program)
                self.load_fog(self.lines_program)
                self.draw_lines()
                GL.glUseProgram(0)
            if self.DOTS:
                GL.glUseProgram(self.dots_program)
                GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
                self.load_matrices(self.dots_program)
                self.load_dot_params(self.dots_program)
                self.draw_dots()
                GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
                GL.glUseProgram(0)
            
        else:
            GL.glClearColor(self.bckgrnd_color[0],self.bckgrnd_color[1],
                            self.bckgrnd_color[2],self.bckgrnd_color[3])
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    
    def load_matrices(self, program):
        """ Load the matrices to OpenGL.
            
            model_mat -- transformation matrix for the objects rendered
            view_mat -- transformation matrix for the camera used
            projection_mat -- matrix for the space to be visualized in the scene
        """
        model = GL.glGetUniformLocation(program, 'model_mat')
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, self.model_mat)
        view = GL.glGetUniformLocation(program, 'view_mat')
        GL.glUniformMatrix4fv(view, 1, GL.GL_FALSE, self.glcamera.get_view_matrix())
        proj = GL.glGetUniformLocation(program, 'projection_mat')
        GL.glUniformMatrix4fv(proj, 1, GL.GL_FALSE, self.glcamera.get_projection_matrix())
        norm = GL.glGetUniformLocation(program, 'normal_mat')
        GL.glUniformMatrix3fv(norm, 1, GL.GL_FALSE, self.normal_mat)
        return True
    
    def load_fog(self, program):
        """ Function doc
        """
        fog_s = GL.glGetUniformLocation(program, 'fog_start')
        GL.glUniform1fv(fog_s, 1, self.glcamera.z_far-5)
        fog_e = GL.glGetUniformLocation(program, 'fog_end')
        GL.glUniform1fv(fog_e, 1, self.glcamera.z_far)
        fog_c = GL.glGetUniformLocation(program, 'fog_color')
        GL.glUniform4fv(fog_c, 1, self.bckgrnd_color)
    
    def load_dot_params(self, program):
        """ Function doc
        """
        # Extern line
        linewidth = 2
        # Intern line
        antialias = 2
        # Dot size factor
        dot_factor = 500/self.glcamera.z_far
        uni_vext_linewidth = GL.glGetUniformLocation(program, 'vert_ext_linewidth')
        GL.glUniform1fv(uni_vext_linewidth, 1, linewidth)
        uni_vint_antialias = GL.glGetUniformLocation(program, 'vert_int_antialias')
        GL.glUniform1fv(uni_vint_antialias, 1, antialias)
        uni_dot_size = GL.glGetUniformLocation(program, 'vert_dot_factor')
        GL.glUniform1fv(uni_dot_size, 1, dot_factor)
        return True
    
    def load_lights(self, program):
        """ Function doc
        """
        light_pos = GL.glGetUniformLocation(program, 'my_light.position')
        GL.glUniform3fv(light_pos, 1, self.light_position)
        light_col = GL.glGetUniformLocation(program, 'my_light.color')
        GL.glUniform3fv(light_col, 1, self.light_color)
        amb_coef = GL.glGetUniformLocation(program, 'my_light.ambient_coef')
        GL.glUniform1fv(amb_coef, 1, self.light_ambient_coef)
        shiny = GL.glGetUniformLocation(program, 'my_light.shininess')
        GL.glUniform1fv(shiny, 1, self.light_shininess)
        intensity = GL.glGetUniformLocation(program, 'my_light.intensity')
        GL.glUniform3fv(intensity, 1, self.light_intensity)
        spec_col = GL.glGetUniformLocation(program, 'my_light.specular_color')
        GL.glUniform3fv(spec_col, 1, self.light_specular_color)
        cam_pos = GL.glGetUniformLocation(program, 'cam_pos')
        GL.glUniform3fv(cam_pos, 1, self.glcamera.get_position())
        return True
    
    def load_data(self, data=None):
        """ In this function you load the data to be displayed. Because of
            using the flag the program loads the data just once. Here you
            bind the coordinates data to the buffer array.
        """
        assert(self.data is not None or data is not None)
        if data is not None:
            self.data = data
        self.dot_list         = []
        self.vdw_list         = []
        self.ball_stick_list  = []
        self.bonds_list       = []
        self.wires_list       = []
        self.sphere_list      = []
        self.pretty_vdw_list  = []
        self.dot_surface_list = []
        self.crystal_list = []
        for chain in self.data[self.frame_i].chains.values():
            for residue in chain.residues.values():
                for atom in residue.atoms.values():
                    if atom.dot:
                        self.dot_list.append(atom)
                    if atom.vdw:
                        self.vdw_list.append(atom)
                    if atom.ball:
                        self.ball_stick_list.append(atom)
                    if atom.sphere:
                        self.sphere_list.append(atom)
                    if atom.dot_surface:
                        self.dot_surface_list.append(atom)
                    if atom.crystal:
                        self.crystal_list.append(atom)
        
        #self.make_gl_sphere(self.ball_stick_program, self.ball_stick_list, self.inner_cryst_vao, False)
        #self.make_gl_cylinder(self.ball_stick_program, self.data[0].bonds, self.bond_cryst_vao, False)
        #self.make_gl_sphere(self.crystal_program, self.crystal_list, self.outer_cryst_vao)
        #self.make_gl_sphere(self.sphere_program, self.sphere_list, self.spheres_vao)
        #self.make_gl_dot_sphere(self.dots_program, self.dot_surface_list, self.dots_surf_vao)
        self.make_gl_dot(self.dots_program, self.dot_surface_list, self.dots_vao)
        #self.make_gl_sphere(self.ball_stick_program, self.ball_stick_list, self.ball_stick_vao, False)
        #self.make_gl_cylinder(self.ball_stick_program, self.data[0].bonds, self.bond_stick_vao, False)
        #self.make_gl_cylinder(self.ribbon_program, self.data[0].ribbons, self.ribbons_vao)
        self.make_gl_lines(self.dots_program, self.data[0].bonds, self.lines_vao)
        print("ended")
        self.modified_data = False
    
    def make_gl_dot(self, program, atom_list, vao_list):
        """ Function doc
        """
        coords = np.array([], dtype=np.float32)
        colors = []
        dot_sizes = []
        for atom in atom_list:
            coords = np.hstack((coords, atom.pos))
            colors = np.hstack((colors, atom.color))
            dot_sizes.append(atom.vdw_rad)
        colors = np.array(colors, dtype=np.float32)
        dot_sizes = np.array(dot_sizes, dtype=np.float32)
        self.dot_qtty = int(len(coords)/3)
        bckgrnd_color = [self.bckgrnd_color[0],self.bckgrnd_color[1],
                         self.bckgrnd_color[2],self.bckgrnd_color[3]]*self.dot_qtty
        bckgrnd_color = np.array(bckgrnd_color, dtype=np.float32)
        
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        
        coord_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
        att_position = GL.glGetAttribLocation(program, 'vert_coord')
        GL.glEnableVertexAttribArray(att_position)
        GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
        
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
        att_colors = GL.glGetAttribLocation(program, 'vert_color')
        GL.glEnableVertexAttribArray(att_colors)
        GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
        
        dot_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, dot_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, dot_sizes.itemsize*len(dot_sizes), dot_sizes, GL.GL_STATIC_DRAW)
        att_size = GL.glGetAttribLocation(program, 'vert_dot_size')
        GL.glEnableVertexAttribArray(att_size)
        GL.glVertexAttribPointer(att_size, 1, GL.GL_FLOAT, GL.GL_FALSE, dot_sizes.itemsize, ctypes.c_void_p(0))
        
        bckgrnd_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, bckgrnd_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, bckgrnd_color.itemsize*len(bckgrnd_color), bckgrnd_color, GL.GL_STATIC_DRAW)
        att_bck_color = GL.glGetAttribLocation(program, 'bckgrnd_color')
        GL.glEnableVertexAttribArray(att_bck_color)
        GL.glVertexAttribPointer(att_bck_color, 4, GL.GL_FLOAT, GL.GL_FALSE, 4*bckgrnd_color.itemsize, ctypes.c_void_p(0))
        
        vao_list.append(vao)
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(att_position)
        GL.glDisableVertexAttribArray(att_colors)
        GL.glDisableVertexAttribArray(att_size)
        GL.glDisableVertexAttribArray(att_bck_color)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    def make_gl_lines(self, program, bond_list, vao_list):
        """ Function doc
        """
        coords = np.array([], dtype=np.float32)
        colors = []
        for bond in bond_list:
            coords = np.hstack((coords, bond[0].pos))
            coords = np.hstack((coords, bond[4]))
            colors = np.hstack((colors, bond[0].color))
            colors = np.hstack((colors, bond[0].color))
            #colors = np.hstack((colors, bond[0].color))
        
        colors = np.array(colors, dtype=np.float32)
        self.line_qtty = int(len(coords)/3)
        
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        
        coord_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
        att_position = GL.glGetAttribLocation(program, 'vert_coord')
        GL.glEnableVertexAttribArray(att_position)
        GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
        
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
        att_colors = GL.glGetAttribLocation(program, 'vert_color')
        GL.glEnableVertexAttribArray(att_colors)
        GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
        
        vao_list.append(vao)
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(att_position)
        GL.glDisableVertexAttribArray(att_colors)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    def make_gl_dot_sphere(self, program, atom_list, vao_list):
        """ Function doc
        """
        for atom in atom_list:
            vertices, indexes, colors = shapes.get_sphere(atom.pos, atom.cov_rad, atom.color, level='level_2')
            vao = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(vao)
            atom.vertices = int(len(vertices)/3)
            
            coord_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.itemsize*int(len(vertices)), vertices, GL.GL_STATIC_DRAW)
            
            att_position = GL.glGetAttribLocation(program, 'vert_coord')
            GL.glEnableVertexAttribArray(att_position)
            GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*vertices.itemsize, ctypes.c_void_p(0))
            
            col_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
            
            att_colors = GL.glGetAttribLocation(program, 'vert_color')
            GL.glEnableVertexAttribArray(att_colors)
            GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
            
            vao_list.append(vao)
            GL.glBindVertexArray(0)
            GL.glDisableVertexAttribArray(att_position)
            GL.glDisableVertexAttribArray(att_colors)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    def make_gl_sphere(self, program, atom_list, vao_list, covalent=True):
        """ Function doc
        """
        self.t_verts = np.array([],dtype=np.float32)
        self.t_inds = np.array([],dtype=np.uint32)
        self.t_cols = np.array([],dtype=np.float32)
        self.t_cents = np.array([],dtype=np.float32)
        for atom in atom_list:
            if covalent:
                vertices, indexes, colors = shapes.get_sphere(atom.pos, atom.cov_rad, atom.color, level='level_1')
            else:
                vertices, indexes, colors = shapes.get_sphere(atom.pos, atom.ball_radius, atom.color, level='level_1')
            centers = [atom.pos[0],atom.pos[1],atom.pos[2]]*int(len(vertices)/3)
            centers = np.array(centers,dtype=np.float32)
            indexes = indexes + int(len(self.t_verts)/3)
            self.t_cents = np.hstack((self.t_cents, centers))
            self.t_verts = np.hstack((self.t_verts, vertices))
            self.t_inds = np.hstack((self.t_inds, indexes))
            self.t_cols = np.hstack((self.t_cols, colors))
        
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        
        ind_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.t_inds.itemsize*int(len(self.t_inds)), self.t_inds, GL.GL_STATIC_DRAW)
    
        coord_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.t_verts.itemsize*int(len(self.t_verts)), self.t_verts, GL.GL_STATIC_DRAW)
        
        att_position = GL.glGetAttribLocation(program, 'vert_coord')
        GL.glEnableVertexAttribArray(att_position)
        GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.t_verts.itemsize, ctypes.c_void_p(0))
    
        center_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, center_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.t_cents.itemsize*int(len(self.t_cents)), self.t_cents, GL.GL_STATIC_DRAW)
        
        att_center = GL.glGetAttribLocation(program, 'vert_center')
        GL.glEnableVertexAttribArray(att_center)
        GL.glVertexAttribPointer(att_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.t_cents.itemsize, ctypes.c_void_p(0))
        
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.t_cols.itemsize*int(len(self.t_cols)), self.t_cols, GL.GL_STATIC_DRAW)
        
        att_colors = GL.glGetAttribLocation(program, 'vert_color')
        GL.glEnableVertexAttribArray(att_colors)
        GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.t_cols.itemsize, ctypes.c_void_p(0))
        
        vao_list.append(vao)
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(att_position)
        GL.glDisableVertexAttribArray(att_colors)
        GL.glDisableVertexAttribArray(att_center)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
        
        #for atom in atom_list:
            #if covalent:
                #vertices, indexes, colors = shapes.get_sphere(atom.pos, atom.cov_rad, atom.color, level='level_2')
            #else:
                #vertices, indexes, colors = shapes.get_sphere(atom.pos, atom.ball_radius, atom.color, level='level_2')
            #centers = [atom.pos[0],atom.pos[1],atom.pos[2]]*int(len(indexes))
            #centers = np.array(centers,dtype=np.float32)
            #vao = GL.glGenVertexArrays(1)
            #GL.glBindVertexArray(vao)
            #atom.triangles = int(len(indexes))
            
            #ind_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
            #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_STATIC_DRAW)
        
            #vert_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vert_vbo)
            #GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.itemsize*int(len(vertices)), vertices, GL.GL_STATIC_DRAW)
            
            #att_position = GL.glGetAttribLocation(program, 'vert_coord')
            #GL.glEnableVertexAttribArray(att_position)
            #GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*vertices.itemsize, ctypes.c_void_p(0))
        
            #center_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, center_vbo)
            #GL.glBufferData(GL.GL_ARRAY_BUFFER, centers.itemsize*int(len(centers)), centers, GL.GL_STATIC_DRAW)
            
            #att_center = GL.glGetAttribLocation(program, 'vert_center')
            #GL.glEnableVertexAttribArray(att_center)
            #GL.glVertexAttribPointer(att_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*centers.itemsize, ctypes.c_void_p(0))
            
            #col_vbo = GL.glGenBuffers(1)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
            #GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
            
            #att_colors = GL.glGetAttribLocation(program, 'vert_color')
            #GL.glEnableVertexAttribArray(att_colors)
            #GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
            
            #vao_list.append(vao)
            #GL.glBindVertexArray(0)
            #GL.glDisableVertexAttribArray(att_position)
            #GL.glDisableVertexAttribArray(att_colors)
            #GL.glDisableVertexAttribArray(att_center)
            #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    def make_gl_cylinder(self, program, bond_list, vao_list, ribbon=True):
        """ Function doc
        """
        for bond in bond_list:
            if ribbon:
                vertices, indexes, colors, normals = shapes.get_cylinder(bond[0].pos,bond[0].color,bond[2],bond[3],bond[1],10,radius=0.2,level='level_6')
                self.ribbon_indexes = int(len(indexes))
            else:
                vertices, indexes, colors, normals = shapes.get_cylinder(bond[0].pos,bond[0].color,bond[2],bond[3],bond[1],10,radius=0.1,level='level_6')
                self.stick_indexes = int(len(indexes))
            vao = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(vao)
            
            ind_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_STATIC_DRAW)
            
            coord_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.itemsize*int(len(vertices)), vertices, GL.GL_STATIC_DRAW)
            
            att_position = GL.glGetAttribLocation(program, 'vert_coord')
            GL.glEnableVertexAttribArray(att_position)
            GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*vertices.itemsize, ctypes.c_void_p(0))
            
            center_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, center_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, normals.itemsize*int(len(normals)), normals, GL.GL_STATIC_DRAW)
            
            att_center = GL.glGetAttribLocation(program, 'vert_center')
            GL.glEnableVertexAttribArray(att_center)
            GL.glVertexAttribPointer(att_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*normals.itemsize, ctypes.c_void_p(0))
            
            col_vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
            
            att_colors = GL.glGetAttribLocation(program, 'vert_color')
            GL.glEnableVertexAttribArray(att_colors)
            GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
            
            vao_list.append(vao)
            GL.glBindVertexArray(0)
            GL.glDisableVertexAttribArray(att_position)
            GL.glDisableVertexAttribArray(att_colors)
            GL.glDisableVertexAttribArray(att_center)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    def draw_dots(self):
        """ Function doc
        """
        assert(len(self.dots_vao)>0)
        GL.glBindVertexArray(self.dots_vao[0])
        GL.glDrawArrays(GL.GL_POINTS, 0, self.dot_qtty)
        GL.glBindVertexArray(0)
    
    def draw_lines(self):
        """ Function doc
        """
        assert(len(self.lines_vao)>0)
        #GL.glPointSize(2)
        GL.glBindVertexArray(self.lines_vao[0])
        GL.glDrawArrays(GL.GL_LINES, 0, self.line_qtty)
        GL.glBindVertexArray(0)
        #GL.glPointSize(2)
    
    def draw_dots_surface(self):
        """ Function doc
        """
        assert(len(self.dots_surf_vao)>0)
        GL.glPointSize(2)
        for i,atom in enumerate(self.dot_surface_list):
            GL.glBindVertexArray(self.dots_surf_vao[i])
            GL.glDrawArrays(GL.GL_POINTS, 0, atom.vertices)
            GL.glBindVertexArray(0)
        GL.glPointSize(2)
    
    def draw_spheres(self):
        """ Function doc
        """
        assert(len(self.spheres_vao)>0)
        GL.glBindVertexArray(self.spheres_vao[0])
        GL.glDrawElements(GL.GL_TRIANGLES, int(len(self.t_inds)), GL.GL_UNSIGNED_INT, None)
        GL.glBindVertexArray(0)
        #assert(len(self.spheres_vao)>0)
        #for i,atom in enumerate(self.sphere_list):
            #GL.glBindVertexArray(self.spheres_vao[i])
            #GL.glDrawElements(GL.GL_TRIANGLES, atom.triangles, GL.GL_UNSIGNED_SHORT, None)
            #GL.glBindVertexArray(0)
    
    def draw_crystal(self):
        """ Function doc
        """
        assert(len(self.crystal_list)>0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        #GL.glDepthFunc(GL.GL_EQUAL)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_SRC_ALPHA)
        GL.glEnable(GL.GL_CULL_FACE)
        for i,atom in enumerate(self.crystal_list):
            GL.glBindVertexArray(self.outer_cryst_vao[i])
            GL.glDrawElements(GL.GL_TRIANGLES, atom.triangles, GL.GL_UNSIGNED_INT, None)
            GL.glBindVertexArray(0)
        #GL.glDepthFunc(GL.GL_LESS)
        GL.glDisable(GL.GL_BLEND)
        GL.glDisable(GL.GL_CULL_FACE)
    
    def draw_ball_stick(self):
        """ Function doc
        """
        assert(len(self.ball_stick_vao)>0)
        for i,atom in enumerate(self.ball_stick_list):
            GL.glBindVertexArray(self.ball_stick_vao[i])
            GL.glDrawElements(GL.GL_TRIANGLES, atom.triangles, GL.GL_UNSIGNED_INT, None)
            GL.glBindVertexArray(0)
        for i,bond in enumerate(self.bond_stick_vao):
            GL.glBindVertexArray(self.bond_stick_vao[i])
            GL.glDrawElements(GL.GL_TRIANGLES, self.stick_indexes, GL.GL_UNSIGNED_INT, None)
            GL.glBindVertexArray(0)
    
    def draw_ribbons(self):
        """ Function doc
        """
        assert(len(self.ribbons_vao)>0)
        for i,bond in enumerate(self.ribbons_vao):
            GL.glBindVertexArray(self.ribbons_vao[i])
            GL.glDrawElements(GL.GL_TRIANGLES, self.ribbon_indexes, GL.GL_UNSIGNED_INT, None)
            GL.glBindVertexArray(0)
    
    def key_press(self, widget, event):
        """ The mouse_button function serves, as the names states, to catch
            events in the keyboard, e.g. letter 'l' pressed, 'backslash'
            pressed. Note that there is a difference between 'A' and 'a'.
            Here I use a specific handler for each key pressed after
            discarding the CONTROL, ALT and SHIFT keys pressed (usefull
            for customized actions) and maintained, i.e. it's the same as
            using Ctrl+Z to undo an action.
        """
        k_name = Gdk.keyval_name(event.keyval)
        func = getattr(self, 'pressed_' + k_name, None)
        #print k_name, 'key Pressed'
        if func:
            func()
        return True
    
    def pressed_Escape(self):
        print('Exit!')
        Gtk.main_quit()
    
    def pressed_k(self):
        self.DOTS = not self.DOTS
        self.queue_draw()
    
    def pressed_j(self):
        self.LINES = not self.LINES
        self.queue_draw()
    
    def pressed_d(self):
        self.DOTS_SURFACE = not self.DOTS_SURFACE
        self.queue_draw()
    
    def pressed_s(self):
        self.SPHERES = not self.SPHERES
        self.queue_draw()
    
    def pressed_y(self):
        self.load_data()
        self.DOTS = not self.DOTS
        self.queue_draw()
    
    def pressed_b(self):
        self.BALL_STICK = not self.BALL_STICK
        self.queue_draw()
    
    def pressed_c(self):
        self.CRYSTAL = not self.CRYSTAL
        self.queue_draw()
    
    def pressed_r(self):
        self.RIBBON = not self.RIBBON
        self.queue_draw()
    
    def pressed_l(self):
        self.modified_data = True
        self.queue_draw()
        print('Load data')
    
    def pressed_m(self):
        temp = np.matrix(self.model_mat[:3,:3]).I * np.matrix([2.030,-1.227,-0.502]).T
        temp = temp.A1
        self.model_mat[3,:3] = -temp
        self.queue_draw()
        print('Load data')
    
    def pressed_n(self):
        self.zero_pt_ref = np.array([2.030,-1.227,-0.502],dtype=np.float32)
        self.model_mat = mop.my_glTranslatef(self.model_mat, self.zero_pt_ref)
        self.queue_draw()
        print('Load data')
    
    def pressed_p(self):
        """ Function doc
        """
        print(self.model_mat, '<-- pos model_mat')
    
    def delete_vaos(self):
        """ Function doc
        """
        # Ball-Stick representation
        if len(self.ball_stick_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.ball_stick_vao)), self.ball_stick_vao)
            GL.glDeleteVertexArrays(int(len(self.bond_stick_vao)), self.bond_stick_vao)
            self.ball_stick_vao = []
            self.bond_stick_vao = []
        # Ribbon representation
        if len(self.ribbons_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.ribbons_vao)), self.ribbons_vao)
            self.ribbons_vao = []
        # Covalent radius representation
        if len(self.spheres_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.spheres_vao)), self.spheres_vao)
            self.spheres_vao = []
        # Dots representation
        if len(self.dots_surf_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.dots_surf_vao)), self.dots_surf_vao)
            self.dots_surf_vao = []
        # Dotted surface representation
        if len(self.dots_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.dots_vao)), self.dots_vao)
            self.dots_vao = []
        # Lines representation
        if len(self.lines_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.lines_vao)), self.lines_vao)
            self.lines_vao = []
        # Van der Waals representation
        if len(self.vdw_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.vdw_vao)), self.vdw_vao)
            self.vdw_vao = []
        # Transparent Representataion
        if len(self.inner_cryst_vao)>0:
            GL.glDeleteVertexArrays(int(len(self.inner_cryst_vao)), self.inner_cryst_vao)
            GL.glDeleteVertexArrays(int(len(self.bond_cryst_vao)), self.bond_cryst_vao)
            GL.glDeleteVertexArrays(int(len(self.outer_cryst_vao)), self.outer_cryst_vao)
            self.inner_cryst_vao = []
            self.bond_cryst_vao = []
            self.outer_cryst_vao = []
    
    def mouse_pressed(self, widget, event):
        left   = event.button==1 and event.type==Gdk.EventType.BUTTON_PRESS
        middle = event.button==2 and event.type==Gdk.EventType.BUTTON_PRESS
        right  = event.button==3 and event.type==Gdk.EventType.BUTTON_PRESS
        self.mouse_rotate = left and not (middle or right)
        self.mouse_zoom   = right and not (middle or left)
        self.mouse_pan    = middle and not (right or left)
        x = self.mouse_x = event.x
        y = self.mouse_y = event.y
        self.drag_pos_x, self.drag_pos_y, self.drag_pos_z = self.pos(x, y)
    
    def mouse_released(self, widget, event):
        pass
        self.mouse_rotate = self.mouse_zoom = self.mouse_pan = False
    
    def mouse_motion(self, widget, event):
        x = event.x
        y = event.y
        state = event.state
        dx = x - self.mouse_x
        dy = y - self.mouse_y
        if (dx==0 and dy==0):
            return
        self.mouse_x, self.mouse_y = x, y
        changed = False
        if self.mouse_rotate:
            angle = math.sqrt(dx**2+dy**2)/float(self.width+1)*180.0
            self.model_mat = mop.my_glRotatef(self.model_mat, angle, [-dy, -dx, 0])
            self.update_normal_mat()
            changed = True
        elif self.mouse_pan:
            px, py, pz = self.pos(x, y)
            pan_matrix = mop.my_glTranslatef(np.identity(4,dtype=np.float32),
                [(px-self.drag_pos_x)*self.glcamera.z_far/10, 
                 (py-self.drag_pos_y)*self.glcamera.z_far/10, 
                 (pz-self.drag_pos_z)*self.glcamera.z_far/10])
            self.model_mat = mop.my_glMultiplyMatricesf(self.model_mat, pan_matrix)
            self.update_normal_mat()
            self.drag_pos_x = px
            self.drag_pos_y = py
            self.drag_pos_z = pz
            changed = True
        elif self.mouse_zoom:
            delta = (((self.glcamera.z_far-self.glcamera.z_near)/2)+self.glcamera.z_near)/200
            direction = mop.my_glForwardVectorAbs(self.glcamera.get_view_matrix())
            #self.model_mat = mop.my_glTranslatef(self.model_mat, -dy*delta*direction)
            self.glcamera.move_position(dy*delta*direction)
            changed = True
        if changed:
            self.queue_draw()
        
    def mouse_scroll(self, widget, event):
        if event.direction == Gdk.ScrollDirection.UP:
            self.glcamera.z_near -= self.scroll
            self.glcamera.z_far += self.scroll
        if event.direction == Gdk.ScrollDirection.DOWN:
            self.glcamera.z_near += self.scroll
            self.glcamera.z_far -= self.scroll
        if self.glcamera.z_near < 0:
            self.glcamera.z_near = 0.001
        if self.glcamera.z_far < self.glcamera.z_near:
            self.glcamera.z_near -= self.scroll
            self.glcamera.z_far = self.glcamera.z_near + 0.05
        self.queue_draw()
    
    def update_normal_mat(self):
        """ Function doc
        """
        modelview = mop.my_glMultiplyMatricesf(self.glcamera.get_view_matrix(), self.model_mat)
        normal_mat = np.matrix(modelview[:3,:3]).I.T
        self.normal_mat = np.array(normal_mat)
        #model = np.matrix(self.model_mat[:3,:3]).I.T
        #self.normal_mat = np.array(model)
    
    def pos(self, x, y):
        """
        Use the ortho projection and viewport information
        to map from mouse co-ordinates back into world
        co-ordinates
        """
        px = x/float(self.width)
        py = y/float(self.height)
        px = self.left + px*(self.right-self.left)
        py = self.top + py*(self.bottom-self.top)
        pz = self.glcamera.z_near
        return px, py, pz
    
