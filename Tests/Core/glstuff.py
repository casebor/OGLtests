#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  glstuff.py
#  
#  Copyright 2022 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
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
import freetype as ft
import matrix_operations as mop
from OpenGL import GL
from dataclasses import dataclass


class GLCamera():
    """ The GLCamera object creates a "camera" to be used in OpenGL.
        It automatically creates a viewing and projection matrices with the
        values defined in the constructor.
    """
    
    def __init__ (self, fov=30.0, var=(4.0 / 3.0), pos=np.array([0,0,10], dtype=np.float32),
                  zrp=np.array([0,0,0], dtype=np.float32)):
        """ Depending of the distance from the camera position to a defined
            reference point, it creates different clipping planes (this function
            could be improved, but will work for now).
            
            Input parameters:
                fov -- Specifies the field of view angle, in degrees, in the
                       Y direction.
                var -- Specifies the aspect ratio that determines the field of
                       view in the x direction. The aspect ratio is the ratio
                       of x (width) to y (height).
                pos -- The position in world coordinates of the camera.
                zrp -- The zero reference point defined for rotation functions.
            
            Automatically generates:
                z_near -- Specifies the distance from the viewer to the near
                          clipping plane (always positive).
                z_far -- Specifies the distance from the viewer to the far
                         clipping plane (always positive).
                fog_start -- Specifies the beggining of the fog effect (always
                             positive and lower than z_far).
                fog_end -- Specifies the end of the fog effect (always positive
                           and preferable equal to z_far).
                view_matrix -- The viewing matrix used in the render by shaders.
                projection_matrix -- The projection matrix used in the render
                                     by shaders.
        """
        self.field_of_view = np.float32(fov)
        self.viewport_aspect_ratio = np.float32(var)
        self.zero_reference_point = np.array(zrp, dtype=np.float32)
        self.max_vertical_angle = 85.0  # must be less than 90 to avoid gimbal lock
        self.horizontal_angle = 0.0
        self.vertical_angle = 0.0
        self.min_znear = 0.1
        self.min_zfar = 9.0
        dist = np.linalg.norm(pos - zrp)
        if dist <= 10.0:
            self.z_near = dist - 3.0
            self.z_far = dist + 3.0
        elif dist <= 20.0:
            self.z_near = dist - 6.0
            self.z_far = dist + 6.0
        elif dist <= 40.0:
            self.z_near = dist - 9.0
            self.z_far = dist + 9.0
        elif dist <= 80.0:
            self.z_near = dist - 12.0
            self.z_far = dist + 12.0
        else:
            self.z_near = dist - 15.0
            self.z_far = dist + 15.0
        
        #testing
        #self.z_near = 0.1
        #self.z_far = 100
        self.fog_end = self.z_far 
        self.fog_start = self.fog_end - self.min_zfar 
        self.view_matrix = self._get_view_matrix(pos)
        self.projection_matrix = self._get_projection_matrix()
    
    def _get_view_matrix(self, position):
        """ Creates the view matrix, i.e. the matrix with the position and
            orientation of the camera used in OpenGL.
            First creates a translation matrix at the position defined by the
            "position" argument, then creates a orientation matrix initially
            with the vertical angle, then the horizontal angle is applied to
            this matrix. Finally the multiplication of translation x orientation
            is returned as the view matrix.
            
            Input parameters:
                position -- a numpy array of size 3 and ndim of 1 containing
                            the camera's position in XYZ coordinates.
            
            Returns:
                view -- a numpy array of size 16 and ndim of 2 containing the
                        information for the camera's position and orientation.
        """
        trans = mop.my_glTranslatef(np.identity(4,dtype=np.float32), -position)
        orient = mop.my_glRotatef(np.identity(4,dtype=np.float32), self.vertical_angle, np.array([1,0,0]))
        orient = mop.my_glRotatef(orient, self.horizontal_angle, np.array([0,1,0]))
        view = mop.my_glMultiplyMatricesf(trans, orient)
        return view
    
    def _get_projection_matrix(self):
        """ Creates the projection matrix using the parameters supplied in the
            constructor of the class. This function creates a perspective with
            a defined field of view, viewport aspect ratio, near and far depth
            clipping planes.
            
            Returns:
                persp -- a numpy array of size 16 and ndim of 2, containing the
                         information for the camera's field and depth view.
        """
        assert(self.field_of_view>0.0 and self.field_of_view<180.0)
        assert(self.z_near>0.0)
        assert(self.z_near<self.z_far)
        assert(self.viewport_aspect_ratio>0.0)
        persp = mop.my_glPerspectivef(self.field_of_view,self.viewport_aspect_ratio,self.z_near,self.z_far)
        return persp
    
    def get_position(self):
        """ Returns the x, y, z position of the camera in 
            absolute coordinates.
        """
        return mop.get_xyz_coords(self.view_matrix)
    
    def get_modelview_position(self, model_matrix):
        modelview = mop.my_glMultiplyMatricesf(model_matrix, self.view_matrix)
        crd_xyz = -1 * np.mat(modelview[:3,:3]) * np.mat(modelview[3,:3]).T
        return crd_xyz.A1
    
    def _normalize_angles(self):
        """ DEPRECATED FUNCTION??? SEEMS TO NOT BE USED ANYWHERE
        """
        self.horizontal_angle = self.horizontal_angle % 360.0
        if self.horizontal_angle<0:
            self.horizontal_angle += 360.0
        if self.vertical_angle>self.max_vertical_angle:
            self.vertical_angle = self.max_vertical_angle
        elif self.vertical_angle<-self.max_vertical_angle:
            self.vertical_angle = -self.max_vertical_angle
    
    def add_orientation_angles(self, h_angle, v_angle):
        """ DEPRECATED FUNCTION??? SEEMS TO NOT BE USED ANYWHERE
        """
        self.horizontal_angle += h_angle
        self.vertical_angle += v_angle
        self._normalize_angles()
        return True
    
    def look_at(self, target):
        """ DEPRECATED FUNCTION??? SEEMS TO NOT BE USED ANYWHERE
        """
        position = self.get_position()
        assert(position[0]!=target[0] and
               position[1]!=target[1] and
               position[2]!=target[2])
        direction = target - position
        direction /= np.linalg.norm(direction)
        self.vertical_angle = -np.asin(direction[1])*180/np.pi
        self.horizontal_angle = -(np.atan2(-direction[0], -direction[2])*180/np.pi)
        self._normalize_angles()
        return True
    
    def get_proj_view_matrix(self):
        """ Returns:
                proview -- a numpy array of size 16 and ndim of 2, containing
                           the information for the camera's projection-view
                           matrix.
        """
        proview = mop.my_glMultiplyMatricesf(self.get_projection_matrix(), self.get_view_matrix())
        return proview
    
    def set_view_matrix(self, new_view_matrix):
        """ Sets a new matrix as view matrix for the camera.
            
            Input parameters:
                new_view_matrix -- a numpy array of size 16 and ndim of 2
                                   containing the new view matrix.
            
            Returns:
                True
        """
        self.view_matrix = new_view_matrix
        return True
    
    def set_projection_matrix(self, new_proj_matrix):
        """ Sets a new matrix as projection matrix for the camera.
            
            Input parameters:
                new_proj_matrix -- a numpy array of size 16 and ndim of 2
                                   containing the new projection matrix.
            
            Returns:
                True
        """
        self.projection_matrix = new_proj_matrix
        return True
    
    def update_projection(self):
        """ Updates the projection matrix. If you change any parameter of the
            camera, you should use this function right after so the changes can
            be applied.
            
            Returns:
                True
        """
        self.projection_matrix = self._get_projection_matrix()
        return True
    
    def update_fog(self):
        """ Updates automatically the fog. This function was created to avoid
            errors when the fog values were changed manually, this way, the fog
            start and end will always have constant values. If you want to
            expand or decrease the fog distance, change the self.min_zfar
            instead of changing this function.
            
            Returns:
                True
        """
        self.fog_end = self.z_far
        self.fog_start = self.fog_end - self.min_zfar 
        return True
    
    def print_parms(self):
        """ Prints camera parameters in the terminal. Method created only for
            debugging purposes. It will come out in the final distribution?
        """
        print("######## GLCAMERA PARAMETERS ########")
        print("<= z_near    =>",self.z_near)
        print("<= z_far     =>",self.z_far)
        print("<= fog_start =>",self.fog_start)
        print("<= fog_end   =>",self.fog_end)
        print("<= position  =>",self.get_position())
        print("######## GLCAMERA PARAMETERS ########")
        return True
    
    def print_matrices(self):
        """ Prints camera matrices in the terminal. Method created only for
            debugging purposes. It will come out in the final distribution?
        """
        print("######## GLCAMERA MATRICES ########")
        print("<= view_matrix =>", self.view_matrix)
        print("<= projection_matrix =>", self.projection_matrix)
        print("######## GLCAMERA MATRICES ########")
        return True


