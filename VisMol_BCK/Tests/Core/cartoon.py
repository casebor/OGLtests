#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2021 Carlos Eduardo Sequeiros Borja <carseq@amu.edu.pl>
#  

import numpy as np

p = 0.6;
q = 0.8071;
COIL_POINTS = np.array([[ -p, -p, 0], [p, -p, 0], [p, p, 0], [-p, p, 0]], dtype=np.float32)

HELIX_POINTS = np.array([[-6.0 * p, -0.9 * q, 0], [-5.8 * p, -1.0 * q, 0],
                         [ 5.8 * p, -1.0 * q, 0], [ 6.0 * p, -0.9 * q, 0],
                         [ 6.0 * p,  0.9 * q, 0], [ 5.8 * p,  1.0 * q, 0],
                         [-5.8 * p,  1.0 * q, 0], [-6.0 * p,  0.9 * q, 0]], dtype=np.float32)

ARROW_POINTS = np.array([[-10.0 * p, -0.9 * q, 0], [ -9.8 * p, -1.0 * q, 0],
                         [  9.8 * p, -1.0 * q, 0], [ 10.0 * p, -0.9 * q, 0],
                         [ 10.0 * p,  0.9 * q, 0], [  9.8 * p,  1.0 * q, 0],
                         [ -9.8 * p,  1.0 * q, 0], [-10.0 * p,  0.9 * q, 0]], dtype=np.float32)

arcDetail = 2.0
splineDetail = 5

def cubic_hermite_interpolate(p_k1, tan_k1, p_k2, tan_k2, t):
    p = np.zeros(3, dtype=np.float32)
    tt = t * t
    tmt_t = 3.0 - 2.0 * t
    h01 = tt * tmt_t
    h00 = 1.0 - h01
    h10 = tt * (t - 2.0) + t
    h11 = tt * (t - 1.0)
    p[:] = p_k1[:]
    p*= h00
    p += tan_k1 * h10
    p += p_k2 * h01
    p += tan_k2 * h11
    return p

def catmull_rom_spline(points, num_points, subdivs, strength=0.5, circular=False):
    if circular:
        out_len = num_points * subdivs
    else:
        out_len = (num_points - 1) * subdivs + 1
    out = np.zeros([out_len, 3], dtype=np.float32)
    index = 0
    dt = 1.0 / subdivs
    tan_k1 = np.zeros(3, dtype=np.float32)
    tan_k2 = np.zeros(3, dtype=np.float32)
    p_k1 = np.zeros(3, dtype=np.float32)
    p_k2 = np.zeros(3, dtype=np.float32)
    p_k3 = np.zeros(3, dtype=np.float32)
    p_k4 = np.zeros(3, dtype=np.float32)
    p_k2[:] = points[0,:]
    p_k3[:] = points[1,:]
    if circular:
        p_k1[:] = points[-1,:]
        tan_k1[:] = p_k3 - p_k1
        tan_k1 *= strength
    else:
        p_k1[:] = points[0,:]
    i = 1
    e = num_points - 1
    while i < e:
        p_k4[:] = points[i+1,:]
        tan_k2[:] = p_k4 - p_k2
        tan_k2 *= strength
        for j in range(subdivs):
            out[index,:] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
            index += 1
        p_k1[:] = p_k2[:]
        p_k2[:] = p_k3[:]
        p_k3[:] = p_k4[:]
        tan_k1[:] = tan_k2[:]
        i += 1
    if circular:
        p_k4[0] = points[0,0]
        p_k4[1] = points[0,1]
        p_k4[2] = points[1,0]
        tan_k1 = p_k4 - p_k2
        tan_k1 *= strength
    else:
        tan_k1 = np.zeros(3, dtype=np.float32)
    for j in range(subdivs):
        out[index] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
        index += 1
    if not circular:
        out[index] = points[num_points-1:num_points]
        return out
    p_k1[:] = p_k2[:]
    p_k2[:] = p_k3[:]
    p_k3[:] = p_k4[:]
    tan_k1[:] = tan_k2[:]
    p_k4[:] = points[1,:]
    tan_k1 = p_k4 - p_k2
    tan_k1 *= strength
    for j in range(subdivs):
        out[index] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
        index += 1
    return out


# calphas = np.loadtxt("cas.txt")
# print(calphas)
# calphas = calphas.flatten()
# spline = catmull_rom_spline(np.copy(calphas), calphas.shape[0], 1)
# print(spline)

def get_rotmat(angle, dir_vec):
    # vector = np.array(dir_vec, dtype=np.float32)
    assert(np.linalg.norm(dir_vec)>0.0)
    # angle = angle*np.pi/180.0
    # x, y, z = vector/np.linalg.norm(vector)
    x, y, z = dir_vec
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
    return rot_matrix

