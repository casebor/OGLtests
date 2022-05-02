#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  matrix_operations.py
#  
#  Copyright 2016 Labio <labio@labio-XPS-8300>
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


def my_glTranslatef(orig_matrix, position):
    """ Creates a translation matrix using an identity matrix and the
        position's coordinates at the last row, but only the xyz components.
        As initial result, you get the following matrix:
        
                        |1 0 0 0|       |1 0 0 0|
                        |0 1 0 0|  ==>  |0 1 0 0|
                        |0 0 1 0|  ==>  |0 0 1 0|
                        |0 0 0 1|       |x y z 1|
        
        then, this translation matrix is multiplied to the input matrix to
        obtain the final result, a translated matrix to position.
        
        Keyword arguments:
            in_matrix -- a 4x4 matrix that you want to apply a translation.
            position -- a 3 elements numpy ndarray with the coordinates of
                        your desired translation.
        
        Returns:
            A multiplied 4x4 matrix of [in_matrix] x [trans_matrix].
    """
    trans_matrix = np.identity(4, dtype=np.float32)
    trans_matrix[3,:3] = position
    return my_glMultiplyMatricesf(orig_matrix, trans_matrix)

def my_glMultiplyMatricesf(mat1, mat2):
    """ Multiplication of matrices in the order [mat1] x [mat2].
        
        Keyword arguments:
            mat1 -- a 4x4 matrix.
            mat2 -- a 4x4 matrix.
        
        Returns:
            result -- a multiplied 4x4 matrix of [mat1] x [mat2].
    """
    result = np.zeros((4,4), dtype=np.float32)
    result[0,0] = mat1[0,0]*mat2[0,0]+mat1[0,1]*mat2[1,0]+mat1[0,2]*mat2[2,0]+mat1[0,3]*mat2[3,0]
    result[1,0] = mat1[1,0]*mat2[0,0]+mat1[1,1]*mat2[1,0]+mat1[1,2]*mat2[2,0]+mat1[1,3]*mat2[3,0]
    result[2,0] = mat1[2,0]*mat2[0,0]+mat1[2,1]*mat2[1,0]+mat1[2,2]*mat2[2,0]+mat1[2,3]*mat2[3,0]
    result[3,0] = mat1[3,0]*mat2[0,0]+mat1[3,1]*mat2[1,0]+mat1[3,2]*mat2[2,0]+mat1[3,3]*mat2[3,0]
    
    result[0,1] = mat1[0,0]*mat2[0,1]+mat1[0,1]*mat2[1,1]+mat1[0,2]*mat2[2,1]+mat1[0,3]*mat2[3,1]
    result[1,1] = mat1[1,0]*mat2[0,1]+mat1[1,1]*mat2[1,1]+mat1[1,2]*mat2[2,1]+mat1[1,3]*mat2[3,1]
    result[2,1] = mat1[2,0]*mat2[0,1]+mat1[2,1]*mat2[1,1]+mat1[2,2]*mat2[2,1]+mat1[2,3]*mat2[3,1]
    result[3,1] = mat1[3,0]*mat2[0,1]+mat1[3,1]*mat2[1,1]+mat1[3,2]*mat2[2,1]+mat1[3,3]*mat2[3,1]
    
    result[0,2] = mat1[0,0]*mat2[0,2]+mat1[0,1]*mat2[1,2]+mat1[0,2]*mat2[2,2]+mat1[0,3]*mat2[3,2]
    result[1,2] = mat1[1,0]*mat2[0,2]+mat1[1,1]*mat2[1,2]+mat1[1,2]*mat2[2,2]+mat1[1,3]*mat2[3,2]
    result[2,2] = mat1[2,0]*mat2[0,2]+mat1[2,1]*mat2[1,2]+mat1[2,2]*mat2[2,2]+mat1[2,3]*mat2[3,2]
    result[3,2] = mat1[3,0]*mat2[0,2]+mat1[3,1]*mat2[1,2]+mat1[3,2]*mat2[2,2]+mat1[3,3]*mat2[3,2]
    
    result[0,3] = mat1[0,0]*mat2[0,3]+mat1[0,1]*mat2[1,3]+mat1[0,2]*mat2[2,3]+mat1[0,3]*mat2[3,3]
    result[1,3] = mat1[1,0]*mat2[0,3]+mat1[1,1]*mat2[1,3]+mat1[1,2]*mat2[2,3]+mat1[1,3]*mat2[3,3]
    result[2,3] = mat1[2,0]*mat2[0,3]+mat1[2,1]*mat2[1,3]+mat1[2,2]*mat2[2,3]+mat1[2,3]*mat2[3,3]
    result[3,3] = mat1[3,0]*mat2[0,3]+mat1[3,1]*mat2[1,3]+mat1[3,2]*mat2[2,3]+mat1[3,3]*mat2[3,3]
    return result

