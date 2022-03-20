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

import os
import json
import ctypes
import numpy as np
import freetype as ft
import matrix_operations as mop
from OpenGL import GL


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


class VismolFont():
    """ VismolFont is used to render text from SDF font files and a description
        of the position of the characters in the image.
    """
    
    def __init__ (self, font_name="Arial", color=None):
        """ Class initialiser
        """
        if color is None:
            self.color = np.ones(3, dtype=np.float32)
        else:
            self.color = np.array(color, dtype=np.float32)
        self.font_image = os.path.join("fonts", font_name + ".png")
        self.font_json = os.path.join("fonts", font_name + ".json")
        self.font_data = None
        self.vao = None
        self.texture = None
        self.coord_vbo = None
        self.texture_vbo = None
        self.modified = True
    
    def _load_font_data(self):
        """ Calculate the parameters for each character in the font atlas.
            [uvsx, uvsy] -> start uv coordinates of the character in the atlas
            [uvex, uvey] -> end uv coordinates of the character in the atlas
            | 0,0    |    | uvsx,uvsy           |
            |    *   | -> |          *          |
            |     1,1|    |           uvex,uvey |
        """
        with open(self.font_json, "r") as f:
            self.font_json = json.load(f)
        self.font_name = self.font_json.pop("name")
        self.font_data = {}
        self.font_data["scaleW"] = np.float32(self.font_json.pop("scaleW"))
        self.font_data["scaleH"] = np.float32(self.font_json.pop("scaleH"))
        wmax, hmax = 0.0, 0.0
        for char, data in self.font_json.items():
            if len(char) > 1:
                continue
            uvsx = data["x"] / self.font_data["scaleW"]
            uvex = (data["x"] + data["w"]) / self.font_data["scaleW"]
            uvsy = data["y"] / self.font_data["scaleH"]
            uvey = (data["y"] + data["h"]) / self.font_data["scaleH"]
            self.font_data[char] = {}
            self.font_data[char]["uv"] = np.array([[uvsx,uvsy], [uvsx,uvey], [uvex,uvsy],
                                                   [uvsx,uvey], [uvex,uvsy], [uvex,uvey]], dtype=np.float32)
            if data["w"] > wmax:
                wmax = data["w"]
            if data["h"] > hmax:
                hmax = data["h"]
        for char, data in self.font_json.items():
            if len(char) > 1:
                continue
            xs = (data["w"] / wmax) / 2.0
            ys = (data["h"] / hmax) / 2.0
            self.font_data[char]["xyz"] = np.array([[-xs,ys,0], [-xs,-ys,0], [xs,ys,0],
                                                    [-xs,-ys,0], [xs,ys,0], [xs,-ys,0]], dtype=np.float32)
            self.font_data[char]["dir_vec"] = np.array([xs,ys], dtype=np.float32)
    
    def make_font_atlas(self, program):
        """ Function doc """
        from PIL import Image
        image_a = Image.open(self.font_image)
        ix = image_a.size[0]
        iy = image_a.size[1]
        assert self.font_data is not None
        assert self.font_data["scaleW"] == np.float32(ix)
        assert self.font_data["scaleH"] == np.float32(iy)
        image_a = np.array(list(image_a.getdata()), dtype=np.uint8)
        font_texture = GL.glGenTextures(1)
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, font_texture)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, ix, iy, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image_a)
        
        coords = np.zeros(3, dtype=np.float32)
        textur = np.zeros(2, dtype=np.float32)
        
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        
        coord_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
        gl_coord = GL.glGetAttribLocation(program, "vert_coord")
        GL.glEnableVertexAttribArray(gl_coord)
        GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize,ctypes.c_void_p(0))
        
        tex_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, tex_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, textur.nbytes, textur, GL.GL_STATIC_DRAW)
        gl_texture = GL.glGetAttribLocation(program, "vert_uv")
        GL.glEnableVertexAttribArray(gl_texture)
        GL.glVertexAttribPointer(gl_texture, 2, GL.GL_FLOAT, GL.GL_FALSE, 2*textur.itemsize, ctypes.c_void_p(0))
        
        self.vao = vao
        self.texture = font_texture
        self.coord_vbo = coord_vbo
        self.texture_vbo = tex_vbo
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(gl_coord)
        GL.glDisableVertexAttribArray(gl_texture)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    
    def fill_texture_buffers(self, program, words, coords):
        coords[0] = [-1,1,0]
        coords[1] = [0,-1,0]
        text_uvs = np.empty(2, dtype=np.float32)
        coords_uv = np.empty(3, dtype=np.float32)
        for i, word in enumerate(words):
            c_uv = np.zeros([len(word)*6,3], dtype=np.float32)
            t_uv = np.zeros([len(word)*6,2], dtype=np.float32)
            offset_x = 0.0
            offset_y = 0.0
            for j, char in enumerate(word):
                if j > 0:
                    offset_y -= (self.font_data[word[j-1]]["dir_vec"][1] - self.font_data[char]["dir_vec"][1])
                offset_x += self.font_data[char]["dir_vec"][0] * 0.6
                t_uv[j*6:(j+1)*6] = self.font_data[char]["uv"]
                c_uv[j*6:(j+1)*6] = self.font_data[char]["xyz"]
                c_uv[j*6:(j+1)*6] += coords[i]
                c_uv[j*6:(j+1)*6,0] += offset_x
                c_uv[j*6:(j+1)*6,1] += offset_y
                offset_x += self.font_data[char]["dir_vec"][0] * 0.6
            coords_uv = np.vstack([coords_uv, c_uv])
            text_uvs = np.vstack([text_uvs, t_uv])
        
        text_uvs = text_uvs[1:]
        coords = coords_uv[1:]
        # coords = np.array(coords_uv, dtype=np.float32)
        self.elements = coords.shape[0]
        print(coords.shape)
        print(text_uvs.shape)
        # print(text_uvs)
        
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
        
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.texture_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, text_uvs.nbytes, text_uvs, GL.GL_STATIC_DRAW)
    
    def render_text(self, program, mmat, vmat, pmat, text, coords):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glUseProgram(program)
        self.load_matrices(program, mmat, vmat, pmat)
        self.load_font_params(program)
        GL.glBindVertexArray(self.vao)
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        
        if self.modified:
            self.fill_texture_buffers(program, text, coords)
            self.modified = False
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.elements)
        
        GL.glDisable(GL.GL_BLEND)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def load_matrices(self, program, model_mat, view_mat, proj_mat):
        """ Function doc """
        m_mat = np.copy(model_mat)
        m_mat[:3,:3] = np.identity(3)
        model = GL.glGetUniformLocation(program, "model_mat")
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, m_mat)
        view = GL.glGetUniformLocation(program, "view_mat")
        GL.glUniformMatrix4fv(view, 1, GL.GL_FALSE, view_mat)
        proj = GL.glGetUniformLocation(program, "proj_mat")
        GL.glUniformMatrix4fv(proj, 1, GL.GL_FALSE, proj_mat)
    
    def load_font_params(self, program):
        """ Loads the uniform parameters for the OpenGL program, such as the
            offset coordinates (X,Y) to calculate the quad and the color of
            the font.
        """
        gl_text = GL.glGetUniformLocation(program, "font_texture")
        GL.glUniform1i(gl_text, 0)
        gl_color = GL.glGetUniformLocation(program, "font_color")
        GL.glUniform3fv(gl_color, 1, self.color)
        return True
    

