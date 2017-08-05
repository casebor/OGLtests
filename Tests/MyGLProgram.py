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
import camera as cam
import shaders as sh
import vaos

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
        self.model_mat = np.identity(4, dtype=np.float32)
        self.view_mat = cam.my_glTranslatef(np.identity(4, dtype=np.float32), [0, 0, -5])
        self.cam_pos = self.get_cam_pos()
        #----------------------------------------------------------------------#
        #self.top = self.z_near * np.degrees(np.tan(np.pi*30/360))
        #self.bottom = -self.top
        #self.right = self.top * self.width / self.height
        #self.left = -self.right
        #self.proj_mat = cam.my_gluFrustumf(self.left, self.right, self.bottom, self.top, self.z_near, self.z_far)
        #----------------------------------------------------------------------#
        self.proj_mat = cam.my_gluPerspectivef(np.identity(4, dtype=np.float32), 30, self.width/self.height, self.z_near, self.z_far)
        self.degrees = np.float32(0)
        self.set_has_depth_buffer(True)
        self.set_has_alpha(True)
        self.gl_programs = True
        self.right = self.width / self.height
        self.left = -self.right
        self.top = 1.0
        self.bottom = -1.0
        self.light_position = np.array([-2.5, 2.5, 3.0],dtype=np.float32)
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
        self.gl_program_spheres = None
        self.spheres_vao = None
        self.spheres_vbos = None
        self.spheres_elemns = None
        self.spheres = False
        self.gl_program_geom_cones = None
        self.geom_cones_vao = None
        self.geom_cones_vbos = None
        self.geom_cones_elemns = None
        self.geom_cones = False
        self.gl_program_sph_cones = None
        self.sph_cones_vao = None
        self.sph_cones_vbos = None
        self.sph_cones_elemns = None
        self.sph_cones = False
        self.gl_program_select_box = None
        self.select_box_vao = None
        self.select_box_vbos = None
        self.select_box_elemns = None
        self.select_box = False
        self.points = []
        self.gl_program_add_points = None
        self.add_points_vao = None
        self.add_points_vbos = None
        self.add_points_elemns = None
    
    def reshape_window(self, widget, width, height):
        """ Function doc """
        self.width = np.float32(width)
        self.height = np.float32(height)
        self.right = self.width / self.height
        self.left = -self.right
        self.proj_mat = cam.my_gluPerspectivef(np.identity(4, dtype=np.float32), 30, self.width/self.height, 0.1, 40.0)
    
    def create_gl_programs(self):
        """ Function doc """
        print('OpenGL version: ',GL.glGetString(GL.GL_VERSION))
        try:
            print('OpenGL major version: ',GL.glGetDoublev(GL.GL_MAJOR_VERSION))
            print('OpenGL minor version: ',GL.glGetDoublev(GL.GL_MINOR_VERSION))
        except:
            print('OpenGL major version not found')
        self.gl_program_diamonds = self.load_shaders(sh.v_shader_diamonds, sh.f_shader_diamonds, sh.g_shader_diamonds)
        self.gl_program_dots = self.load_shaders(sh.v_shader_dots, sh.f_shader_dots)
        self.gl_program_circles = self.load_shaders(sh.v_shader_circles, sh.f_shader_circles)
        self.gl_program_lines = self.load_shaders(sh.v_shader_lines, sh.f_shader_lines, sh.g_shader_lines)
        self.gl_program_spheres = self.load_shaders(sh.v_shader_spheres, sh.f_shader_spheres, sh.g_shader_spheres5)
        self.gl_program_geom_cones = self.load_shaders(sh.v_shader_geom_cones, sh.f_shader_geom_cones)
        self.gl_program_sph_cones = self.load_shaders(sh.v_shader_sph_cones, sh.f_shader_sph_cones)
        self.gl_program_select_box = self.load_shaders(sh.v_shader_select_box, sh.f_shader_select_box)
        self.gl_program_add_points = self.load_shaders(sh.v_shader_add_points, sh.f_shader_add_points)
    
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
        print(modelview, "<= modelview")
        crd_xyz = -1 * np.mat(modelview[:3,:3]) * np.mat(modelview[3,:3]).T
        return crd_xyz.A1
    
    def render(self, area, context):
        """ Function doc """
        if self.gl_programs:
            self.create_gl_programs()
            self.gl_programs = False
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
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
        if self.spheres:
            if self.spheres_vao is None:
                self.spheres_vao, self.spheres_vbos, self.spheres_elemns = vaos.make_spheres(self.gl_program_spheres)
                self.queue_draw()
            else:
                self._draw_spheres()
        if self.geom_cones:
            if self.geom_cones_vao is None:
                self.geom_cones_vao, self.geom_cones_vbos, self.geom_cones_elemns = vaos.make_geom_cones(self.gl_program_geom_cones)
                self.queue_draw()
            else:
                self._draw_geom_cones()
        if self.sph_cones:
            if self.sph_cones_vao is None:
                self.sph_cones_vao, self.sph_cones_vbos, self.sph_cones_elemns = vaos.make_sph_cones(self.gl_program_sph_cones)
                self.queue_draw()
            else:
                self._draw_sph_cones()
        if self.select_box:
            if self.select_box_vao is None:
                self.select_box_vao, self.select_box_vbos, self.select_box_elemns = vaos.make_select_box(self.gl_program_select_box)
                self.queue_draw()
            else:
                self._draw_select_box()
        if len(self.points) > 0:
            #print(self.points)
            self.add_points_vao, self.add_points_vbos, self.add_points_elemns = vaos.make_add_points(self.gl_program_add_points, self.points)
            self._draw_add_points()
    
    def _draw_dots(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_dots)
        self.load_matrices(self.gl_program_dots)
        GL.glBindVertexArray(self.dots_vao)
        GL.glDrawArrays(GL.GL_POINTS, 0, self.dots_elemns)
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
        GL.glLineWidth(5)
        GL.glUseProgram(self.gl_program_lines)
        self.load_matrices(self.gl_program_lines)
        GL.glBindVertexArray(self.lines_vao)
        GL.glDrawElements(GL.GL_LINES, self.lines_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_spheres(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_spheres)
        self.load_matrices(self.gl_program_spheres)
        GL.glBindVertexArray(self.spheres_vao)
        GL.glDrawElements(GL.GL_POINTS, self.spheres_elemns, GL.GL_UNSIGNED_INT, None)
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
    
    def _draw_sph_cones(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_sph_cones)
        self.load_matrices(self.gl_program_sph_cones)
        self.load_lights(self.gl_program_sph_cones)
        GL.glBindVertexArray(self.sph_cones_vao)
        GL.glDrawElements(GL.GL_TRIANGLES, self.sph_cones_elemns, GL.GL_UNSIGNED_INT, None)
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
    
    def _draw_add_points(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_add_points)
        GL.glPointSize(4)
        self.load_matrices(self.gl_program_add_points)
        GL.glBindVertexArray(self.add_points_vao)
        GL.glDrawArrays(GL.GL_POINTS, 0, self.add_points_elemns)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def mouse_pressed(self, widget, event):
        """ Function doc """
        left   = event.button == 1
        middle = event.button == 2
        right  = event.button == 3
        self.mouse_rotate = left   and not (middle or right)
        self.mouse_zoom   = right  and not (middle or left)
        self.mouse_pan    = middle and not (right  or left)
        self.dragging = False
        if event.button == 1:
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
            c_vec = cam.unit_vector(-self.cam_pos)
            angle = np.radians(cam.get_angle(c_vec, u_vec))
            hypo = cam.get_euclidean(self.cam_pos, [0,0,0]) / np.cos(angle)
            test = u_vec * hypo
            mod = self.cam_pos + test
            self.add_points(mod[:3])
            self.queue_draw()
        if event.button == 2:
            pass
        if event.button == 3:
            pass
            self.points = []
            self.queue_draw()
    
    def mouse_released(self, widget, event):
        """ Function doc """
        if event.button == 1:
            pass
        if event.button == 2:
            pass
        if event.button == 3:
            pass
    
    def mouse_scroll(self, widget, event):
        """ Function doc """
        if event.direction == Gdk.ScrollDirection.UP:
            pos = [0,0,1]
        if event.direction == Gdk.ScrollDirection.DOWN:
            pos = [0,0,-1]
        self.view_mat = cam.my_glTranslatef(self.view_mat, pos)
        self.cam_pos = self.get_cam_pos()
        self.queue_draw()
    
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
    
    def _pressed_i(self):
        print("------------------------------------")
        print(self.points,"<- points")
    
    def _pressed_o(self):
        print("------------------------------------")
        print(self.get_cam_pos(),"<- camera position")
    
    def _pressed_m(self):
        print("------------------------------------")
        print(self.model_mat,"<- model matrix")
        print("------------------------------------")
        print(self.view_mat,"<- view matrix")
        print("------------------------------------")
        print(self.proj_mat,"<- projection matrix")
    
    def _pressed_Left(self):
        self.model_mat = cam.my_glRotateYf(self.model_mat, 10)
        self.cam_pos = self.get_cam_pos()
        self.queue_draw()
    
    def _pressed_Right(self):
        self.model_mat = cam.my_glRotateYf(self.model_mat, -10)
        self.cam_pos = self.get_cam_pos()
        self.queue_draw()
    
    def _pressed_Up(self):
        self.model_mat = cam.my_glRotateXf(self.model_mat, 10)
        self.cam_pos = self.get_cam_pos()
        self.queue_draw()
    
    def _pressed_Down(self):
        self.model_mat = cam.my_glRotateXf(self.model_mat, -10)
        self.cam_pos = self.get_cam_pos()
        self.queue_draw()
    
    def _pressed_p(self):
        self.dots = not self.dots
        self.queue_draw()
    
    def _pressed_d(self):
        self.diamonds = not self.diamonds
        self.queue_draw()
    
    def _pressed_c(self):
        self.circles = not self.circles
        self.queue_draw()
    
    def _pressed_l(self):
        self.lines = not self.lines
        self.queue_draw()
    
    def _pressed_s(self):
        self.spheres = not self.spheres
        self.queue_draw()
    
    def _pressed_n(self):
        self.geom_cones = not self.geom_cones
        self.queue_draw()
    
    def _pressed_q(self):
        self.sph_cones = not self.sph_cones
        self.queue_draw()
    
    def _pressed_b(self):
        self.select_box = not self.select_box
        self.queue_draw()
    
    def add_points(self, point):
        """ Function doc """
        for i in point:
            self.points.append(i)
    
    

test = MyGLProgram()
wind = Gtk.Window()
wind.add(test)

wind.connect("delete-event", Gtk.main_quit)
wind.connect("key-press-event", test.key_pressed)
wind.connect("key-release-event", test.key_released)
wind.show_all()
Gtk.main()
