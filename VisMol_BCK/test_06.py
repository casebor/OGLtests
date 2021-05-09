#!/usr/bin/env python

import math
import numpy as np
import ctypes
import camera as cam

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import OpenGL
from OpenGL import GL
from OpenGL.GL import shaders

global degrees
degrees = np.float32(0)

class MyGLProgram():
    def __init__(self, vertex, geometry, fragment):
        self.glarea = Gtk.GLArea.new()
        self.glarea.connect("realize", self.initialize)
        self.glarea.connect("render", self.render)
        self.vertex_shader = vertex
        self.geometry_shader = geometry
        self.fragment_shader = fragment
        self.model_mat = self.view_mat = self.proj_mat = np.identity(4, dtype=np.float32)
        
    def initialize(self, otro):
        self.glarea.set_has_depth_buffer(True)
        self.glarea.set_has_alpha(True)
        self.flag = True
    
    def load_shaders(self):
        my_vertex = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        GL.glShaderSource(my_vertex, self.vertex_shader)
        GL.glCompileShader(my_vertex)
        if GL.glGetShaderiv(my_vertex, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", GL.GL_VERTEX_SHADER)
        my_geometry = GL.glCreateShader(GL.GL_GEOMETRY_SHADER)
        GL.glShaderSource(my_geometry, self.geometry_shader)
        GL.glCompileShader(my_geometry)
        if GL.glGetShaderiv(my_geometry, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", GL.GL_GEOMETRY_SHADER)
        my_fragment = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        GL.glShaderSource(my_fragment, self.fragment_shader)
        GL.glCompileShader(my_fragment)
        if GL.glGetShaderiv(my_fragment, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", GL.GL_FRAGMENT_SHADER)
        self.program = GL.glCreateProgram()
        GL.glAttachShader(self.program, my_vertex)
        GL.glAttachShader(self.program, my_geometry)
        GL.glAttachShader(self.program, my_fragment)
        GL.glLinkProgram(self.program)
        GL.glValidateProgram(self.program)
        self.load_data()
        self.flag = False
    
    def render(self, area, context):
        if self.flag:
            self.load_shaders()
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glUseProgram(self.program)
        
        global degrees
        model = view = proj = np.identity(4, dtype=np.float32)
        model = cam.my_glRotateYf(model, degrees)
        view = cam.my_glTranslatef(view, np.array([0,0,-3],dtype=np.float32))
        aloc = self.glarea.get_allocation()
        w = np.float32(aloc.width)
        h = np.float32(aloc.height)
        proj = cam.my_gluPerspectivef(proj, 30, w/h, 0.1, 10.0)
        
        self.model = GL.glGetUniformLocation(self.program, 'model_mat')
        GL.glUniformMatrix4fv(self.model, 1, GL.GL_FALSE, model)
        self.view = GL.glGetUniformLocation(self.program, 'view_mat')
        GL.glUniformMatrix4fv(self.view, 1, GL.GL_FALSE, view)
        self.proj = GL.glGetUniformLocation(self.program, 'projection_mat')
        GL.glUniformMatrix4fv(self.proj, 1, GL.GL_FALSE, proj)
        
        GL.glBindVertexArray(self.vertex_array_object)
        if self.coords is None:
            pass
        else:
            GL.glDrawArrays(GL.GL_POINTS, 0, int(len(self.coords)/3))
        
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
        degrees += 1
        if degrees >= 360:
            degrees = np.float32(0)
    
    def load_data(self):
        self.vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vertex_array_object)
        
        self.coords = 0.45 * np.random.randn(1000000, 3)
        self.colors = np.random.uniform(0.85, 1.00, (1000000, 4))
        a_size = np.random.uniform(.1, .2, 1000000)
        
        #self.coords = np.array([1.0, 1.0, 0.0,
                                #0.0, 1.0, 0.0,
                                #1.0, 0.0, 0.0,
                               #-1.0, 0.0, 0.0,
                               #-1.0, 1.0, 0.0,
                               #-1.0,-1.0, 0.0,
                                #0.0,-1.0, 0.0,
                                #1.0,-1.0, 0.0,
                                #0.0, 0.0, 0.0],dtype=np.float32)
        #self.colors = np.array([1.0, 0.0, 0.0,
                                #1.0, 1.0, 0.0,
                                #1.0, 0.0, 1.0,
                                #0.0, 0.0, 1.0,
                                #0.0, 1.0, 0.0,
                                #0.0, 1.0, 1.0,
                                #0.0, 1.0, 0.0,
                                #0.0, 1.0, 0.0,
                                #0.0, 1.0, 0.0],dtype=np.float32)
        
        
        coord_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.coords.itemsize*len(self.coords), self.coords, GL.GL_STATIC_DRAW)
        position = GL.glGetAttribLocation(self.program, 'vert_coord')
        GL.glEnableVertexAttribArray(position)
        GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.coords.itemsize, ctypes.c_void_p(0))
        
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.colors.itemsize*len(self.colors), self.colors, GL.GL_STATIC_DRAW)
        gl_colors = GL.glGetAttribLocation(self.program, 'vert_color')
        GL.glEnableVertexAttribArray(gl_colors)
        GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.colors.itemsize, ctypes.c_void_p(0))
         
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(position)
        GL.glDisableVertexAttribArray(gl_colors)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

vertex_shader = """
#version 330

in vec3 vert_coord;
in vec3 vert_color;

out vec3 geom_color;

void main()
{
   geom_color = vert_color;
   gl_Position = vec4(vert_coord, 1.0);
}
"""

geometry_shader = """
#version 330

layout (points) in; // Name for use is gl_in[] is default for GLSL
layout (points, max_vertices = 6) out;

in vec3 geom_color[];

out vec3 sh_color;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;

void main()
{
   vec4 offset = vec4(0.2, 0.0, 0.0, 1.0);
   vec4 vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   EndPrimitive();
   
   offset = vec4(-.2, 0.0, 0.0, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   EndPrimitive();
   
   offset = vec4(0.0, 0.2, 0.0, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   EndPrimitive();
   
   offset = vec4(0.0,-0.2, 0.0, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   EndPrimitive();
   
   offset = vec4(0.0, 0.0, 0.2, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   EndPrimitive();
   
   offset = vec4(0.0, 0.0,-0.2, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   EndPrimitive();
   
}
"""
 
fragment_shader = """
#version 330

in vec3 sh_color;

out vec4 final_color;

void main()
{
   final_color = vec4(sh_color, 1.0);
}
"""

test = MyGLProgram(vertex_shader, geometry_shader, fragment_shader)
wind = Gtk.Window()
wind.add(test.glarea)

wind.connect("delete-event", Gtk.main_quit)
wind.show_all()
Gtk.main()





























