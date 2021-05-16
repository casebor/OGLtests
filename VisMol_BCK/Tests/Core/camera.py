#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  camera.py
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

import math
import numpy as np

def my_glRotateXf(in_matrix, angle):
    angle = angle*math.pi/180.0
    rot_matrix = np.identity(4, dtype=np.float32)
    rot_matrix[1,1] = math.cos(angle)
    rot_matrix[2,1] = math.sin(angle)
    rot_matrix[1,2] = -math.sin(angle)
    rot_matrix[2,2] =  math.cos(angle)
    return my_glMultiplyMatricesf(in_matrix, rot_matrix)

def my_glRotateYf(in_matrix, angle):
    angle = angle*math.pi/180.0
    rot_matrix = np.identity(4, dtype=np.float32)
    rot_matrix[0,0] = math.cos(angle)
    rot_matrix[0,2] = math.sin(angle)
    rot_matrix[2,0] = -math.sin(angle)
    rot_matrix[2,2] =  math.cos(angle)
    return my_glMultiplyMatricesf(in_matrix, rot_matrix)

def my_glRotateZf(in_matrix, angle):
    angle = angle*math.pi/180.0
    rot_matrix = np.identity(4, dtype=np.float32)
    rot_matrix[0,0] = math.cos(angle)
    rot_matrix[1,0] = math.sin(angle)
    rot_matrix[0,1] = -math.sin(angle)
    rot_matrix[1,1] =  math.cos(angle)
    return my_glMultiplyMatricesf(in_matrix, rot_matrix)

def my_glPerspectivef(fovy, aspect, z_near, z_far):
    assert(aspect>0)
    assert(z_far>z_near)
    f = np.float32(1.0/(math.tan(fovy*math.pi/180.0)))
    pers_matrix = np.zeros((4,4), dtype=np.float32)
    pers_matrix[0,0] = f/aspect
    pers_matrix[1,1] = f
    pers_matrix[2,2] = (z_near+z_far)/(z_near-z_far)
    pers_matrix[3,2] = 2*z_near*z_far/(z_near-z_far)
    pers_matrix[2,3] = -1
    return pers_matrix

def my_glScalef(in_matrix, x_scale, y_scale, z_scale):
    x_scale = np.float32(x_scale)
    y_scale = np.float32(y_scale)
    z_scale = np.float32(z_scale)
    scale_matrix = np.identity(4, dtype=np.float32)
    scale_matrix[0,0] = x_scale
    scale_matrix[1,1] = y_scale
    scale_matrix[2,2] = z_scale
    return my_glMultiplyMatricesf(in_matrix, scale_matrix)

def my_glTranslatef(orig_matrix, position):
    trans_matrix = np.identity(4, dtype=np.float32)
    trans_matrix[3,:3] = position
    return my_glMultiplyMatricesf(orig_matrix, trans_matrix)

def my_glMultiplyMatricesf(mat1, mat2):
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
    vector = np.array(dir_vec, dtype=np.float32)
    assert(np.linalg.norm(vector)>0.0)
    angle = angle*math.pi/180.0
    x,y,z = vector/np.linalg.norm(vector)
    c = math.cos(angle)
    s = math.sin(angle)
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

def unit_vector(vector):
    """ Returns the unit vector of the vector.
    """
    return vector / np.linalg.norm(vector)

def get_angle(vecA, vecB):
    """ Return the angle in degrees of two vectors.
    """
    vecA_u = unit_vector(vecA)
    vecB_u = unit_vector(vecB)
    return np.degrees(np.arccos(np.clip(np.dot(vecA_u, vecB_u), -1.0, 1.0)))

def get_euclidean(pa, pb):
    """ Returns the distance between two points in R3
    """
    import math
    if int(len(pa)) == 1:
        pa = [pa[0], 0.0, 0.0]
    if int(len(pa)) == 2:
        pa = [pa[0], pa[1], 0.0]
    if int(len(pb)) == 1:
        pb = [pb[0], 0.0, 0.0]
    if int(len(pb)) == 2:
        pb = [pb[0], pb[1], 0.0]
    return math.sqrt((pb[0]-pa[0])**2 + (pb[1]-pa[1])**2 + (pb[2]-pa[2])**2)

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

#################### NOT RELIABLE FUNCTIONS, NEEDS REVISION ####################

#def my_gluLookAt(in_matrix, eye, target, up):
    #forward = target - eye
    #forward = forward/np.linalg.norm(forward)
    #side = np.cross(forward, up)
    #side = side/np.linalg.norm(side)
    #up = np.cross(side, forward)
    #temp_matrix = np.identity(4, dtype=np.float32)
    #temp_matrix[:3,0] = side
    #temp_matrix[:3,1] = up
    #temp_matrix[:3,2] = -forward
    #result_matrix = my_glTranslatef(temp_matrix, -eye)
    #return result_matrix

def my_gluPerspective(fov, aspect, z_near, z_far):
    y_max = np.float32(z_near*math.tan(fov*math.pi/180.0))
    x_max = np.float32(y_max*aspect)
    return my_gluFrustum(-x_max, x_max, -y_max, y_max, z_near, z_far)

def my_gluFrustum(left, right, bottom, top, near, far):
    frust = np.zeros((4,4), dtype=np.float32)
    frust[0,0] = np.float32((2*near)/(right-left))
    frust[1,1] = np.float32((2*near)/(top-bottom))
    frust[2,0] = np.float32((right+left)/(right-left))
    frust[2,1] = np.float32((top+bottom)/(top-bottom))
    frust[2,2] = np.float32((-far-near)/(far-near))
    frust[2,3] = np.float32(-1)
    frust[3,2] = np.float32((-2*near*far)/(far-near))
    return frust.T

#def my_gluFrustumf(left, right, bottom, top, near, far):
    #frust = np.zeros((4,4), dtype=np.float32)
    #frust[0,0] = np.float32((2*near)/(right-left))
    #frust[1,1] = np.float32((2*near)/(top-bottom))
    #frust[2,0] = np.float32((right+left)/(right-left))
    #frust[2,1] = np.float32((top+bottom)/(top-bottom))
    #frust[2,2] = np.float32((-far-near)/(far-near))
    #frust[2,3] = np.float32(-1)
    #frust[3,2] = np.float32((-2*near*far)/(far-near))
    #return frust
