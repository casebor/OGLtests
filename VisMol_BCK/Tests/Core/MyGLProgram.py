#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  MyGLProgram.py
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

import numpy as np
import math
import camera as cam
import shaders as sh
import VisMolFont as vmf
import vaos
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from OpenGL import GL

class MyGLProgram(Gtk.GLArea):
    
    def __init__(self, width=350, height=250):
        """ Function doc """
        super(MyGLProgram, self).__init__()
        self.connect("realize", self.initialize)
        self.connect("resize", self.reshape_window)
        self.connect("render", self.render)
        self.connect("key-press-event", self.key_pressed)
        self.connect("key-release-event", self.key_released)
        self.connect("scroll-event", self.mouse_scroll)
        self.connect("button-press-event", self.mouse_pressed)
        self.connect("motion-notify-event", self.mouse_motion)
        self.connect("button-release-event", self.mouse_released)
        self.grab_focus()
        self.set_events( self.get_events() | Gdk.EventMask.SCROLL_MASK
                       | Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK
                       | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.POINTER_MOTION_HINT_MASK
                       | Gdk.EventMask.KEY_PRESS_MASK | Gdk.EventMask.KEY_RELEASE_MASK )
    
    def initialize(self, widget):
        """ Function doc """
        aloc = self.get_allocation()
        self.width = np.float32(aloc.width)
        self.height = np.float32(aloc.height)
        self.z_near = 1.0
        self.z_far = 9.0
        self.min_znear = 0.1
        self.min_zfar = 1.1
        self.model_mat = np.identity(4, dtype=np.float32)
        self.view_mat = cam.my_glTranslatef(np.identity(4, dtype=np.float32), [0, 0, -5])
        self.cam_pos = self.get_cam_pos()
        self.fov = 20.0 # Field Of View = fov
        self.var = self.width/self.height # Viewport Aspect Ratio
        self.top = np.float32(1.0)
        self.bottom = -self.top
        self.proj_mat = cam.my_glPerspectivef(self.fov, self.var, self.z_near, self.z_far)
        # self.proj_mat = cam.my_gluPerspective(self.fov, self.var, self.z_near, self.z_far)
        self.set_has_depth_buffer(True)
        self.set_has_alpha(True)
        self.gl_programs = True
        self.right = self.width / self.height
        self.left = -self.right
        self.top = 1.0
        self.bottom = -1.0
        self.scroll = 0.3
        self.edit_points = []
        self.editing = False
        self.mouse_rotate = False
        self.mouse_pan = False
        self.mouse_zoom = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.drag_pos_x = 0
        self.drag_pos_y = 0
        self.drag_pos_z = 0
        self.dx = 0.0
        self.dy = 0.0
        self.start_time = time.perf_counter()
        self.ctrl = False
        self.shift = False
        self.bckgrnd_color = np.array([0.0, 0.0, 0.0, 1.0],dtype=np.float32)
        self.bckgrnd_color = np.array([0.5, 0.5, 0.5, 1.0],dtype=np.float32)
        self.light_position = np.array([-2.5, 2.5, 2.5],dtype=np.float32)
        self.light_color = np.array([1.0, 1.0, 1.0, 1.0],dtype=np.float32)
        self.light_ambient_coef = 0.5
        self.light_shininess = 5.5
        self.light_intensity = np.array([0.6, 0.6, 0.6],dtype=np.float32)
        self.light_specular_color = np.array([1.0, 1.0, 1.0],dtype=np.float32)
        # Here are the test programs and flags
        self.gl_program_dots = None
        self.dots_vao = None
        self.dots_vbos = None
        self.dots_elemns = None
        self.dots = False
        self.gl_program_diamonds = None
        self.diamonds_vao = None
        self.diamonds_vbos = None
        self.diamonds_elemns = None
        self.diamonds = False
        self.gl_program_circles = None
        self.circles_vao = None
        self.circles_vbos = None
        self.circles_elemns = None
        self.circles = False
        self.gl_program_lines = None
        self.lines_vao = None
        self.lines_vbos = None
        self.lines_elemns = None
        self.lines = False
        self.gl_program_antialias = None
        self.antialias_vao = None
        self.antialias_vbos = None
        self.antialias_elemns = None
        self.antialias = False
        self.antialias_length = 0.03
        self.gl_program_pseudospheres = None
        self.pseudospheres_vao = None
        self.pseudospheres_vbos = None
        self.pseudospheres_elemns = None
        self.pseudospheres = False
        self.gl_program_non_bonded = None
        self.non_bonded_vao = None
        self.non_bonded_vbos = None
        self.non_bonded_elemns = None
        self.non_bonded = False
        self.gl_program_geom_cones = None
        self.geom_cones_vao = None
        self.geom_cones_vbos = None
        self.geom_cones_elemns = None
        self.geom_cones = False
        self.gl_program_arrow = None
        self.arrow_vao = None
        self.arrow_vbos = None
        self.arrow_elemns = None
        self.arrow = False
        self.gl_program_select_box = None
        self.select_box_vao = None
        self.select_box_vbos = None
        self.select_box_elemns = None
        self.select_box = False
        self.gl_program_edit_mode = None
        self.edit_mode_vao = None
        self.edit_mode_vbos = None
        self.edit_mode_elemns = None
        self.modified_points = False
        self.gl_program_texture = None
        self.texture_vao = None
        self.texture_vbos = None
        self.texture_elemns = None
        self.texture = False
        self.tex = None
        self.gl_program_text = None
        self.text_vao = None
        self.text_vbos = None
        self.text_elemns = None
        self.text = False
        self.text_texture = None
        self.gl_program_freetype = None
        #self.freetype_vao = None
        #self.freetype_vbos = None
        #self.freetype_elemns = None
        self.freetype = False
        #self.freetype_texture = None
        self.vm_font = vmf.VisMolFont()
        self.gl_program_cylinders = None
        self.cylinders_vao = None
        self.cylinders_vbos = None
        self.cylinders_elemns = None
        self.cylinders = False
        self.gl_program_dots_surface = None
        self.dots_surface_vao = None
        self.dots_surface_vbos = None
        self.dots_surface_elemns = None
        self.dots_surface = False
        self.gl_program_icosahedron = None
        self.icosahedron_vao = None
        self.icosahedron_vbos = None
        self.icosahedron_elemns = None
        self.icosahedron = False
        self.gl_program_sphere = None
        self.sphere_vao = None
        self.sphere_vbos = None
        self.sphere_elemns = None
        self.sphere = False
        self.gl_program_lines_1 = None
        self.lines_1_vao = None
        self.lines_1_vbos = None
        self.lines_1_elemns = None
        self.lines_1 = False
        self.gl_program_triangles = None
        self.triangles_vao = None
        self.triangles_vbos = None
        self.triangles_elemns = None
        self.triangles = False
        self.gl_program_impostor = None
        self.impostor_vao = None
        self.impostor_vbos = None
        self.impostor_elemns = None
        self.impostor = False
        self.gl_program_test = None
        self.test_vao = None
        self.test_vbos = None
        self.test_elemns = None
        self.test = False
    
    def reshape_window(self, widget, width, height):
        """ Function doc """
        self.width = np.float32(width)
        self.height = np.float32(height)
        self.right = self.width / self.height
        self.left = -self.right
        self.var = self.width/self.height # Viewport Aspect Ratio
        self.top = np.float32(1.0)
        self.bottom = -self.top
        self.proj_mat = cam.my_glPerspectivef(self.fov, self.var, self.z_near, self.z_far)
        # self.proj_mat = cam.my_gluPerspective(self.fov, self.var, self.z_near, self.z_far)
    
    def create_gl_programs(self):
        """ Function doc """
        print('OpenGL version: ',GL.glGetString(GL.GL_VERSION))
        try:
            print('OpenGL major version: ',GL.glGetDoublev(GL.GL_MINOR_VERSION))
            print('OpenGL minor version: ',GL.glGetDoublev(GL.GL_MAJOR_VERSION))
        except:
            print('OpenGL major version not found')
        self.gl_program_diamonds = self.load_shaders(sh.v_shader_diamonds, sh.f_shader_diamonds, sh.g_shader_diamonds)
        self.gl_program_dots = self.load_shaders(sh.v_shader_dots, sh.f_shader_dots)
        self.gl_program_circles = self.load_shaders(sh.v_shader_circles, sh.f_shader_circles)
        self.gl_program_lines = self.load_shaders(sh.v_shader_lines, sh.f_shader_lines, sh.g_shader_lines)
        self.gl_program_antialias = self.load_shaders(sh.v_shader_antialias, sh.f_shader_antialias, sh.g_shader_antialias)
        self.gl_program_pseudospheres = self.load_shaders(sh.v_shader_pseudospheres, sh.f_shader_pseudospheres, sh.g_shader_pseudospheres5)
        self.gl_program_non_bonded = self.load_shaders(sh.v_shader_non_bonded, sh.f_shader_non_bonded, sh.g_shader_non_bonded)
        self.gl_program_geom_cones = self.load_shaders(sh.v_shader_geom_cones, sh.f_shader_geom_cones)
        self.gl_program_arrow = self.load_shaders(sh.v_shader_arrow, sh.f_shader_arrow, sh.g_shader_arrow)
        self.gl_program_select_box = self.load_shaders(sh.v_shader_select_box, sh.f_shader_select_box)
        self.gl_program_edit_mode = self.load_shaders(sh.v_shader_edit_mode, sh.f_shader_edit_mode)
        self.gl_program_texture = self.load_shaders(sh.v_shader_texture, sh.f_shader_texture)
        #self.gl_program_text = self.load_shaders(sh.v_shader_text, sh.f_shader_text, sh.g_shader_text)
        self.gl_program_text = self.load_shaders(sh.v_shader_text, sh.f_shader_text, sh.g_shader_text)
        self.gl_program_freetype = self.load_shaders(sh.v_shader_freetype, sh.f_shader_freetype, sh.g_shader_freetype)
        self.gl_program_cylinders = self.load_shaders(sh.v_shader_cylinders, sh.f_shader_cylinders, sh.g_shader_cylinders)
        self.gl_program_dots_surface = self.load_shaders(sh.v_shader_dots_surface, sh.f_shader_dots_surface, sh.g_shader_dots_surface)
        self.gl_program_icosahedron = self.load_shaders(sh.v_shader_icosahedron, sh.f_shader_icosahedron, sh.g_shader_icosahedron)
        self.gl_program_sphere = self.load_shaders(sh.v_shader_sphere, sh.f_shader_sphere)
        self.gl_program_lines_1 = self.load_shaders(sh.v_shader_lines_1, sh.f_shader_lines_1, sh.g_shader_lines_2)
        self.gl_program_triangles = self.load_shaders(sh.v_shader_triangles, sh.f_shader_triangles)
        self.gl_program_impostor = self.load_shaders(sh.v_shader_impostor, sh.f_shader_impostor, sh.g_shader_impostor)
        self.gl_program_test = self.load_shaders(sh.v_shader_test, sh.f_shader_test)
    
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
        """ Function doc """
        model = GL.glGetUniformLocation(program, 'model_mat')
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, self.model_mat)
        view = GL.glGetUniformLocation(program, 'view_mat')
        GL.glUniformMatrix4fv(view, 1, GL.GL_FALSE, self.view_mat)
        proj = GL.glGetUniformLocation(program, 'proj_mat')
        GL.glUniformMatrix4fv(proj, 1, GL.GL_FALSE, self.proj_mat)
    
    def load_test_data(self, program):
        """ Function doc """
        model = GL.glGetUniformLocation(program, 'u_resolution')
        GL.glUniform2fv(model, 1, np.array([self.width, self.height], dtype=np.float32))
    
    def load_impostor_params(self, program):
        """ Function doc """
        # uBottomLeft = GL.glGetUniformLocation(program, 'uBottomLeft')
        # GL.glUniform2fv(uBottomLeft, 1, np.array([self.left, self.bottom], dtype=np.float32))
        # uTopRight = GL.glGetUniformLocation(program, 'uTopRight')
        # GL.glUniform2fv(uTopRight, 1, np.array([self.right, self.top], dtype=np.float32))
        # uRes = GL.glGetUniformLocation(program, 'uRes')
        # GL.glUniform2fv(uRes, 1, np.array([self.width, self.height], dtype=np.float32))
        # uRes = GL.glGetUniformLocation(program, 'uRes')
        # GL.glUniform1fv(uRes, 1, self.width*self.height)
        u_depth = GL.glGetUniformLocation(program, 'u_depth')
        GL.glUniform1fv(u_depth, 1, (self.z_near-self.z_far))
        u_mode = GL.glGetUniformLocation(program, 'u_mode')
        GL.glUniform1i(u_mode, 1)
        u_campos = GL.glGetUniformLocation(program, 'u_campos')
        GL.glUniform3fv(u_campos, 1, self.get_cam_pos())
    
    def load_lights(self, program):
        """ Function doc
        """
        light_pos = GL.glGetUniformLocation(program, 'my_light.position')
        GL.glUniform3fv(light_pos, 1, self.light_position)
        #light_col = GL.glGetUniformLocation(program, 'my_light.color')
        #GL.glUniform3fv(light_col, 1, self.light_color)
        amb_coef = GL.glGetUniformLocation(program, 'my_light.ambient_coef')
        GL.glUniform1fv(amb_coef, 1, self.light_ambient_coef)
        shiny = GL.glGetUniformLocation(program, 'my_light.shininess')
        GL.glUniform1fv(shiny, 1, self.light_shininess)
        intensity = GL.glGetUniformLocation(program, 'my_light.intensity')
        GL.glUniform3fv(intensity, 1, self.light_intensity)
        #spec_col = GL.glGetUniformLocation(program, 'my_light.specular_color')
        #GL.glUniform3fv(spec_col, 1, self.light_specular_color)
        return True
    
    def load_texture(self, program):
        """ Function doc """
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex)
        text = GL.glGetUniformLocation(program, 'textu')
        GL.glUniform1i(text, 0)
        #GL.glActiveTexture(GL.GL_TEXTURE1)
        #GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex[1])
        #GL.glUniform1i(text, 1)
    
    def load_text(self, program):
        """ Function doc """
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.text_texture)
        text = GL.glGetUniformLocation(program, 'textu')
        GL.glUniform1i(text, 0)
    
    def load_antialias_params(self, program):
        """ Function doc """
        a_length = GL.glGetUniformLocation(program, 'antialias_length')
        GL.glUniform1fv(a_length, 1, self.antialias_length)
        bck_col = GL.glGetUniformLocation(program, 'alias_color')
        GL.glUniform3fv(bck_col, 1, self.bckgrnd_color[:3])
    
    def get_viewport_pos(self, x, y):
        """ Function doc """
        px = (2.0*x - self.width)/self.width
        py = (self.height - 2.0*y)/self.height
        return [px, py, self.z_near]
    
    def get_cam_pos(self):
        """ Returns the position of the camera in XYZ coordinates
            The type of data returned is 'numpy.ndarray'.
        """
        modelview = cam.my_glMultiplyMatricesf(self.model_mat, self.view_mat)
        crd_xyz = -1 * np.mat(modelview[:3,:3]) * np.mat(modelview[3,:3]).T
        return crd_xyz.A1
    
    def _update_cam_pos(self):
        """ Function doc """
        self.cam_pos = self.get_cam_pos()
    
    def render(self, area, context):
        """ Function doc """
        if self.gl_programs:
            self.create_gl_programs()
            self.gl_programs = False
        GL.glClearColor(self.bckgrnd_color[0], self.bckgrnd_color[1], self.bckgrnd_color[2], self.bckgrnd_color[3])
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        if self.dots:
            if self.dots_vao is None:
                self.dots_vao, self.dots_vbos, self.dots_elemns = vaos.make_dots(self.gl_program_dots)
                self.queue_draw()
            else:
                self._draw_dots()
        if self.diamonds:
            if self.diamonds_vao is None:
                self.diamonds_vao, self.diamonds_vbos, self.diamonds_elemns = vaos.make_diamonds(self.gl_program_diamonds)
                self.queue_draw()
            else:
                self._draw_diamonds()
        if self.circles:
            if self.circles_vao is None:
                self.circles_vao, self.circles_vbos, self.circles_elemns = vaos.make_circles(self.gl_program_circles)
                self.queue_draw()
            else:
                self._draw_circles()
        if self.lines:
            if self.lines_vao is None:
                self.lines_vao, self.lines_vbos, self.lines_elemns = vaos.make_lines(self.gl_program_lines)
                self.queue_draw()
            else:
                self._draw_lines()
        if self.antialias:
            if self.antialias_vao is None:
                self.antialias_vao, self.antialias_vbos, self.antialias_elemns = vaos.make_antialias(self.gl_program_antialias)
                self.queue_draw()
            else:
                self._draw_antialias()
        if self.pseudospheres:
            if self.pseudospheres_vao is None:
                self.pseudospheres_vao, self.pseudospheres_vbos, self.pseudospheres_elemns = vaos.make_pseudospheres(self.gl_program_pseudospheres)
                self.queue_draw()
            else:
                self._draw_pseudospheres()
        if self.non_bonded:
            if self.non_bonded_vao is None:
                self.non_bonded_vao, self.non_bonded_vbos, self.non_bonded_elemns = vaos.make_non_bonded(self.gl_program_non_bonded)
                self.queue_draw()
            else:
                self._draw_non_bonded()
        if self.geom_cones:
            if self.geom_cones_vao is None:
                self.geom_cones_vao, self.geom_cones_vbos, self.geom_cones_elemns = vaos.make_geom_cones(self.gl_program_geom_cones)
                self.queue_draw()
            else:
                self._draw_geom_cones()
        if self.arrow:
            if self.arrow_vao is None:
                self.arrow_vao, self.arrow_vbos, self.arrow_elemns = vaos.make_arrow(self.gl_program_arrow)
                self.queue_draw()
            else:
                self._draw_arrow()
        if self.select_box:
            if self.select_box_vao is None:
                self.select_box_vao, self.select_box_vbos, self.select_box_elemns = vaos.make_select_box(self.gl_program_select_box)
                self.queue_draw()
            else:
                self._draw_select_box()
        if len(self.edit_points) > 0:
            if self.modified_points:
                self.edit_mode_vao, self.edit_mode_vbos, self.edit_mode_elemns = vaos.make_edit_mode(self.gl_program_edit_mode, self.edit_points)
                self.modified_points = False
            self._draw_edit_mode()
        if self.texture:
            if self.texture_vao is None:
                self.tex = vaos.make_texture_texture()
                self.texture_vao, self.texture_vbos, self.texture_elemns = vaos.make_texture(self.gl_program_texture)
                self.queue_draw()
            else:
                self._draw_texture()
        if self.text:
            if self.text_vao is None:
                self.text_texture = vaos.make_text_texture()
                self.text_vao, self.text_vbos, self.text_elemns = vaos.make_text(self.gl_program_text)
                self.queue_draw()
            else:
                self._draw_text()
        if self.freetype:
            if self.vm_font.vao is None:
                self.vm_font.make_freetype_font()
                self.vm_font.make_freetype_texture(self.gl_program_freetype)
                #self.vm_font.print_all()
                self.queue_draw()
            else:
                self._draw_freetype()
        if self.cylinders:
            if self.cylinders_vao is None:
                self.cylinders_vao, self.cylinders_vbos, self.cylinders_elemns = vaos.make_cylinders(self.gl_program_cylinders)
                self.queue_draw()
            else:
                self._draw_cylinders()
        if self.dots_surface:
            if self.dots_surface_vao is None:
                self.dots_surface_vao, self.dots_surface_vbos, self.dots_surface_elemns = vaos.make_dots_surface(self.gl_program_dots_surface)
                self.queue_draw()
            else:
                self._draw_dots_surface()
        if self.icosahedron:
            if self.icosahedron_vao is None:
                self.icosahedron_vao, self.icosahedron_vbos, self.icosahedron_elemns = vaos.make_icosahedron(self.gl_program_icosahedron)
                self.queue_draw()
            else:
                self._draw_icosahedron()
        if self.sphere:
            if self.sphere_vao is None:
                self.sphere_vao, self.sphere_vbos, self.sphere_elemns = vaos.make_sphere(self.gl_program_sphere)
                self.queue_draw()
            else:
                self._draw_sphere()
        if self.lines_1:
            if self.lines_1_vao is None:
                self.lines_1_vao, self.lines_1_vbos, self.lines_1_elemns = vaos.make_lines(self.gl_program_lines_1)
                self.queue_draw()
            else:
                self._draw_lines_1()
        if self.triangles:
            if self.triangles_vao is None:
                self.triangles_vao, self.triangles_vbos, self.triangles_elemns = vaos.make_cartoon(self.gl_program_triangles)
                self.queue_draw()
            else:
                self._draw_triangles()
        if self.impostor:
            if self.impostor_vao is None:
                self.impostor_vao, self.impostor_vbos, self.impostor_elemns = vaos.make_impostor(self.gl_program_impostor)
                self.queue_draw()
            else:
                self._draw_impostor()
        if self.test:
            if self.test_vao is None:
                self.test_vao, self.test_vbos, self.test_elemns = vaos.make_test(self.gl_program_test)
                self.queue_draw()
            else:
                self._draw_test()
    
    def _draw_dots(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_dots)
        GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        self.load_matrices(self.gl_program_dots)
        GL.glBindVertexArray(self.dots_vao)
        GL.glDrawArrays(GL.GL_POINTS, 0, self.dots_elemns)
        GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_diamonds(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_diamonds)
        self.load_matrices(self.gl_program_diamonds)
        GL.glBindVertexArray(self.diamonds_vao)
        GL.glDrawArrays(GL.GL_POINTS, 0, self.diamonds_elemns)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_circles(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_circles)
        GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        self.load_matrices(self.gl_program_circles)
        GL.glBindVertexArray(self.circles_vao)
        GL.glDrawArrays(GL.GL_POINTS, 0, self.circles_elemns)
        GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_lines(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glLineWidth(10)
        GL.glUseProgram(self.gl_program_lines)
        self.load_matrices(self.gl_program_lines)
        GL.glBindVertexArray(self.lines_vao)
        GL.glDrawElements(GL.GL_LINES, self.lines_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glLineWidth(1)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_antialias(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_antialias)
        self.load_matrices(self.gl_program_antialias)
        self.load_antialias_params(self.gl_program_antialias)
        GL.glBindVertexArray(self.antialias_vao)
        GL.glDrawElements(GL.GL_LINES, self.antialias_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_pseudospheres(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_pseudospheres)
        self.load_matrices(self.gl_program_pseudospheres)
        GL.glBindVertexArray(self.pseudospheres_vao)
        GL.glDrawElements(GL.GL_POINTS, self.pseudospheres_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_non_bonded(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_non_bonded)
        self.load_matrices(self.gl_program_non_bonded)
        GL.glBindVertexArray(self.non_bonded_vao)
        GL.glDrawElements(GL.GL_POINTS, self.non_bonded_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_geom_cones(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_geom_cones)
        self.load_matrices(self.gl_program_geom_cones)
        self.load_lights(self.gl_program_geom_cones)
        GL.glBindVertexArray(self.geom_cones_vao)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.geom_cones_elemns)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_arrow(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_arrow)
        self.load_matrices(self.gl_program_arrow)
        self.load_lights(self.gl_program_arrow)
        GL.glBindVertexArray(self.arrow_vao)
        GL.glDrawElements(GL.GL_TRIANGLES, self.arrow_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_select_box(self):
        """ Function doc """
        #GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glLineWidth(1)
        GL.glUseProgram(self.gl_program_select_box)
        GL.glBindVertexArray(self.select_box_vao)
        GL.glDrawElements(GL.GL_LINE_STRIP, 5, GL.GL_UNSIGNED_INT, None)
        #GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_edit_mode(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_edit_mode)
        self.load_matrices(self.gl_program_edit_mode)
        self.load_lights(self.gl_program_edit_mode)
        GL.glBindVertexArray(self.edit_mode_vao)
        GL.glDrawElements(GL.GL_TRIANGLES, self.edit_mode_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_texture(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_SRC_ALPHA)
        GL.glUseProgram(self.gl_program_texture)
        self.load_matrices(self.gl_program_texture)
        self.load_texture(self.gl_program_texture)
        GL.glBindVertexArray(self.texture_vao)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.texture_elemns)
        GL.glDisable(GL.GL_BLEND)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_text(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_text)
        self.load_matrices(self.gl_program_text)
        self.load_text(self.gl_program_text)
        GL.glBindVertexArray(self.text_vao)
        GL.glDrawElements(GL.GL_POINTS, self.text_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_freetype(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glUseProgram(self.gl_program_freetype)
        self.vm_font.load_matrices(self.gl_program_freetype, np.copy(self.model_mat), self.view_mat, self.proj_mat)
        self.vm_font.load_font_params(self.gl_program_freetype)
        GL.glBindVertexArray(self.vm_font.vao)
        texto = "Hello World!!! :)"
        point = np.array((-2,-1, 0),np.float32)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.vm_font.texture_id)
        for i,c in enumerate(texto):
            c_id = ord(c)
            x = c_id%16
            y = c_id//16-2
            xyz_pos = np.array([point[0]+i*self.vm_font.char_width, point[1], point[2]],np.float32)
            uv_coords = np.array([x*self.vm_font.text_u, y*self.vm_font.text_v, (x+1)*self.vm_font.text_u, (y+1)*self.vm_font.text_v],np.float32)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vm_font.vbos[0])
            GL.glBufferData(GL.GL_ARRAY_BUFFER, xyz_pos.itemsize*len(xyz_pos), xyz_pos, GL.GL_DYNAMIC_DRAW)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vm_font.vbos[1])
            GL.glBufferData(GL.GL_ARRAY_BUFFER, uv_coords.itemsize*len(uv_coords), uv_coords, GL.GL_DYNAMIC_DRAW)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            GL.glDrawArrays(GL.GL_POINTS, 0, 1)
        GL.glDisable(GL.GL_BLEND)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_cylinders(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_cylinders)
        self.load_matrices(self.gl_program_cylinders)
        self.load_lights(self.gl_program_cylinders)
        GL.glBindVertexArray(self.cylinders_vao)
        GL.glDrawElements(GL.GL_LINES, self.cylinders_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_dots_surface(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_dots_surface)
        self.load_matrices(self.gl_program_dots_surface)
        GL.glPointSize(5)
        GL.glBindVertexArray(self.dots_surface_vao)
        GL.glDrawElements(GL.GL_POINTS, self.dots_surface_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glPointSize(1)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_icosahedron(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_icosahedron)
        self.load_matrices(self.gl_program_icosahedron)
        self.load_lights(self.gl_program_cylinders)
        GL.glBindVertexArray(self.icosahedron_vao)
        GL.glDrawElements(GL.GL_POINTS, self.icosahedron_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_sphere(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_sphere)
        self.load_matrices(self.gl_program_sphere)
        self.load_lights(self.gl_program_sphere)
        GL.glBindVertexArray(self.sphere_vao)
        GL.glDrawElements(GL.GL_TRIANGLES, self.sphere_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_lines_1(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glLineWidth(10)
        GL.glUseProgram(self.gl_program_lines_1)
        self.load_matrices(self.gl_program_lines_1)
        GL.glBindVertexArray(self.lines_1_vao)
        GL.glDrawElements(GL.GL_LINES, self.lines_1_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glLineWidth(1)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_triangles(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_triangles)
        self.load_matrices(self.gl_program_triangles)
        self.load_lights(self.gl_program_triangles)
        GL.glBindVertexArray(self.triangles_vao)
        GL.glDrawElements(GL.GL_TRIANGLES, self.triangles_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_impostor(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_impostor)
        # GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        self.load_matrices(self.gl_program_impostor)
        self.load_impostor_params(self.gl_program_impostor)
        self.load_lights(self.gl_program_impostor)
        GL.glBindVertexArray(self.impostor_vao)
        GL.glDrawArrays(GL.GL_POINTS, 0, self.impostor_elemns)
        # GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
        
    def _draw_test(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_test)
        GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        self.load_matrices(self.gl_program_test)
        self.load_test_data(self.gl_program_test)
        GL.glBindVertexArray(self.test_vao)
        GL.glDrawArrays(GL.GL_POINTS, 0, self.test_elemns)
        GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def mouse_pressed(self, widget, event):
        """ Function doc """
        left = event.button == 1
        middle = event.button == 2
        right = event.button == 3
        self.mouse_rotate = left and not (middle or right)
        self.mouse_zoom = right and not (middle or left)
        self.mouse_pan = middle and not (right  or left)
        self.mouse_x = float(event.x)
        self.mouse_y = float(event.y)
        self.drag_pos_x, self.drag_pos_y, self.drag_pos_z = self.get_viewport_pos(self.mouse_x, self.mouse_y)
        self.dragging = False
        if event.button == 1:
            pass
            self.dx = 0.0
            self.dy = 0.0
        if event.button == 2:
            pass
        if event.button == 3:
            pass
    
    def mouse_released(self, widget, event):
        """ Function doc """
        self.mouse_rotate = False
        self.mouse_zoom = False
        self.mouse_pan = False
        if event.button == 1:
            if self.dragging:
                pass
                #if (time.perf_counter()-self.start_time) <= 0.01:
                    #for i in range(10):
                        #self._rotate_view(self.dx, self.dy, self.mouse_x, self.mouse_y)
                        #self.get_window().invalidate_rect(None, False)
                        #self.get_window().process_updates(False)
                        #time.sleep(0.02)
                    #for i in range(1, 18):
                        #self._rotate_view(self.dx/i, self.dy/i, self.mouse_x, self.mouse_y)
                        #self.get_window().invalidate_rect(None, False)
                        #self.get_window().process_updates(False)
                        #time.sleep(0.02)
            else:
                if self.editing:
                    self.edit_draw(event)
                self.dragging = False
        if event.button == 2:
            pass
        if event.button == 3:
            if not self.dragging:
                if self.editing:
                    self.edit_points = []
                    self.queue_draw()
    
    def mouse_motion(self, widget, event):
        """ Function doc """
        x = float(event.x)
        y = float(event.y)
        dx = x - self.mouse_x
        dy = y - self.mouse_y
        if (dx==0 and dy==0):
            return
        self.mouse_x, self.mouse_y = x, y
        changed = False
        if self.mouse_rotate:
            changed = self._rotate_view(dx, dy, x, y)
        elif self.mouse_pan:
            changed = self._pan_view(x, y)
        elif self.mouse_zoom:
            changed = self._zoom_view(dy)
        if changed:
            self._update_cam_pos()
            self.start_time = time.perf_counter()
            self.dx = dx
            self.dy = dy
            self.dragging = True
            self.queue_draw()
        return True
    
    def mouse_scroll(self, widget, event):
        """ Function doc """
        if self.ctrl:
            if event.direction == Gdk.ScrollDirection.UP:
                self.model_mat = cam.my_glTranslatef(self.model_mat, [0.0, 0.0, -self.scroll])
            if event.direction == Gdk.ScrollDirection.DOWN:
                self.model_mat = cam.my_glTranslatef(self.model_mat, [0.0, 0.0, self.scroll])
        else:
            #pos_z = self.get_cam_pos()[2]
            pos_z = self.cam_pos[2]
            if event.direction == Gdk.ScrollDirection.UP:
                self.z_near -= self.scroll
                self.z_far += self.scroll
            if event.direction == Gdk.ScrollDirection.DOWN:
                if (self.z_far-self.scroll) >= (self.min_zfar):
                    if (self.z_far-self.scroll) > (self.z_near+self.scroll):
                        self.z_near += self.scroll
                        self.z_far -= self.scroll
            if (self.z_near >= self.min_znear):
                self.proj_mat = cam.my_glPerspectivef(self.fov, self.var, self.z_near, self.z_far)
            else:
                if self.z_far < (self.min_zfar+self.min_znear):
                    self.z_near -= self.scroll
                    self.z_far = self.min_znear + self.min_zfar
                self.proj_mat = cam.my_glPerspectivef(self.fov, self.var, self.min_znear, self.z_far)
        self.queue_draw()
    
    def _rotate_view(self, dx, dy, x, y):
        """ Function doc """
        angle = math.sqrt(dx**2+dy**2)/float(self.width+1)*36.0*np.linalg.norm(self.cam_pos)
        if self.ctrl:
            if abs(dx) >= abs(dy):
                if (y-self.height/2.0) < 0:
                    rot_mat = cam.my_glRotatef(np.identity(4), angle, [0.0, 0.0, dx])
                else:
                    rot_mat = cam.my_glRotatef(np.identity(4), angle, [0.0, 0.0, -dx])
            else:
                if (x-self.width/2.0) < 0:
                    rot_mat = cam.my_glRotatef(np.identity(4), angle, [0.0, 0.0, -dy])
                else:
                    rot_mat = cam.my_glRotatef(np.identity(4), angle, [0.0, 0.0, dy])
        else:
            rot_mat = cam.my_glRotatef(np.identity(4), angle, [-dy, -dx, 0.0])
        self.model_mat = cam.my_glMultiplyMatricesf(self.model_mat, rot_mat)
        return True
    
    def _pan_view(self, x, y):
        """ Function doc """
        px, py, pz = self.get_viewport_pos(x, y)
        pan_mat = cam.my_glTranslatef(np.identity(4, dtype=np.float32),
            [(px-self.drag_pos_x)*self.z_far/10.0, 
             (py-self.drag_pos_y)*self.z_far/10.0, 
             (pz-self.drag_pos_z)*self.z_far/10.0])
        self.model_mat = cam.my_glMultiplyMatricesf(self.model_mat, pan_mat)
        self.drag_pos_x = px
        self.drag_pos_y = py
        self.drag_pos_z = pz
        return True
    
    def _zoom_view(self, dy):
        """ Function doc """
        delta = (((self.z_far-self.z_near)/2.0)+self.z_near)/200.0
        move_z = dy * delta
        moved_mat = cam.my_glTranslatef(self.view_mat, [0.0, 0.0, move_z])
        moved_pos = cam.get_xyz_coords(moved_mat)
        if moved_pos[2] > 0.101:
            self.view_mat = moved_mat
            self.z_near -= move_z
            self.z_far -= move_z
            if self.z_near >= self.min_znear:
                self.proj_mat = cam.my_glPerspectivef(self.fov, self.var, self.z_near, self.z_far)
            else:
                if self.z_far < (self.min_zfar+self.min_znear):
                    self.z_near += move_z
                    self.z_far = self.min_zfar+self.min_znear
                self.proj_mat = cam.my_glPerspectivef(self.fov, self.var, self.min_znear, self.z_far)
        else:
            pass
        return True
    
    def edit_draw(self, event):
        """ Function doc """
        #self.cam_pos = self.get_cam_pos()
        proj = np.matrix(self.proj_mat)
        view = np.matrix(self.view_mat)
        model = np.matrix(self.model_mat)
        i_proj = proj.I
        i_view = view.I
        i_model = model.I
        i_mvp = i_proj * i_view * i_model
        mod = self.get_viewport_pos(event.x, event.y)
        mod.append(1)
        mod = np.matrix(mod)
        mod = (mod*i_mvp).A1
        mod /= mod[3]
        u_vec = cam.unit_vector(mod[:3] - self.cam_pos)
        v_vec = cam.unit_vector(-self.cam_pos)
        angle = np.radians(cam.get_angle(v_vec, u_vec))
        hypo = cam.get_euclidean(self.cam_pos, [0,0,0]) / np.cos(angle)
        test = u_vec * hypo
        mod = self.cam_pos + test
        self.add_points(mod[:3])
        self.queue_draw()
    
    def add_points(self, point):
        """ Function doc """
        for i in point:
            self.edit_points.append(i)
        self.modified_points = True
        print("Point added")
    
    def save_image(self, filename):
        from PIL import Image
        pixels = GL.glReadPixels(0, 0, self.width, self.height, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (self.width, self.height), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(filename, "png")
        print('Saved image to %s'% (filename))
        # return image

    def key_pressed(self, widget, event):
        """ Function doc """
        k_name = Gdk.keyval_name(event.keyval)
        func = getattr(self, '_pressed_' + k_name, None)
        #print(k_name)
        if func:
            func()
        return True
    
    def key_released(self, widget, event):
        """ Function doc """
        k_name = Gdk.keyval_name(event.keyval)
        func = getattr(self, '_released_' + k_name, None)
        if func:
            func()
        return True
    
    def _pressed_Escape(self):
        Gtk.main_quit()
    
    def _pressed_Control_L(self):
        self.ctrl = True
    
    def _released_Control_L(self):
        self.ctrl = False
    
    def _pressed_Up(self):
        self.model_mat = cam.my_glRotateXf(self.model_mat, 5)
        self.queue_draw()
    
    def _pressed_Down(self):
        self.model_mat = cam.my_glRotateXf(self.model_mat,-5)
        self.queue_draw()
    
    def _pressed_Left(self):
        self.model_mat = cam.my_glRotateYf(self.model_mat, 5)
        self.queue_draw()
    
    def _pressed_Right(self):
        self.model_mat = cam.my_glRotateYf(self.model_mat,-5)
        self.queue_draw()
    
    def _pressed_a(self):
        self.arrow = not self.arrow
        self.queue_draw()
    
    def _pressed_b(self):
        self.select_box = not self.select_box
        self.queue_draw()
    
    def _pressed_c(self):
        self.circles = not self.circles
        self.queue_draw()
    
    def _pressed_d(self):
        self.diamonds = not self.diamonds
        self.queue_draw()
    
    def _pressed_e(self):
        self.editing = not self.editing
        print("Editing mode:", self.editing)
    
    def _pressed_f(self):
        self.non_bonded = not self.non_bonded
        self.queue_draw()
    
    def _pressed_g(self):
        self.dots_surface = not self.dots_surface
        self.queue_draw()
    
    def _pressed_h(self):
        self.lines_1 = not self.lines_1
        self.queue_draw()
    
    def _pressed_i(self):
        self.icosahedron = not self.icosahedron
        self.queue_draw()
    
    def _pressed_j(self):
        pass

    def _pressed_k(self):
        self.antialias = not self.antialias
        self.queue_draw()
    
    def _pressed_l(self):
        self.lines = not self.lines
        self.queue_draw()
    
    def _pressed_m(self):
        print("------------------------------------")
        print(self.model_mat,"<- model matrix")
        print("------------------------------------")
        print(self.view_mat,"<- view matrix")
        print("------------------------------------")
        print(self.proj_mat,"<- projection matrix")
    
    def _pressed_n(self):
        self.geom_cones = not self.geom_cones
        self.queue_draw()
    
    def _pressed_o(self):
        print("------------------------------------")
        print(self.cam_pos,"<- camera position")
        print(np.linalg.norm(self.cam_pos),"<- camera dist to 0")
    
    def _pressed_p(self):
        self.dots = not self.dots
        self.queue_draw()
    
    def _pressed_q(self):
        print("------------------------------------")
        print(self.edit_points,"<- points")
    
    def _pressed_r(self):
        self.freetype = not self.freetype
        self.queue_draw()
    
    def _pressed_s(self):
        self.pseudospheres = not self.pseudospheres
        self.queue_draw()
    
    def _pressed_t(self):
        self.texture = not self.texture
        self.queue_draw()
    
    def _pressed_u(self):
        self.text = not self.text
        self.queue_draw()
    
    def _pressed_v(self):
        self.test = not self.test
        self.queue_draw()
    
    def _pressed_w(self):
        self.sphere = not self.sphere
        self.queue_draw()
    
    def _pressed_x(self):
        import time
        self.save_image("screenshot_{}.bmp".format(time.time()))
    
    def _pressed_y(self):
        self.cylinders = not self.cylinders
        self.queue_draw()
    
    def _pressed_z(self):
        self.triangles = not self.triangles
        self.queue_draw()
    
    def _pressed_1(self):
        self.impostor = not self.impostor
        self.queue_draw()
    

test = MyGLProgram()
wind = Gtk.Window()
wind.add(test)

wind.connect("delete-event", Gtk.main_quit)
wind.connect("key-press-event", test.key_pressed)
wind.connect("key-release-event", test.key_released)
wind.show_all()
Gtk.main()
