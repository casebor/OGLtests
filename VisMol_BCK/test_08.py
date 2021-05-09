#!/usr/bin/env python3

import math
import numpy as np
import ctypes
import camera as cam
import shaders as sh

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import OpenGL
from OpenGL import GL

class MyGLProgram(Gtk.GLArea):
    
    def __init__(self):
        super(MyGLProgram, self).__init__()
        self.connect("realize", self.initialize)
        self.connect("render", self.render)
        self.connect("key-press-event", self.key_pressed)
        self.connect("key-release-event", self.key_released)
        self.grab_focus()
        self.set_events( self.get_events() | Gdk.EventMask.SCROLL_MASK
                       | Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK
                       | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.POINTER_MOTION_HINT_MASK
                       | Gdk.EventMask.KEY_PRESS_MASK | Gdk.EventMask.KEY_RELEASE_MASK )
    
    def initialize(self, widget):
        aloc = self.get_allocation()
        w = np.float32(aloc.width)
        h = np.float32(aloc.height)
        self.model_mat = np.identity(4, dtype=np.float32)
        self.view_mat = cam.my_glTranslatef(np.identity(4, dtype=np.float32), np.array([0,0,-3],dtype=np.float32))
        self.proj_mat = cam.my_gluPerspectivef(np.identity(4, dtype=np.float32), 30, w/h, 0.1, 10.0)
        self.degrees = np.float32(0)
        self.set_has_depth_buffer(True)
        self.set_has_alpha(True)
        self.gl_programs = True
        # Here are the test programs and flags
        self.gl_program_diamonds = None
        self.gl_program_circles = None
        self.diamonds = True
        self.circles = True
    
    def create_gl_programs(self):
        """ Function doc
        """
        print('OpenGL version: ',GL.glGetString(GL.GL_VERSION))
        try:
            print('OpenGL major version: ',GL.glGetDoublev(GL.GL_MAJOR_VERSION))
            print('OpenGL minor version: ',GL.glGetDoublev(GL.GL_MINOR_VERSION))
        except:
            print('OpenGL major version not found')
        self.gl_program_diamonds = self.load_shaders(sh.v_shader_diamonds, sh.f_shader_diamonds, sh.g_shader_diamonds)
        self.gl_program_circles = self.load_shaders(sh.v_shader_circles, sh.f_shader_circles)
    
    def load_shaders(self, vertex, fragment, geometry=None):
        """ Here the shaders are loaded and compiled to an OpenGL program. By default
            the constructor shaders will be used, if you want to change the shaders
            use this function. The flag is used to create only one OpenGL program.
            
            Keyword arguments:
            vertex -- The vertex shader to be used
            fragment -- The fragment shader to be used
        """
        my_vertex_shader = self.create_shader(vertex, GL.GL_VERTEX_SHADER)
        my_fragment_shader = self.create_shader(fragment, GL.GL_FRAGMENT_SHADER)
        if geometry is not None:
            my_geometry_shader = self.create_shader(geometry, GL.GL_GEOMETRY_SHADER)
        program = GL.glCreateProgram()
        GL.glAttachShader(program, my_vertex_shader)
        GL.glAttachShader(program, my_fragment_shader)
        if geometry is not None:
            GL.glAttachShader(program, my_geometry_shader)
        GL.glLinkProgram(program)
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
    
    def load_matrices(self, program):
        """ Function doc
        """
        model = GL.glGetUniformLocation(program, 'model_mat')
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, self.model_mat)
        view = GL.glGetUniformLocation(program, 'view_mat')
        GL.glUniformMatrix4fv(view, 1, GL.GL_FALSE, self.view_mat)
        proj = GL.glGetUniformLocation(program, 'projection_mat')
        GL.glUniformMatrix4fv(proj, 1, GL.GL_FALSE, self.proj_mat)
    
    def render(self, area, context):
        if self.gl_programs:
            self.create_gl_programs()
            self.gl_programs = False
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        if self.diamonds:
            pass
        
        if self.circles:
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glUseProgram(self.gl_program_circles)
            GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
            self.load_matrices(self.gl_program_circles)
            self.load_data(self.gl_program_circles)
            GL.glBindVertexArray(self.vertex_array_object)
            if self.coords is None:
                pass
            else:
                GL.glDrawArrays(GL.GL_POINTS, 0, int(len(self.coords)/3))
                #GL.glDrawElements(GL.GL_LINES, int(len(self.coords)), GL.GL_UNSIGNED_SHORT, None)
            GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
            GL.glDisable(GL.GL_DEPTH_TEST)
            GL.glBindVertexArray(0)
            GL.glUseProgram(0)
        
        self.degrees += 1
        if self.degrees >= 360:
            self.degrees = np.float32(0)
    
    def load_data(self, program):
        self.vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vertex_array_object)
        
        #self.coords = 0.45 * np.random.randn(1000000, 3)
        #self.colors = np.random.uniform(0.85, 1.00, (1000000, 4))
        a_size = np.random.uniform(.1, .2, 1000000)
        
        self.coords = np.array([1.0, 1.0, 0.0,
                                0.0, 1.0, 0.0,
                                1.0, 0.0, 0.0,
                               -1.0, 0.0, 0.0,
                               -1.0, 1.0, 0.0,
                               -1.0,-1.0, 0.0,
                                0.0,-1.0, 0.0,
                                1.0,-1.0, 0.0,
                                0.0, 0.0, 0.0],dtype=np.float32)
        self.colors = np.array([1.0, 0.0, 0.0,
                                1.0, 1.0, 0.0,
                                1.0, 0.0, 1.0,
                                0.0, 0.0, 1.0,
                                0.0, 1.0, 0.0,
                                0.0, 1.0, 1.0,
                                0.0, 1.0, 0.0,
                                0.0, 1.0, 0.0,
                                0.0, 1.0, 0.0],dtype=np.float32)
        
        coord_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.coords.itemsize*len(self.coords), self.coords, GL.GL_STATIC_DRAW)
        position = GL.glGetAttribLocation(program, 'vert_coord')
        GL.glEnableVertexAttribArray(position)
        GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.coords.itemsize, ctypes.c_void_p(0))
        
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.colors.itemsize*len(self.colors), self.colors, GL.GL_STATIC_DRAW)
        gl_colors = GL.glGetAttribLocation(program, 'vert_color')
        GL.glEnableVertexAttribArray(gl_colors)
        GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.colors.itemsize, ctypes.c_void_p(0))
         
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(position)
        GL.glDisableVertexAttribArray(gl_colors)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    
    def key_pressed(self, widget, event):
        """ Function doc
        """
        k_name = Gdk.keyval_name(event.keyval)
        func = getattr(self, '_pressed_' + k_name, None)
        print(k_name)
        if func:
            func()
        return True
    
    def key_released(self, widget, event):
        """ Function doc
        """
        k_name = Gdk.keyval_name(event.keyval)
        func = getattr(self, '_released_' + k_name, None)
        if func:
            func()
        return True
    
    def _pressed_Right(self):
        """ Function doc """
        pass
    
    def _pressed_Left(self):
        """ Function doc """
        pass
    
    def _pressed_Up(self):
        """ Function doc """
        pass
    
    def _pressed_Down(self):
        """ Function doc """
        pass
    

test = MyGLProgram()
wind = Gtk.Window()
wind.add(test)

wind.connect("delete-event", Gtk.main_quit)
wind.connect("key-press-event", test.key_pressed)
wind.connect("key-release-event", test.key_released)
wind.show_all()
Gtk.main()
