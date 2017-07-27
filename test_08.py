#!/usr/bin/env python3

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

class MyGLProgram():
    def __init__(self, vertex, fragment, geometry=None):
        self.glarea = Gtk.GLArea.new()
        self.glarea.connect("realize", self.initialize)
        self.glarea.connect("render", self.render)
        self.vertex_shader = vertex
        self.geometry_shader = geometry
        self.fragment_shader = fragment
        self.model_mat = np.identity(4, dtype=np.float32)
        self.view_mat = np.identity(4, dtype=np.float32)
        self.proj_mat = np.identity(4, dtype=np.float32)
        self.degrees = np.float32(0)
    
    def initialize(self, otro):
        self.glarea.set_has_depth_buffer(True)
        self.glarea.set_has_alpha(True)
        self.flag = True
    
    def create_gl_programs(self):
        """ Function doc
        """
        print('OpenGL version: ',GL.glGetString(GL.GL_VERSION))
        try:
            print('OpenGL major version: ',GL.glGetDoublev(GL.GL_MAJOR_VERSION))
            print('OpenGL minor version: ',GL.glGetDoublev(GL.GL_MINOR_VERSION))
        except:
            print('OpenGL major version not found')
        self.program = self.load_shaders(vertex_shader, fragment_shader, geometry_shader)
        self.program2 = self.load_shaders(vertex_shader2, fragment_shader2)
    
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
        model = view = proj = np.identity(4, dtype=np.float32)
        model = cam.my_glRotateYf(model, self.degrees)
        view = cam.my_glTranslatef(view, np.array([0,0,-3],dtype=np.float32))
        aloc = self.glarea.get_allocation()
        w = np.float32(aloc.width)
        h = np.float32(aloc.height)
        proj = cam.my_gluPerspectivef(proj, 30, w/h, 0.1, 10.0)
        
        self.model = GL.glGetUniformLocation(program, 'model_mat')
        GL.glUniformMatrix4fv(self.model, 1, GL.GL_FALSE, model)
        self.view = GL.glGetUniformLocation(program, 'view_mat')
        GL.glUniformMatrix4fv(self.view, 1, GL.GL_FALSE, view)
        self.proj = GL.glGetUniformLocation(program, 'projection_mat')
        GL.glUniformMatrix4fv(self.proj, 1, GL.GL_FALSE, proj)
    
    def render(self, area, context):
        if self.flag:
            self.create_gl_programs()
            self.flag = False
        
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        #GL.glUseProgram(self.program)
        #self.load_matrices(self.program)
        #self.load_data(self.program)
        
        #GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        GL.glUseProgram(self.program2)
        GL.glPointSize(50)
        self.load_matrices(self.program2)
        self.load_data(self.program2)
        GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        #GL.glDisable(GL.GL_DEPTH_TEST)
        
        GL.glBindVertexArray(self.vertex_array_object)
        if self.coords is None:
            pass
        else:
            GL.glDrawArrays(GL.GL_POINTS, 0, int(len(self.coords)/3))
        
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
layout (triangle_strip, max_vertices = 14) out;

in vec3 geom_color[];

out vec3 sh_color;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;

void main()
{
   vec4 offset = vec4(0.0, 0.5, 0.0, 1.0);
   vec4 vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   offset = vec4(-.5, 0.0, 0.0, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   offset = vec4(0.0, 0.0, 0.5, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   offset = vec4(0.0,-0.5, 0.0, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   offset = vec4(0.5, 0.0, 0.0, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   offset = vec4(0.0, 0.0,-0.5, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   offset = vec4(0.0, 0.5, 0.0, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   offset = vec4(-.5, 0.0, 0.0, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   EndPrimitive();
   
   offset = vec4(-.5, 0.0, 0.0, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   offset = vec4(0.0, 0.0,-0.5, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   offset = vec4(0.0,-0.5, 0.0, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   EndPrimitive();
   
   offset = vec4(0.0, 0.5, 0.0, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   offset = vec4(0.0, 0.0, 0.5, 1.0);
   vertPos = offset + gl_in[0].gl_Position;
   gl_Position = projection_mat * view_mat * model_mat * vertPos;
   sh_color = geom_color[0];
   EmitVertex();
   offset = vec4(0.5, 0.0, 0.0, 1.0);
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

vertex_shader2 = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;

in vec3 vert_coord;
in vec3 vert_color;

out vec3 frag_color;

void main()
{
   frag_color = vert_color;
   gl_Position = projection_mat * view_mat * model_mat * vec4(vert_coord, 1.0);
}
"""
fragment_shader2 = """
#version 330

in vec3 frag_color;
out vec4 final_color;

void main(){
    float dist = length((gl_PointCoord - vec2(0.5, 0.5)));
    if (dist > 0.5)
        discard;
    if (dist >= 0. && dist <= 0.5)
        final_color = mix(vec4(frag_color,1), vec4(0, 0, 0, 1), dist);
    else
        final_color = vec4(frag_color, 1);
}
"""





test = MyGLProgram(vertex_shader, geometry_shader, fragment_shader)
wind = Gtk.Window()
wind.add(test.glarea)

wind.connect("delete-event", Gtk.main_quit)
wind.show_all()
Gtk.main()