def get_norm_vector(p1, p2, p3, p4):
    com1234 = (p1 + p2 + p3 + p4) / 4.0
    com12 = (p1 + p2) / 2.0
    com23 = (p2 + p3) / 2.0
    com34 = (p3 + p4) / 2.0
    # com14 = (p1 + p4) / 2.0
    vec1 = com23 - com1234
    vec2 = com34 - com1234
    vec3 = np.cross(vec1, vec2)
    vec3 /= np.linalg.norm(vec3)
    pointA = com1234 + vec3 * np.linalg.norm(com34-com1234)
    pointB = com1234 - vec3 * np.linalg.norm(com34-com1234)
    com12B = (com12 + pointB) / 2.0
    com34A = (com34 + pointA) / 2.0
    dir_vec = com34A - com12B
    return dir_vec / np.linalg.norm(dir_vec)

def get_coil(spline, spline_detail):
    # TODO: this should return the coil points, but for now is returning the
    # entry points
    return spline

def get_helix(spline, spline_detail):
    out = []
    normal = np.zeros(3, dtype=np.float32)
    for i in range(spline.shape[0] - spline_detail*3):
        normal += get_norm_vector(spline[i], spline[i+spline_detail],
                 spline[i+spline_detail*2], spline[i+spline_detail*3])
        normal /= np.linalg.norm(normal)
        dir_vec = spline[i+1] - spline[i]
        side_vec = np.cross(dir_vec, normal)
        side_vec /= np.linalg.norm(side_vec)
        out.append(spline[i]+normal-side_vec*.1)
        out.append(spline[i]+normal+side_vec*.1)
        out.append(spline[i]+side_vec*.2)
        out.append(spline[i]-normal+side_vec*.1)
        out.append(spline[i]-normal-side_vec*.1)
        out.append(spline[i]-side_vec*.2)
    for i in range(spline.shape[0] - spline_detail*3, spline.shape[0]):
        if i < spline.shape[0] - 1:
            dir_vec = spline[i+1] - spline[i]
            side_vec = np.cross(dir_vec, normal)
            side_vec /= np.linalg.norm(side_vec)
        out.append(spline[i]+normal-side_vec*.1)
        out.append(spline[i]+normal+side_vec*.1)
        out.append(spline[i]+side_vec*.2)
        out.append(spline[i]-normal+side_vec*.1)
        out.append(spline[i]-normal-side_vec*.1)
        out.append(spline[i]-side_vec*.2)
    return np.array(out, dtype=np.float32)

def get_beta(spline, spline_detail):
    pass

def cartoon(calphas_file="cas.txt", spline_detail=5):
    sd = spline_detail
    calphas = np.loadtxt(calphas_file)
    spline = catmull_rom_spline(np.copy(calphas), calphas.shape[0], sd)
    # TODO: function to calculate the boundaries for secondary structures.
    # This list contains the indices of the residues that are alpha helices in
    # zero-based indexing.
    secstruc = [(0, 0, 2), (1, 2, 13), (0, 13, 19), (1, 19, 34)]
    output = np.zeros(3, dtype=np.float32)
    for ss in secstruc:
        if ss[0] == 0:
            output = np.vstack((output, get_coil(spline[ss[1]*sd:ss[2]*sd], sd)))
        elif ss[0] == 1:
            output = np.vstack((output, get_helix(spline[ss[1]*sd:ss[2]*sd], sd)))
        elif ss[0] == 2:
            output = np.vstack((output, get_beta(spline[ss[1]*sd:ss[2]*sd], sd)))
    # print(calphas.shape, spline.shape)
    # print(calphas)
    output = output[1:]
    # print(output)
    # vec_dir = np.array([0.0, 0.0, 1.0], dtype=np.float32)
    # for i in range(spline.shape[0]):
    #     if (i%spline_detail == 0) and ((i//spline_detail) < (calphas.shape[0]-4)):
    #         vec_dir = spline[i+spline_detail*4] - spline[i]
    #         vec_dir /= np.linalg.norm(vec_dir)
    #     angle = np.degrees(np.arccos(np.dot([-1.0, 0.0, 0.0], vec_dir)))
    #     normal = np.cross([-1.0, 0.0, 0.0], vec_dir)
    #     rotmat = get_rotmat(angle, normal)[:3,:3]
    #     for point in HELIX_POINTS:
    #         output.append(np.matmul(rotmat, point) + spline[i])
    # return np.array(output)
    return output

# print(cartoon())