def my_glRotatef(in_matrix, angle, dir_vec):
    """ Produces a rotation matrix of "angle" degrees around the vector 
        "dir_vec", then multiply the input matrix "in_matrix" with this 
        rotation matrix "rot_matrix" in the order [in_matrix] x [trans_matrix].
        The rotation matrix takes the form of:
        
        | x*x*(1-c)+c   x*y*(1-c)-z*s   x*z*(1-c)+y*s   0|
        |y*x*(1-c)+z*s   y*y*(1-c)+c    y*z*(1-c)-x*s   0|
        |x*z*(1-c)-y*s  y*z*(1-c)+x*s    z*z*(1-c)+c    0|
        |      0              0               0         1|
        
        Keyword arguments:
            in_matrix -- a 4x4 matrix that you want to apply a rotation.
            angle -- the angle of rotation in radians.
            dir_vec -- a 3 elements vector with the xyz components to use as
                       axis of rotation.
        
        Returns:
            A multiplied 4x4 matrix of [in_matrix] x [rot_matrix].
    """
    vector = np.array(dir_vec, dtype=np.float32)
    assert(np.linalg.norm(vector)>0.0)
    angle = angle*np.pi/180.0
    x,y,z = vector/np.linalg.norm(vector)
    c = np.cos(angle)
    s = np.sin(angle)
    rot_matrix = np.identity(4, dtype=np.float32)
    rot_matrix[0,0] = x*x*(1-c)+c
    rot_matrix[1,0] = y*x*(1-c)+z*s
    rot_matrix[2,0] = x*z*(1-c)-y*s
    rot_matrix[0,1] = x*y*(1-c)-z*s
    rot_matrix[1,1] = y*y*(1-c)+c
    rot_matrix[2,1] = y*z*(1-c)+x*s
    rot_matrix[0,2] = x*z*(1-c)+y*s
    rot_matrix[1,2] = y*z*(1-c)-x*s
    rot_matrix[2,2] = z*z*(1-c)+c
    return my_glMultiplyMatricesf(in_matrix, rot_matrix)

def my_glPerspectivef(fovy, aspect, z_near, z_far):
    """ Creates a perspective matrix with "fovy" as field of view, "aspect" as
        viewport aspect ratio, "z_near" as the near clipping plane and "z_far"
        as far clipping plane. The perpective matrix is constructed in the form:
        
        |f/aspect  0                 0                   0|
        |   0      f                 0                   0|
        |   0      0    (z_near+z_far)/(z_near-z_far)   -1|
        |   0      0   2.0*z_near*z_far/(z_near-z_far)   0|
        
        With f = cotangent(fovy/2)
        
    """
    assert(aspect>0)
    assert(z_far>z_near)
    f = np.float32(1/(np.tan(fovy*np.pi/180.0)))
    pers_matrix = np.zeros((4,4), dtype=np.float32)
    pers_matrix[0,0] = f/aspect
    pers_matrix[1,1] = f
    pers_matrix[2,2] = (z_near+z_far)/(z_near-z_far)
    pers_matrix[3,2] = 2*z_near*z_far/(z_near-z_far)
    pers_matrix[2,3] = -1
    return pers_matrix

def my_glFrustum(left, right, bottom, top, z_near, z_far):
    assert(z_far>z_near)
    frustum = np.zeros((4,4), dtype=np.float32)
    frustum[0,0] = 2*z_near/(rigth-left)
    frustum[1,1] = 2*z_near/(top-bottom)
    frustum[2,2] = (z_far+z_near)/(z_near-z_far)
    frustum[2,0] = (rigth+left)/(rigth-left)
    frustum[2,1] = (top+bottom)/(top-bottom)
    frustum[2,3] = -1
    frustum[3,2] = 2*z_near*z_far/(z_near-z_far)
    return frustum

def my_glOrtho(left, right, bottom, top, z_near, z_far):
    assert(z_far>z_near)
    ortho_matrix = np.zeros((4,4), dtype=np.float32)
    ortho_matrix[0,0] = 2/(right-left)
    ortho_matrix[1,1] = 2/(top-bottom)
    ortho_matrix[2,2] = 2/(z_near-z_far)
    ortho_matrix[3,3] = 1
    ortho_matrix[3,0] = (left+right)/(left-right)
    ortho_matrix[3,1] = (bottom+top)/(bottom-top)
    ortho_matrix[3,1] = (z_near+z_far)/(z_near-z_far)
    return ortho_matrix

def get_xyz_coords(xyz_mat):
    """ Returns the x, y, z position contained in the xyz_mat matrix. The
        input matrix needs to be a 4x4 matrix.
    """
    assert(xyz_mat.ndim==2)
    assert(xyz_mat.size==16)
    rot_mat = xyz_mat[:3,:3]
    pos = -xyz_mat[3,:3]
    position = pos.dot(rot_mat)
    return position
