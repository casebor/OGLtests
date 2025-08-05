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
    
    def __init__ (self, fov=30.0, var=4.0/3.0, pos=None, zrp=None):
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
        if zrp is None:
            self.zero_reference_point = np.array([0,0,0], dtype=np.float32)
        if pos is None:
            pos = np.array([0,0,10], dtype=np.float32)
        self.max_vertical_angle = 85.0  # must be less than 90 to avoid gimbal lock
        self.horizontal_angle = 0.0
        self.vertical_angle = 0.0
        self.min_znear = 0.1
        self.min_zfar = 9.0
        dist = np.linalg.norm(pos - self.zero_reference_point)
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
        # return mop.get_xyz_coords(self.view_matrix)
        return self.view_matrix[3,:3]
    
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
        self.font_scale = 1.0
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
            self.font_data[char]["geom_uv"] = np.array([uvsx, uvex, uvsy, uvey], dtype=np.float32)
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
        GL.glVertexAttribPointer(gl_texture, 4, GL.GL_FLOAT, GL.GL_FALSE, 4*textur.itemsize, ctypes.c_void_p(0))
        
        self.vao = vao
        self.texture = font_texture
        self.coord_vbo = coord_vbo
        self.texture_vbo = tex_vbo
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(gl_coord)
        GL.glDisableVertexAttribArray(gl_texture)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    
    def fill_texture_buffers_BCK(self, program, words, coords):
        coords[0] = [-1,1,0]
        coords[1] = [0,-1,0]
        w_size = 0
        for word in words:
            w_size += len(word) * 6
        text_uvs = np.empty([w_size,2], dtype=np.float32)
        coords_uv = np.empty([w_size,3], dtype=np.float32)
        pos = 0
        for i, word in enumerate(words):
            t_uv = np.zeros([len(word)*6,2], dtype=np.float32)
            c_uv = np.zeros([len(word)*6,3], dtype=np.float32)
            offset_x = 0.0
            offset_y = 0.0
            for j, char in enumerate(word):
                if j > 0:
                    offset_y -= (self.font_data[word[j-1]]["dir_vec"][1] - self.font_data[char]["dir_vec"][1])
                offset_x += self.font_data[char]["dir_vec"][0] * 0.6
                t_uv[j*6:(j+1)*6] = self.font_data[char]["uv"]
                c_uv[j*6:(j+1)*6] = self.font_data[char]["xyz"] * self.font_scale
                c_uv[j*6:(j+1)*6] += coords[i]
                c_uv[j*6:(j+1)*6,0] += offset_x * self.font_scale
                c_uv[j*6:(j+1)*6,1] += offset_y * self.font_scale
                offset_x += self.font_data[char]["dir_vec"][0] * 0.6
            text_uvs[pos:pos+len(word)*6] = t_uv
            coords_uv[pos:pos+len(word)*6] = c_uv
            pos += len(word) * 6
        
        self.elements = coords_uv.shape[0]
        print(coords_uv.shape)
        print(text_uvs.shape)
        
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, coords_uv.nbytes, coords_uv, GL.GL_STATIC_DRAW)
        
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.texture_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, text_uvs.nbytes, text_uvs, GL.GL_STATIC_DRAW)
    
    def fill_texture_buffers(self, program, words, coords):
        coords[0] = [-1,1,0]
        coords[1] = [0,-1,0]
        w_size = 0
        for word in words:
            w_size += len(word)
        text_uvs = np.empty([w_size,4], dtype=np.float32)
        coords_uv = np.empty([w_size,3], dtype=np.float32)
        pos = 0
        for i, word in enumerate(words):
            t_uv = np.zeros([len(word),4], dtype=np.float32)
            c_uv = np.zeros([len(word),3], dtype=np.float32)
            offset_x = 0.0
            offset_y = 0.0
            for j, char in enumerate(word):
                if j > 0:
                    offset_y -= (self.font_data[word[j-1]]["dir_vec"][1] - self.font_data[char]["dir_vec"][1])
                offset_x += self.font_data[char]["dir_vec"][0]
                t_uv[j:j+1] = self.font_data[char]["geom_uv"]
                c_uv[j:j+1] = coords[i] * self.font_scale
                c_uv[j:j+1,0] += offset_x * self.font_scale
                c_uv[j:j+1,1] += offset_y * self.font_scale
                offset_x += self.font_data[char]["dir_vec"][0]
            text_uvs[pos:pos+len(word)] = t_uv
            coords_uv[pos:pos+len(word)] = c_uv
            pos += len(word)
        
        self.elements = coords_uv.shape[0]
        print(coords_uv.shape)
        print(text_uvs.shape)
        
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, coords_uv.nbytes, coords_uv, GL.GL_STATIC_DRAW)
        
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
        GL.glDrawArrays(GL.GL_POINTS, 0, self.elements)
        
        GL.glDisable(GL.GL_BLEND)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def load_matrices(self, program, model_mat, view_mat, proj_mat):
        """ Function doc """
        m_mat = np.copy(model_mat)
        # m_mat[:3,:3] = np.identity(3)
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
    