class VisMolFont():
    """ VisMolFont stores the data created using the freetype python binding
        library, such as filename, character width, character height, character
        resolution, font color, etc.
    """
    
    def __init__ (self, font_file="Vera.ttf", char_res=64, c_w=0.25, c_h=0.3, color=[1,1,1,1]):
        """ Class initialiser
        """
        self.font_file = font_file
        self.char_res = char_res
        self.char_width = c_w
        self.char_height = c_h
        self.offset = np.array([c_w/2.0,c_h/2.0],dtype=np.float32)
        self.color = np.array(color,dtype=np.float32)
        self.font_buffer = None
        self.texture_id = None
        self.text_u = None
        self.text_v = None
        self.vao = None
        self.vbos = None
    
    def make_freetype_font(self):
        """ Function doc
        """
        face = ft.Face(self.font_file)
        face.set_char_size(self.char_res*64)
        # Determine largest glyph size
        width, height, ascender, descender = 0, 0, 0, 0
        for c in range(32,128):
            face.load_char(chr(c), ft.FT_LOAD_RENDER | ft.FT_LOAD_FORCE_AUTOHINT)
            bitmap = face.glyph.bitmap
            width = max(width, bitmap.width)
            ascender = max(ascender, face.glyph.bitmap_top)
            descender = max(descender, bitmap.rows-face.glyph.bitmap_top)
        height = ascender+descender
        # Generate texture data
        self.font_buffer = np.zeros((height*6, width*16), dtype=np.ubyte)
        for j in range(6):
            for i in range(16):
                face.load_char(chr(32+j*16+i), ft.FT_LOAD_RENDER | ft.FT_LOAD_FORCE_AUTOHINT )
                bitmap = face.glyph.bitmap
                x = i*width  + face.glyph.bitmap_left
                y = j*height + ascender - face.glyph.bitmap_top
                self.font_buffer[y:y+bitmap.rows,x:x+bitmap.width].flat = bitmap.buffer
        # Bound texture
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        self.texture_id = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RED, self.font_buffer.shape[1], self.font_buffer.shape[0], 0, GL.GL_RED, GL.GL_UNSIGNED_BYTE, self.font_buffer)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        # Fill the font variables with data
        self.text_u = width/float(self.font_buffer.shape[1])
        self.text_v = height/float(self.font_buffer.shape[0])
        return True
    
    def make_freetype_texture(self, program):
        """ Function doc
        """
        coords = np.zeros(3,np.float32)
        uv_pos = np.zeros(4,np.float32)
        
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        
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
        
        self.vao = vao
        self.vbos = (coord_vbo, tex_vbo)
        return True
    
    def load_matrices(self, program, model_mat, view_mat, proj_mat):
        """ Function doc """
        # model_mat[:3,:3] = np.identity(3)
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
    