@dataclass()
class CharsInfo:
    ax: np.float32
    ay: np.float32
    bw: np.float32
    bh: np.float32
    bl: np.float32
    bt: np.float32
    tx: np.float32

@dataclass()
class Point:
    x: np.float32
    y: np.float32
    s: np.float32
    t: np.float32


class VismolFont():
    """ VisMolFont stores the data created using the freetype python binding
        library, such as filename, character width, character height, character
        resolution, font color, etc.
    """
    
    def __init__ (self, font_file="VeraMono.ttf", char_res=64, c_w=2, c_h=3, color=[1,1,1,1]):
        """ Class initialiser
        """
        self.font_file = font_file
        self.char_res = char_res
        self.char_width = c_w
        self.char_height = c_h
        self.offset = np.array([c_w/2.0,c_h/2.0],dtype=np.float32)
        self.color = np.array(color,dtype=np.float32)
        self.face = None
        
        self.font_buffer = None
        self.texture_id = None
        self.text_u = None
        self.text_v = None
        self.vao = None
        self.vbos = None
    
    def make_freetype_font(self, program):
        """ Function doc
        """
        self.face = ft.Face(self.font_file)
        self.face.set_pixel_sizes(0, self.char_height)
        self.glyph = self.face.glyph
        roww, rowh = 0, 0
        w, h = 0, 0
        for i in range(32, 128):
            if self.face.load_char(chr(i), ft.FT_LOAD_RENDER | ft.FT_LOAD_FORCE_AUTOHINT):
                raise RuntimeError("Character {} failed to load".format(chr(i)))
            if roww + self.glyph.bitmap.width + 1 >= 1024:
                w = max(w, roww)
                h += rowh
                roww, rowh = 0, 0
            roww += self.face.glyph.bitmap.width + 1
            rowh = max(rowh, self.face.glyph.bitmap.rows)
        self.atlas_width = np.uint32(max(w, roww))
        h += rowh
        self.atlas_heigth = np.uint32(h)
        
        GL.glActiveTexture(GL.GL_TEXTURE0)
        self.texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        
        # tex = GL.glGetUniformLocation(program, "tex")
        # GL.glUniform1i(tex, 0)
        
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RED, self.atlas_width, h, 0,
                        GL.GL_ALPHA, GL.GL_UNSIGNED_BYTE, 0)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        
        # self.chars_info = [None] * 128
        # ox, oy = 0, 0
        # rowh = 0
        # for i in range(32, 128):
        #     if face.load_char(chr(i), ft.FT_LOAD_RENDER | ft.FT_LOAD_FORCE_AUTOHINT):
        #         raise RuntimeError("Character {} failed to load".format(chr(i)))
        #     if ox + self.glyph.bitmap.width + 1 >= 1024:
        #         oy += rowh
        #         rowh = 0
        #         ox = 0
        #     GL.glTexSubImage2D(GL.GL_TEXTURE_2D, 0, ox, oy, self.glyph.bitmap.width,
        #                        self.glyph.bitmap.rows, GL.GL_ALPHA, GL.GL_UNSIGNED_BYTE,
        #                        self.glyph.bitmap.buffer)
        #     _ax = self.glyph.advance.x >> 6
        #     _ay = self.glyph.advance.y >> 6
        #     _bw = self.glyph.bitmap.width
        #     _bh = self.glyph.bitmap.rows
        #     _bl = self.glyph.bitmap_left
        #     _bt = self.glyph.bitmap_top
        #     _tx = np.float32(ox / w)
        #     _ty = np.float32(oy / h)
        #     self.chars_info[i] = CharsInfo(_ax, _ay, _bw, _bh, _bl, _bt, _tx, _ty)
        #     rowh = max(rowh, self.glyph.bitmap.rows)
        #     ox += self.glyph.bitmap.width + 1
        return True
    
    def render_text(self, program, text, x, y, sx, sy):
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        tex = GL.glGetUniformLocation(program, "tex")
        GL.glUniform1i(tex, 0)
        
        coord_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        # GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_DYNAMIC_DRAW)
        gl_coord = GL.glGetAttribLocation(program, "coord")
        GL.glEnableVertexAttribArray(gl_coord)
        GL.glVertexAttribPointer(gl_coord, 4, GL.GL_FLOAT, GL.GL_FALSE, 0, 0)
        
        coords = [None] * 6 * len(text)
        i = 0
        for c in text:
            x2 = x + self.chars_info[ord(c)].bl * sx
            y2 = -y - self.chars_info[ord(c)].bt * sy
            w = self.chars_info[ord(c)].bw * sx
            h = self.chars_info[ord(c)].bh * sy
            x += self.chars_info[ord(c)].ax * sx
            y += self.chars_info[ord(c)].ay * sy
            if not w or not h:
                continue
            
            coords[i] = Point(x2, -y2, self.chars_info[ord(c)].tx, self.chars_info[ord(c)].ty)
            i += 1
            coords[i] = Point(x2 + w, -y2, self.chars_info[ord(c)].tx + self.chars_info[ord(c)].bw / self.atlas_width, self.chars_info[ord(c)].ty)
            i += 1
            coords[i] = Point(x2, -y2 - h, self.chars_info[ord(c)].tx, self.chars_info[ord(c)].ty + self.chars_info[ord(c)].bh / self.atlas_heigth)
            i += 1
            coords[i] = Point(x2 + w, -y2, self.chars_info[ord(c)].tx + self.chars_info[ord(c)].bw / self.atlas_width, self.chars_info[ord(c)].ty)
            i += 1
            coords[i] = Point(x2, -y2 - h, self.chars_info[ord(c)].tx, self.chars_info[ord(c)].ty + self.chars_info[ord(c)].bh / self.atlas_heigth)
            i += 1
            coords[i] = Point(x2 + w, -y2 - h, self.chars_info[ord(c)].tx + self.chars_info[ord(c)].bw / self.atlas_width, self.chars_info[ord(c)].ty + self.chars_info[ord(c)].bh / self.atlas_heigth)
            i += 1
            
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(coords), coords, GL.GL_DYNAMIC_DRAW)
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, i)
            GL.glDisableVertexAttribArray(gl_coord)
    
    def make_freetype_texture(self, program):
        """ Function doc
        """
        coords = np.zeros(3,np.float32)
        uv_pos = np.zeros(4,np.float32)
        
        vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vertex_array_object)
        
        coord_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_DYNAMIC_DRAW)
        gl_coord = GL.glGetAttribLocation(program, "vert_coord")
        GL.glEnableVertexAttribArray(gl_coord)
        GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
        
        tex_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, tex_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, uv_pos.itemsize*len(uv_pos), uv_pos, GL.GL_DYNAMIC_DRAW)
        gl_texture = GL.glGetAttribLocation(program, "vert_uv")
        GL.glEnableVertexAttribArray(gl_texture)
        GL.glVertexAttribPointer(gl_texture, 4, GL.GL_FLOAT, GL.GL_FALSE, 4*uv_pos.itemsize, ctypes.c_void_p(0))
        
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(gl_coord)
        GL.glDisableVertexAttribArray(gl_texture)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        
        self.vao = vertex_array_object
        self.vbos = (coord_vbo, tex_vbo)
        return True
    
    def load_matrices(self, program, model_mat, view_mat, proj_mat):
        """ Function doc """
        model_mat[:3,:3] = np.identity(3)
        model = GL.glGetUniformLocation(program, "model_mat")
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, model_mat)
        view = GL.glGetUniformLocation(program, "view_mat")
        GL.glUniformMatrix4fv(view, 1, GL.GL_FALSE, view_mat)
        proj = GL.glGetUniformLocation(program, "proj_mat")
        GL.glUniformMatrix4fv(proj, 1, GL.GL_FALSE, proj_mat)
    
    def load_font_params(self, program):
        """ Loads the uniform parameters for the OpenGL program, such as the
            offset coordinates (X,Y) to calculate the quad and the color of
            the font.
        """
        offset = GL.glGetUniformLocation(program, "offset")
        GL.glUniform2fv(offset, 1, self.offset)
        color = GL.glGetUniformLocation(program, "text_color")
        GL.glUniform4fv(color, 1, self.color)
        return True
    
    def print_all(self):
        """ Function created only with debuging purposes.
        """
        print("#############################################")
        print(self.font_file, "font_file")
        print(self.char_res, "char_res")
        print(self.char_width, "char_width")
        print(self.char_height, "char_height")
        print(self.offset, "offset")
        print(self.color, "color")
        print(self.font_buffer, "font_buffer")
        print(self.texture_id, "texture_id")
        print(self.text_u, "text_u")
        print(self.text_v, "text_v")
        print(self.vao, "vao")
        print(self.vbos, "vbos")
    