class GLAxis:
    """ This class contains all necessary components for the creation of a
        gizmo axis, including shaders, matrices, coordinates and functions to
        represent it in OpenGL. This class was created with the purpose of
        being completely independent from the VisMol widget, i.e. you could
        take this class and implement it in your own window.
        As this class is intended to be independent, almost all the methods
        receive no arguments.
    """
    
    def __init__ (self, cam_pos=np.zeros(3, dtype=np.float32)):
        """ For creating a GLAxis object you only need to supply the position
            of your camera or eye as an numpy array of XYZ components.
            The default position for the camera is 0x, 0y, 0z.
            The default position of the gismo is at the bottom left of the
            window, you can change this location by multiplying the coordinates
            by a translation matrix, or using another set of coordinates.
        """
        # These coordinates are for a cone with the base at the origen ant pointining
        # towards the positive X axis. To use the data for the other axis, rotate
        # the points :P
        a, b, c = 0.0, 0.707107, 1.0
        self.axis_cone = np.array([[ a, a,-c],[ c, a, a],[ a,-b,-b],
                                   [ a,-b,-b],[ c, a, a],[ a,-c, a],
                                   [ a,-c, a],[ c, a, a],[ a,-b, b],
                                   [ a,-b, b],[ c, a, a],[-a, a, c],
                                   [-a, a, c],[ c, a, a],[-a, b, b],
                                   [-a, b, b],[ c, a, a],[-a, c,-a],
                                   [-a, c,-a],[ c, a, a],[-a, b,-b],
                                   [-a, b,-b],[ c, a, a],[ a, a,-c],

                                   [ a, a,-c],[ a,-b,-b],[ a,-c, a],
                                   [ a,-c, a],[ a,-b, b],[-a, a, c],
                                   [-a, a, c],[-a, b, b],[-a, c,-a],
                                   [-a, c,-a],[-a, b,-b],[ a, a,-c],
                                   [ a, a,-c],[ a,-c, a],[-a, a, c],
                                   [-a, a, c],[-a, c,-a],[ a, a,-c]], dtype=np.float32)
        p, q, r, s = 0.0, 0.2811, 0.6786, 1.0
        self.axis_norms = np.array([[ r,-q,-r],[ r,-q,-r],[ r,-q,-r],
                                    [ r,-r,-q],[ r,-r,-q],[ r,-r,-q],
                                    [ r,-r, q],[ r,-r, q],[ r,-r, q],
                                    [ r,-q, r],[ r,-q, r],[ r,-q, r],
                                    [ r, q, r],[ r, q, r],[ r, q, r],
                                    [ r, r, q],[ r, r, q],[ r, r, q],
                                    [ r, r,-q],[ r, r,-q],[ r, r,-q],
                                    [ r, q,-r],[ r, q,-r],[ r, q,-r],
                                    [-s,-p, p],[-s,-p, p],[-s,-p, p],
                                    [-s,-p, p],[-s,-p, p],[-s,-p, p],
                                    [-s,-p, p],[-s,-p, p],[-s,-p, p],
                                    [-s,-p, p],[-s,-p, p],[-s,-p, p],
                                    [-s,-p, p],[-s,-p, p],[-s,-p, p],
                                    [-s,-p, p],[-s,-p, p],[-s,-p, p]], dtype=np.float32)
        self.lines_vertices = np.array([[-0.900,-0.900, 0.000],[-0.825,-0.900, 0.000],
                                        [-0.900,-0.900, 0.000],[-0.900,-0.825, 0.000],
                                        [-0.900,-0.900, 0.000],[-0.900,-0.900,-0.075]], dtype=np.float32)
        self.axis_indices = np.arange(42, dtype=np.uint32)
        self.axis_colors = {"x_axis" : [1.0, 0.0, 0.0],
                            "y_axis" : [0.0, 1.0, 0.0],
                            "z_axis" : [0.0, 0.0, 1.0]}
        self.model_mat = np.identity(4, dtype=np.float32)
        self.model_mat[3,:3] = cam_pos
        self.gizmo_axis_program = None
        self.gl_lines_program = None
        self.x_vao = None
        self.y_vao = None
        self.z_vao = None
        self.lines_vao = None
        self.zrp = np.array([-0.9,-0.9, 0.0],dtype=np.float32)
        self.camera_position = np.array(cam_pos, dtype=np.float32)
        self.light_position = np.array([-0.5, 0.0,-1.0],dtype=np.float32)
        self.light_color = np.array([0.0, 0.0, 0.0, 1.0],dtype=np.float32)
        self.light_intensity = np.array([0.6, 0.6, 0.6],dtype=np.float32)
        self.light_ambient_coef = 0.2
        self.light_specular_coef = 1.0
        self.light_shininess = 3.0
        self.vertex_shader_axis = """
#version 330

uniform mat4 model_mat;

in vec3 vert_coord;
in vec3 vert_color;
in vec3 vert_norm;

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_norm;

void main(){
    frag_coord = vec3(model_mat * vec4(vert_coord, 1.0));
    frag_norm = mat3(transpose(inverse(model_mat))) * vert_norm;
    frag_color = vert_color;
    gl_Position = vec4(frag_coord, 1.0);
}
"""
        self.fragment_shader_axis = """
#version 330

struct Light {
    vec3 position;
    vec3 color;
    vec3 intensity;
    vec3 specular_color;
    float ambient_coef;
    float shininess;
};

uniform Light my_light;

in vec3 frag_coord;
in vec3 frag_color;
in vec3 frag_norm;

out vec4 final_color;

vec4 calculate_color(vec3 fnrm, vec3 fcrd, vec3 fcol){
    vec3 normal = normalize(fnrm);
    vec3 vert_to_light = normalize(my_light.position);
    vec3 vert_to_cam = normalize(fcrd);
    // Ambient Component
    vec3 ambient = my_light.ambient_coef * fcol * my_light.intensity;
    // Diffuse component
    float diffuse_coef = max(0.0, dot(normal, vert_to_light));
    vec3 diffuse = diffuse_coef * fcol * my_light.intensity;
    // Specular component
    float specular_coef = 0.0;
    if (diffuse_coef > 0.0)
        specular_coef = pow(max(0.0, dot(vert_to_cam, reflect(vert_to_light, normal))), my_light.shininess);
    vec3 specular = specular_coef * my_light.intensity;
    specular = specular * (vec3(1) - diffuse);
    vec4 out_color = vec4(ambient + diffuse + specular, 1.0);
    return out_color;
}

void main() {
    final_color = calculate_color(frag_norm, frag_coord, frag_color);
}
"""
        self.vertex_shader_lines = """
#version 330

uniform mat4 model_mat;

in vec3 vert_coord;
in vec3 vert_color;

out vec3 frag_color;

void main()
{
    gl_Position = model_mat * vec4(vert_coord, 1.0);
    frag_color = vert_color;
}
"""
        self.fragment_shader_lines = """
#version 330

in vec3 frag_color;

out vec4 final_color;

void main()
{
    final_color = vec4(frag_color, 1.0);
}
"""
    
    def initialize_gl(self):
        """ First function, called right after the object creation. Creates the
            OpenGL programs and Vertex Array Objects.
        """
        self._make_axis_program()
        self._make_lines_program()
        self._make_gl_gizmo_axis()
        return True
    
    def _make_gl_gizmo_axis(self):
        """ Creates the Vertex Array Objects for the XYZ axis. Initially creates
            the vaos for the cones of the axis and then for the lines.
        """
        self.x_vao = self._get_vao("x_axis")
        self.y_vao = self._get_vao("y_axis")
        self.z_vao = self._get_vao("z_axis")
        self.lines_vao = self._get_vao_lines()
        return True
    
    def _make_axis_program(self):
        """ Compiles the cone shaders. This function compiles only the cones
            of the gizmo axis.
        """
        v_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        GL.glShaderSource(v_shader, self.vertex_shader_axis)
        GL.glCompileShader(v_shader)
        f_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        GL.glShaderSource(f_shader, self.fragment_shader_axis)
        GL.glCompileShader(f_shader)
        self.gizmo_axis_program = GL.glCreateProgram()
        GL.glAttachShader(self.gizmo_axis_program, v_shader)
        GL.glAttachShader(self.gizmo_axis_program, f_shader)
        GL.glLinkProgram(self.gizmo_axis_program)
        if GL.glGetShaderiv(v_shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", "GL_VERTEX_SHADER")
            raise RuntimeError(GL.glGetShaderInfoLog(v_shader))
        if GL.glGetShaderiv(f_shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", "GL_FRAGMENT_SHADER")
            raise RuntimeError(GL.glGetShaderInfoLog(f_shader))
        return True
    
    def _make_lines_program(self):
        """ Compiles the lines shaders. This function compiles only the lines
            of the gizmo axis.
        """
        v_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        GL.glShaderSource(v_shader, self.vertex_shader_lines)
        GL.glCompileShader(v_shader)
        f_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        GL.glShaderSource(f_shader, self.fragment_shader_lines)
        GL.glCompileShader(f_shader)
        self.gl_lines_program = GL.glCreateProgram()
        GL.glAttachShader(self.gl_lines_program, v_shader)
        GL.glAttachShader(self.gl_lines_program, f_shader)
        GL.glLinkProgram(self.gl_lines_program)
        if GL.glGetShaderiv(v_shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", "GL_VERTEX_SHADER")
            raise RuntimeError(GL.glGetShaderInfoLog(v_shader))
        if GL.glGetShaderiv(f_shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", "GL_FRAGMENT_SHADER")
            raise RuntimeError(GL.glGetShaderInfoLog(f_shader))
        return True
    
    def _get_rotmat3f(self, angle, dir_vec):
        assert(np.linalg.norm(dir_vec)>0.0)
        x = dir_vec[0]
        y = dir_vec[1]
        z = dir_vec[2]
        c = np.cos(angle)
        s = np.sin(angle)
        rot_matrix = np.identity(3, dtype=np.float32)
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
    
    def _get_vao(self, axis):
        """ Creates the Vertex Array Object, Vertex Buffer Objects and fill the
            shaders with the data of the corresponding axis. The buffers are not
            stored anywhere since the data will be the same always, so does the
            drawing method is GL_STATIC_DRAW and not GL_DYNAMIC_DRAW.
            
            Input parameters:
            axis -- a string describing the corresponding axis, its values can
                    be x_axis, y_axis or z_axis.
        
            Returns:
                The Vertex Array Object of the corresponding axis.
        """
        if axis == "y_axis":
            rot_mat = self._get_rotmat3f(np.pi/2.0, [0,0,1])
            offset = np.array([0.0, 0.075, 0.0], dtype=np.float32)
        elif axis == "z_axis":
            rot_mat = self._get_rotmat3f(np.pi/2.0, [0,1,0])
            offset = np.array([0.0, 0.0,-0.075], dtype=np.float32)
        elif axis == "x_axis":
            rot_mat = np.identity(3, dtype=np.float32)
            offset = np.array([0.075, 0.0, 0.0], dtype=np.float32)
        scale = 0.03
        coords = np.empty([42,3], dtype=np.float32)
        normals = np.empty([42,3], dtype=np.float32)
        for i in range(self.axis_cone.shape[0]):
            coords[i] = np.matmul(rot_mat, self.axis_cone[i]) * scale + self.zrp + offset
            normals [i] = np.matmul(rot_mat, self.axis_norms[i])
        colors = np.tile(self.axis_colors[axis], 42).reshape(42, 3).astype(np.float32)
        
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        
        ind_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.axis_indices.nbytes, self.axis_indices, GL.GL_STATIC_DRAW)
        
        vert_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vert_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
        att_position = GL.glGetAttribLocation(self.gizmo_axis_program, "vert_coord")
        GL.glEnableVertexAttribArray(att_position)
        GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
        
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
        att_colors = GL.glGetAttribLocation(self.gizmo_axis_program, "vert_color")
        GL.glEnableVertexAttribArray(att_colors)
        GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
        
        norm_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, norm_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, normals.nbytes, normals, GL.GL_STATIC_DRAW)
        att_norm = GL.glGetAttribLocation(self.gizmo_axis_program, "vert_norm")
        GL.glEnableVertexAttribArray(att_norm)
        GL.glVertexAttribPointer(att_norm, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*normals.itemsize, ctypes.c_void_p(0))
        
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(att_position)
        GL.glDisableVertexAttribArray(att_colors)
        GL.glDisableVertexAttribArray(att_norm)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
        
        return vao
    
    def _get_vao_lines(self):
        """ Creates the Vertex Array Object, Vertex Buffer Objects and fill the
            shaders with the data of the gizmo"s lines. It takes no arguments
            since the lines are taken as one entity
            
            Returns:
                The Vertex Array Object of the corresponding axis.
        """
        line_colors = np.empty(18, dtype=np.float32)
        line_colors[:6] = np.tile(self.axis_colors["x_axis"], 2)
        line_colors[6:12] = np.tile(self.axis_colors["y_axis"], 2)
        line_colors[12:] = np.tile(self.axis_colors["z_axis"], 2)
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        
        vert_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vert_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.lines_vertices.nbytes, self.lines_vertices, GL.GL_STATIC_DRAW)
        
        att_position = GL.glGetAttribLocation(self.gl_lines_program, "vert_coord")
        GL.glEnableVertexAttribArray(att_position)
        GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.lines_vertices.itemsize, ctypes.c_void_p(0))
        
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, line_colors.nbytes, line_colors, GL.GL_STATIC_DRAW)
        
        att_colors = GL.glGetAttribLocation(self.gl_lines_program, "vert_color")
        GL.glEnableVertexAttribArray(att_colors)
        GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*line_colors.itemsize, ctypes.c_void_p(0))
        
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(att_position)
        GL.glDisableVertexAttribArray(att_colors)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        
        return vao
    
    def load_params(self):
        """ This function load the model matrix of the gizmo, the camera
            position and the light parameters in the cones OpenGL program.
        """
        model = GL.glGetUniformLocation(self.gizmo_axis_program, "model_mat")
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, self.model_mat)
        light_pos = GL.glGetUniformLocation(self.gizmo_axis_program, "my_light.position")
        GL.glUniform3fv(light_pos, 1, self.light_position)
        light_col = GL.glGetUniformLocation(self.gizmo_axis_program, "my_light.color")
        GL.glUniform3fv(light_col, 1, self.light_color)
        amb_coef = GL.glGetUniformLocation(self.gizmo_axis_program, "my_light.ambient_coef")
        GL.glUniform1fv(amb_coef, 1, self.light_ambient_coef)
        spec_coef = GL.glGetUniformLocation(self.gizmo_axis_program, "my_light.specular_coef")
        GL.glUniform1fv(spec_coef, 1, self.light_specular_coef)
        shiny = GL.glGetUniformLocation(self.gizmo_axis_program, "my_light.shininess")
        GL.glUniform1fv(shiny, 1, self.light_shininess)
        intensity = GL.glGetUniformLocation(self.gizmo_axis_program, "my_light.intensity")
        GL.glUniform3fv(intensity, 1, self.light_intensity)
        return True
    
    def load_lines_params(self):
        """ Load the model matrix of the gizmo"s lines in the lines OpenGL
            program.
        """
        model = GL.glGetUniformLocation(self.gl_lines_program, "model_mat")
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, self.model_mat)
        return True
    
    def _draw(self, flag):
        """ Function called to draw the gizmo axis in an OpenGL window.
            To drawing method is inside the class to make the class completely
            independent.
            
            Input parameters:
            flag -- a boolean to determine if the cones or the lines are going
                    to be drawed up. True for draw the cones, False to draw only
                    the lines.
            
            IMPORTANT!!!
            THIS FUNCTION MUST BE CALLED ONLY WHEN AN OPENGL CONTEXT WINDOW HAS
            BEEN CREATED AND INITIALIZED, OTHERWISE WILL RAISE AN ERROR IN THE
            OPENGL WRAPPER!!!
            YOU HAVE BEEN WARNED
        """
        GL.glEnable(GL.GL_DEPTH_TEST)
        if flag:
            GL.glUseProgram(self.gizmo_axis_program)
            self.load_params()
            GL.glBindVertexArray(self.x_vao)
            GL.glDrawElements(GL.GL_TRIANGLES, len(self.axis_indices), GL.GL_UNSIGNED_INT, None)
            GL.glBindVertexArray(0)
            GL.glBindVertexArray(self.y_vao)
            GL.glDrawElements(GL.GL_TRIANGLES, len(self.axis_indices), GL.GL_UNSIGNED_INT, None)
            GL.glBindVertexArray(0)
            GL.glBindVertexArray(self.z_vao)
            GL.glDrawElements(GL.GL_TRIANGLES, len(self.axis_indices), GL.GL_UNSIGNED_INT, None)
            GL.glBindVertexArray(0)
            GL.glUseProgram(0)
        else:
            GL.glUseProgram(self.gl_lines_program)
            GL.glLineWidth(5)
            self.load_lines_params()
            GL.glBindVertexArray(self.lines_vao)
            GL.glDrawArrays(GL.GL_LINES, 0, len(self.lines_vertices))
            GL.glBindVertexArray(0)
            GL.glLineWidth(1)
            GL.glUseProgram(0)
        GL.glDisable(GL.GL_DEPTH_TEST)
        return True
    
