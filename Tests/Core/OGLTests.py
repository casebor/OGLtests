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
import OGLshaders as sh
import VisMolFont as vmf
import vaos
import time
import matrix_operations as mop
from glstuff import GLCamera
from glstuff import VismolFont

import gi
gi.require_version("Gtk", "3.0")
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
        self.model_mat = np.identity(4, dtype=np.float32)
        self.glcamera = GLCamera(fov=30.0, var=self.width / self.height,
                                 pos=np.array([0,0,5], dtype=np.float32))
        self.set_has_depth_buffer(True)
        self.set_has_alpha(True)
        
        self.model_mat = np.identity(4, dtype=np.float32) # Not sure if this is used :S
        # self.view_mat = cam.my_glTranslatef(np.identity(4, dtype=np.float32), [0, 0, -5])
        self.dist_cam_zrp = np.linalg.norm(self.glcamera.get_position())
        self.gl_programs = True
        self.right = self.width / self.height
        self.left = -self.right
        self.top = 1.0
        self.bottom = -1.0
        self.scroll = 0.3
        self.edit_points = []
        self.editing = False
        self.dragging = False
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
        #self.bckgrnd_color = np.array([1.0, 1.0, 1.0, 1.0],dtype=np.float32)
        self.light_position = np.array([-2.5, 2.5, 3.0],dtype=np.float32)
        self.light_color = np.array([1.0, 1.0, 1.0, 1.0],dtype=np.float32)
        self.light_ambient_coef = 0.4
        self.light_shininess = 5.5
        self.light_intensity = np.array([0.6, 0.6, 0.6],dtype=np.float32)
        self.light_specular_color = np.array([1.0, 1.0, 1.0],dtype=np.float32)
        # Here are the test programs and flags
        self.gl_program_impostor_sph = None
        self.impostor_sph_vao = None
        self.impostor_sph_vbos = None
        self.impostor_sph_elemns = None
        self.impostor_sph = False
        # Here are the test programs and flags
        self.gl_program_cubes = None
        self.cubes_vao = None
        self.cubes_vbos = None
        self.cubes_elemns = None
        self.cubes = False
        # Here are the test programs and flags
        self.gl_program_impostor_cyl = None
        self.impostor_cyl_vao = None
        self.impostor_cyl_vbos = None
        self.impostor_cyl_elemns = None
        self.impostor_cyl = False
        # Here are the test programs and flags
        self.gl_program_glumpy = None
        self.glumpy_vao = None
        self.glumpy_vbos = None
        self.glumpy_elemns = None
        self.glumpy = False
        # Here are the test programs and flags
        self.gl_program_text = None
        self.text = False
        self.vm_font = VismolFont(font_name="Arial", color=[0,1,1])
        # Here are the test programs and flags
        self.gl_program_cartoon = None
        self.cartoon_vao = None
        self.cartoon_vbos = None
        self.cartoon_elemns = None
        self.cartoon = False
        # Here are the test programs and flags
        self.gl_program_texture = None
        self.texture_texture = None
        self.texture_vbos = None
        self.texture_elemns = None
        self.texture = False
    
    def reshape_window(self, widget, width, height):
        """ Function doc """
        self.width = np.float32(width)
        self.height = np.float32(height)
        self.right = self.width / self.height
        self.left = -self.right
        self.glcamera.viewport_aspect_ratio = self.width / self.height
        _proj_mat = mop.my_glPerspectivef(self.glcamera.field_of_view,
                                          self.glcamera.viewport_aspect_ratio,
                                          self.glcamera.z_near, self.glcamera.z_far)
        self.glcamera.set_projection_matrix(_proj_mat)
    
    def _mouse_pos(self, x, y):
        """
        Use the ortho projection and viewport information
        to map from mouse co-ordinates back into world
        co-ordinates
        """
        px = x / self.width
        py = y / self.height
        px = self.left + px * (self.right - self.left)
        py = self.top + py * (self.bottom - self.top)
        pz = self.glcamera.z_near
        return px, py, pz
    
    def mouse_pressed(self, widget, event):
        """ Function doc """
        left = np.int32(event.button) == 1
        middle = np.int32(event.button) == 2
        right = np.int32(event.button) == 3
        self.mouse_rotate = left and not (middle or right)
        self.mouse_zoom = right and not (middle or left)
        self.mouse_pan = middle and not (right  or left)
        self.mouse_x = np.float32(event.x)
        self.mouse_y = np.float32(event.y)
        self.drag_pos_x, self.drag_pos_y, self.drag_pos_z = self._mouse_pos(self.mouse_x, self.mouse_y)
        self.dragging = False
        if left:
            self.dx = 0.0
            self.dy = 0.0
        if middle:
            pass
        if right:
            pass
    
    def mouse_released(self, widget, event):
        """ Function doc """
        left = np.int32(event.button) == 1
        middle = np.int32(event.button) == 2
        right = np.int32(event.button) == 3
        self.mouse_rotate = False
        self.mouse_zoom = False
        self.mouse_pan = False
        if self.dragging:
            return
        if left:
            self.button = 1
        if middle:
            self.button = 2
        if right:
            self.button = 3
    
    def mouse_motion(self, widget, event):
        """ Function doc """
        x = np.float32(event.x)
        y = np.float32(event.y)
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
            self.dragging = True
            self.queue_draw()
        return True
    
    def mouse_scroll(self, widget, event):
        """ Function doc """
        up = event.direction == Gdk.ScrollDirection.UP
        down = event.direction == Gdk.ScrollDirection.DOWN
        if self.ctrl:
            if up:
                self.model_mat = mop.my_glTranslatef(self.model_mat, np.array([0.0, 0.0, -self.scroll]))
            if down:
                self.model_mat = mop.my_glTranslatef(self.model_mat, np.array([0.0, 0.0, self.scroll]))
        else:
            pos_z = self.glcamera.get_position()[2]
            if up:
                self.glcamera.z_near -= self.scroll
                self.glcamera.z_far += self.scroll
            if down:
                if (self.glcamera.z_far-self.scroll) >= (self.glcamera.min_zfar):
                    if (self.glcamera.z_far-self.scroll) > (self.glcamera.z_near+self.scroll+0.005):
                        self.glcamera.z_near += self.scroll
                        self.glcamera.z_far -= self.scroll
            if (self.glcamera.z_near >= self.glcamera.min_znear):
                self.glcamera.set_projection_matrix(mop.my_glPerspectivef(self.glcamera.field_of_view,
                        self.glcamera.viewport_aspect_ratio, self.glcamera.z_near, self.glcamera.z_far))
            else:
                if self.glcamera.z_far < (self.glcamera.min_zfar+self.glcamera.min_znear):
                    self.glcamera.z_near -= self.scroll
                    self.glcamera.z_far = self.glcamera.min_clip + self.glcamera.min_znear
                self.glcamera.set_projection_matrix(mop.my_glPerspectivef(self.glcamera.field_of_view,
                                                    self.glcamera.viewport_aspect_ratio,
                                                    self.glcamera.min_znear, self.glcamera.z_far))
        self.queue_draw()
    
    def _rotate_view(self, dx, dy, x, y):
        """ Function doc """
        angle = np.sqrt(dx**2 + dy**2) / (self.width + 1) * 180.0
        if self.ctrl:
            if abs(dx) >= abs(dy):
                if (y - self.height / 2.0) < 0:
                    rot_mat = mop.my_glRotatef(np.identity(4), angle, np.array([0.0, 0.0, dx]))
                else:
                    rot_mat = mop.my_glRotatef(np.identity(4), angle, np.array([0.0, 0.0, -dx]))
            else:
                if (x - self.width / 2.0) < 0:
                    rot_mat = mop.my_glRotatef(np.identity(4), angle, np.array([0.0, 0.0, -dy]))
                else:
                    rot_mat = mop.my_glRotatef(np.identity(4), angle, np.array([0.0, 0.0, dy]))
        else:
            rot_mat = mop.my_glRotatef(np.identity(4), angle, np.array([-dy, -dx, 0.0]))
        self.model_mat = mop.my_glMultiplyMatricesf(self.model_mat, rot_mat)
        return True
    
    def _pan_view(self, x, y):
        """ Function doc """
        px, py, pz = self._mouse_pos(x, y)
        pan_mat = mop.my_glTranslatef(np.identity(4, dtype=np.float32), np.array(
                                    [(px - self.drag_pos_x) * self.glcamera.z_far / 10.0,
                                     (py - self.drag_pos_y) * self.glcamera.z_far / 10.0,
                                     (pz - self.drag_pos_z) * self.glcamera.z_far / 10.0]))
        self.model_mat = cam.my_glMultiplyMatricesf(self.model_mat, pan_mat)
        self.zero_reference_point = mop.get_xyz_coords(self.model_mat)
        self.drag_pos_x = px
        self.drag_pos_y = py
        self.drag_pos_z = pz
        return True
    
    def _zoom_view(self, dy):
        """ Function doc """
        delta = (((self.glcamera.z_far-self.glcamera.z_near)/2.0)+self.glcamera.z_near)/200.0
        move_z = dy * delta
        moved_mat = mop.my_glTranslatef(self.glcamera.view_matrix, np.array([0.0, 0.0, move_z]))
        moved_pos = mop.get_xyz_coords(moved_mat)
        if moved_pos[2] > 0.101:
            self.glcamera.set_view_matrix(moved_mat)
            self.glcamera.z_near -= move_z
            self.glcamera.z_far -= move_z
            if self.glcamera.z_near >= self.glcamera.min_znear:
                self.glcamera.set_projection_matrix(mop.my_glPerspectivef(self.glcamera.field_of_view, 
                                                    self.glcamera.viewport_aspect_ratio,
                                                    self.glcamera.z_near, self.glcamera.z_far))
            else:
                if self.glcamera.z_far < (self.glcamera.min_zfar+self.glcamera.min_znear):
                    self.glcamera.z_near += move_z
                    self.glcamera.z_far = self.glcamera.min_zfar+self.glcamera.min_znear
                self.glcamera.set_projection_matrix(mop.my_glPerspectivef(self.glcamera.field_of_view, 
                                                    self.glcamera.viewport_aspect_ratio,
                                                    self.glcamera.min_znear, self.glcamera.z_far))
            self.glcamera.update_fog()
            self.dist_cam_zrp += -move_z
            return True
        return False
    
    def create_gl_programs(self):
        """ Function doc """
        print("OpenGL version: ",GL.glGetString(GL.GL_VERSION))
        try:
            print("OpenGL major version: ",GL.glGetDoublev(GL.GL_MINOR_VERSION))
            print("OpenGL minor version: ",GL.glGetDoublev(GL.GL_MAJOR_VERSION))
        except:
            print("OpenGL major version not found")
        self.gl_program_cubes = self.load_shaders(sh.v_cubes, sh.f_cubes, sh.g_cubes)
        self.gl_program_glumpy = self.load_shaders(sh.v_glumpy, sh.f_glumpy)
        self.gl_program_impostor_sph = self.load_shaders(sh.v_impostor_sph, sh.f_impostor_sph, sh.g_impostor_sph)
        self.gl_program_impostor_cyl = self.load_shaders(sh.v_impostor_cyl, sh.f_impostor_cyl, sh.g_impostor_cyl)
        # self.gl_program_text = self.load_shaders(sh.v_text, sh.f_text)
        self.gl_program_cartoon = self.load_shaders(sh.v_cartoon, sh.f_cartoon)
        self.gl_program_texture = self.load_shaders(sh.v_texture, sh.f_texture)
        self.gl_program_text = self.load_shaders(sh.v_diamonds, sh.f_diamonds, sh.g_diamonds)
    
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
        model = GL.glGetUniformLocation(program, "model_mat")
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, self.model_mat)
        view = GL.glGetUniformLocation(program, "view_mat")
        GL.glUniformMatrix4fv(view, 1, GL.GL_FALSE, self.glcamera.view_matrix)
        proj = GL.glGetUniformLocation(program, "proj_mat")
        GL.glUniformMatrix4fv(proj, 1, GL.GL_FALSE, self.glcamera.projection_matrix)
    
    def load_lights(self, program):
        """ Function doc
        """
        light_pos = GL.glGetUniformLocation(program, "my_light.position")
        GL.glUniform3fv(light_pos, 1, self.light_position)
        #light_col = GL.glGetUniformLocation(program, "my_light.color")
        #GL.glUniform3fv(light_col, 1, self.light_color)
        amb_coef = GL.glGetUniformLocation(program, "my_light.ambient_coef")
        GL.glUniform1fv(amb_coef, 1, self.light_ambient_coef)
        shiny = GL.glGetUniformLocation(program, "my_light.shininess")
        GL.glUniform1fv(shiny, 1, self.light_shininess)
        intensity = GL.glGetUniformLocation(program, "my_light.intensity")
        GL.glUniform3fv(intensity, 1, self.light_intensity)
        #spec_col = GL.glGetUniformLocation(program, "my_light.specular_color")
        #GL.glUniform3fv(spec_col, 1, self.light_specular_color)
        return True
    
    def load_texture(self, program):
        """ Function doc """
        # GL.glActiveTexture(GL.GL_TEXTURE0)
        # GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_texture)
        # text = GL.glGetUniformLocation(program, "textu")
        # GL.glUniform1i(text, 0)
        #GL.glActiveTexture(GL.GL_TEXTURE1)
        #GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex[1])
        #GL.glUniform1i(text, 1)
        # GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_texture)
        text = GL.glGetUniformLocation(program, "font_texture")
        GL.glUniform1i(text, 0)
        gl_color = GL.glGetUniformLocation(program, "font_color")
        GL.glUniform3fv(gl_color, 1, [1.0,0.0,0.5])
    
    def load_antialias_params(self, program):
        """ Function doc """
        a_length = GL.glGetUniformLocation(program, "antialias_length")
        GL.glUniform1fv(a_length, 1, self.antialias_length)
        bck_col = GL.glGetUniformLocation(program, "alias_color")
        GL.glUniform3fv(bck_col, 1, self.bckgrnd_color[:3])
    
    def get_viewport_pos(self, x, y):
        """ Function doc """
        px = (2.0*x - self.width)/self.width
        py = (self.height - 2.0*y)/self.height
        return [px, py, self.glcamera.z_near]
    
    def render(self, area, context):
        """ Function doc """
        if self.gl_programs:
            self.create_gl_programs()
            self.gl_programs = False
        GL.glClearColor(self.bckgrnd_color[0], self.bckgrnd_color[1], self.bckgrnd_color[2], self.bckgrnd_color[3])
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        if self.impostor_sph:
            if self.impostor_sph_vao is None:
                self.impostor_sph_vao, self.impostor_sph_vbos, self.impostor_sph_elemns = vaos.make_impostor_sph(self.gl_program_impostor_sph)
                self.queue_draw()
            else:
                self._draw_impostor_sph()
        if self.cubes:
            if self.cubes_vao is None:
                self.cubes_vao, self.cubes_vbos, self.cubes_elemns = vaos.make_cubes(self.gl_program_cubes)
                self.queue_draw()
            else:
                self._draw_cubes()
        if self.impostor_cyl:
            if self.impostor_cyl_vao is None:
                self.impostor_cyl_vao, self.impostor_cyl_vbos, self.impostor_cyl_elemns = vaos.make_impostor_cyl(self.gl_program_impostor_cyl)
                self.queue_draw()
            else:
                self._draw_impostor_cyl()
        if self.glumpy:
            if self.glumpy_vao is None:
                self.glumpy_vao, self.glumpy_vbos, self.glumpy_elemns = vaos.make_glumpy(self.gl_program_glumpy)
                self.queue_draw()
            else:
                self._draw_glumpy()
        if self.cartoon:
            if self.cartoon_vao is None:
                self.cartoon_vao, self.cartoon_vbos, self.cartoon_elemns = vaos.make_cartoon(self.gl_program_cartoon)
                self.queue_draw()
            else:
                self._draw_cartoon()
        if self.texture:
            if self.texture_texture is None:
                # self.texture_texture = vaos.make_texture_OGL()
                # self.texture_vao, self.texture_vbos, self.texture_elemns = vaos.make_texture_coords(self.gl_program_texture)
                self.texture_texture, self.texture_vao, self.texture_vbos = vaos.make_texture_OGL(self.gl_program_texture)
                self.queue_draw()
            else:
                self._draw_texture()
        if self.text:
            if self.vm_font.vao is None:
                self.vm_font._load_font_data()
                self.vm_font.make_font_atlas(self.gl_program_text)
                self.queue_draw()
            else:
                self._draw_text()
    
    def _draw_impostor_sph(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_impostor_sph)
        GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        self.load_matrices(self.gl_program_impostor_sph)
        self.load_lights(self.gl_program_impostor_sph)
        
        xyz_coords = self.glcamera.get_modelview_position(self.model_mat)
        # print(self.glcamera.get_position(), xyz_coords)
        u_campos = GL.glGetUniformLocation(self.gl_program_impostor_sph, "u_campos")
        GL.glUniform3fv(u_campos, 1, xyz_coords)
        
        GL.glBindVertexArray(self.impostor_sph_vao)
        GL.glDrawArrays(GL.GL_POINTS, 0, self.impostor_sph_elemns)
        GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_cubes(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_cubes)
        self.load_matrices(self.gl_program_cubes)
        GL.glBindVertexArray(self.cubes_vao)
        GL.glDrawElements(GL.GL_POINTS, self.cubes_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_impostor_cyl(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_impostor_cyl)
        GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        self.load_matrices(self.gl_program_impostor_cyl)
        self.load_lights(self.gl_program_impostor_cyl)
        
        xyz_coords = self.glcamera.get_modelview_position(self.model_mat)
        u_campos = GL.glGetUniformLocation(self.gl_program_impostor_cyl, "u_campos")
        GL.glUniform3fv(u_campos, 1, xyz_coords)
        
        GL.glBindVertexArray(self.impostor_cyl_vao)
        GL.glDrawElements(GL.GL_LINES, self.impostor_cyl_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_glumpy(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        GL.glUseProgram(self.gl_program_glumpy)
        self.load_matrices(self.gl_program_glumpy)
        self.load_lights(self.gl_program_glumpy)
        xyz_coords = self.glcamera.get_modelview_position(self.model_mat)
        u_campos = GL.glGetUniformLocation(self.gl_program_glumpy, "u_campos")
        GL.glUniform3fv(u_campos, 1, xyz_coords)
        GL.glBindVertexArray(self.glumpy_vao)
        GL.glDrawElements(GL.GL_POINTS, self.glumpy_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_cartoon(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_cartoon)
        self.load_matrices(self.gl_program_cartoon)
        self.load_lights(self.gl_program_cartoon)
        GL.glBindVertexArray(self.cartoon_vao)
        GL.glDrawElements(GL.GL_TRIANGLES, self.cartoon_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def _draw_text(self):
        """ Function doc """
        self.vm_font.render_text(self.gl_program_text, self.model_mat, self.glcamera.view_matrix,
                                 self.glcamera.projection_matrix,
                                 ["Hello-", "World"], np.zeros([2,3], dtype=np.float32))
    
    def _draw_texture(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glUseProgram(self.gl_program_texture)
        self.load_matrices(self.gl_program_texture)
        self.load_texture(self.gl_program_texture)
        GL.glBindVertexArray(self.texture_vao)
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_texture)
        vaos.fill_texture_buffers(self.gl_program_texture, self.texture_vbos)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
        
        GL.glDisable(GL.GL_BLEND)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def edit_draw(self, event):
        """ Function doc """
        #self.glcamera.get_position() = self.get_cam_pos()
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
        u_vec = cam.unit_vector(mod[:3] - self.glcamera.get_position())
        v_vec = cam.unit_vector(-self.glcamera.get_position())
        angle = np.radians(cam.get_angle(v_vec, u_vec))
        hypo = cam.get_euclidean(self.glcamera.get_position(), [0,0,0]) / np.cos(angle)
        test = u_vec * hypo
        mod = self.glcamera.get_position() + test
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
        print("Saved image to %s"% (filename))
        # return image

    def key_pressed(self, widget, event):
        """ Function doc """
        k_name = Gdk.keyval_name(event.keyval)
        func = getattr(self, "_pressed_" + k_name, None)
        #print(k_name)
        if func:
            func()
        return True
    
    def key_released(self, widget, event):
        """ Function doc """
        k_name = Gdk.keyval_name(event.keyval)
        func = getattr(self, "_released_" + k_name, None)
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
    
    def _pressed_q(self):
        self.cubes = not self.cubes
        self.queue_draw()
    
    def _pressed_i(self):
        self.impostor_sph = not self.impostor_sph
        self.queue_draw()
    
    def _pressed_y(self):
        self.impostor_cyl = not self.impostor_cyl
        self.queue_draw()
    
    def _pressed_g(self):
        self.glumpy = not self.glumpy
        self.queue_draw()
    
    def _pressed_c(self):
        self.cartoon = not self.cartoon
        self.queue_draw()
    
    def _pressed_t(self):
        self.texture = not self.texture
        self.queue_draw()
    
    def _pressed_w(self):
        self.text = not self.text
        self.queue_draw()
    
    def _pressed_Up(self):
        self.vm_font.font_scale += 1
        self.vm_font.modified = True
        self.queue_draw()
    
    def _pressed_Down(self):
        self.vm_font.font_scale -= 1
        self.vm_font.modified = True
        self.queue_draw()
    
    def _pressed_m(self):
        print("------------------------------------")
        print(self.model_mat,"<- model matrix")
        print("------------------------------------")
        print(self.glcamera.view_matrix,"<- view matrix")
        print("------------------------------------")
        print(self.glcamera.projection_matrix,"<- projection matrix")
    
    def _pressed_o(self):
        print("------------------------------------")
        print(self.glcamera.get_position(),"<- camera position")
        print(np.linalg.norm(self.glcamera.get_position()),"<- camera dist to 0")

test = MyGLProgram()
wind = Gtk.Window()
wind.add(test)

wind.connect("delete-event", Gtk.main_quit)
wind.connect("key-press-event", test.key_pressed)
wind.connect("key-release-event", test.key_released)
wind.show_all()
Gtk.main()
