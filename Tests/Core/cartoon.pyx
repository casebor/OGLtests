#!python
#cython: language_level=3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2022 Carlos Eduardo Sequeiros Borja <carseq@amu.edu.pl>
#  

cimport numpy
import cython
import numpy as np


cpdef float distance(float[:] a, float[:] b):
    cdef cython.float d, x, y, z
    x = a[0] - b[0]
    y = a[1] - b[1]
    z = a[2] - b[2]
    d = x*x + y*y + z*z
    return np.sqrt(d)

cpdef bint is_strand(float[:,:] calphas, Py_ssize_t ca_i):
    strand_dists = [6.1, 10.4, 13.0]
    cdef cython.float b_delta = 1.42
    cdef Py_ssize_t i, j
    for i in range(ca_i-2, ca_i):
        for j in range(2, 5):
            dist = distance(calphas[i], calphas[i+j])
            if abs(dist - strand_dists[j-2]) > b_delta:
                return False
    return True

cpdef bint is_helix(float[:,:] calphas, Py_ssize_t ca_i):
    helix_dists = [5.45, 5.18, 6.37]
    cdef cython.float h_delta = 2.1
    cdef Py_ssize_t i, j
    for i in range(ca_i-2, ca_i):
        for j in range(2, 5):
            dist = distance(calphas[i], calphas[i+j])
            if abs(dist - helix_dists[j-2]) > h_delta:
                return False
    return True

cpdef calculate_secondary_structure(float[:,:] calphas):
    assert calphas.shape[0] > 6
    cdef Py_ssize_t camax = calphas.shape[0]
    cdef Py_ssize_t i, j
    cdef cython.float dist
    ss = "CC"
    for i in range(2, camax-4):
        if is_helix(calphas, i):
            ss += "H"
        elif is_strand(calphas, i):
            ss += "S"
        else:
            ss += "C"
    ss += "CCCC"
    print(ss)


cpdef cython.float[:] cubic_hermite_interpolate(p_k1, tan_k1, p_k2, tan_k2, t):
    result = np.copy(p_k1)
    cdef cython.float tt, tmt_t, h00, h01, h10, h11
    tt = t * t
    tmt_t = 3.0 - 2.0 * t
    h01 = tt * tmt_t
    h00 = 1.0 - h01
    h10 = tt * (t - 2.0) + t
    h11 = tt * (t - 1.0)
    result *= h00
    result += tan_k1 * h10
    result += p_k2 * h01
    result += tan_k2 * h11
    return result

cpdef cython.float[:,:] catmull_rom_spline(float[:,:] points, int  num_points, int subdivs, float strength=0.6, bint circular=False):
    cdef cython.int out_len
    if circular:
        out_len = num_points * subdivs
    else:
        out_len = (num_points - 1) * subdivs + 1
    out = np.empty([out_len, 3], dtype=np.float32)
    cdef cython.float[:,:] out_view = out
    cdef Py_ssize_t index = 0
    cdef cython.float dt = 1.0 / subdivs
    tan_k1 = np.empty(3, dtype=np.float32)
    tan_k2 = np.empty(3, dtype=np.float32)
    p_k1 = np.empty(3, dtype=np.float32)
    p_k2 = np.copy(points[0])
    p_k3 = np.copy(points[1])
    p_k4 = np.empty(3, dtype=np.float32)
    if circular:
        p_k1[:] = points[-1,:]
        tan_k1[:] = p_k3 - p_k1
        tan_k1 *= strength
    else:
        p_k1[:] = points[0,:]
    cdef Py_ssize_t i = 1
    while i < num_points - 1:
        p_k4[:] = points[i+1,:]
        tan_k2[:] = p_k4 - p_k2
        tan_k2 *= strength
        for j in range(subdivs):
            out_view[index,:] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
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
        tan_k1[:] = [0,0,0]
    for j in range(subdivs):
        out_view[index,:] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
        index += 1
    if not circular:
        out_view[index] = points[-1]
        return out
    p_k1[:] = p_k2[:]
    p_k2[:] = p_k3[:]
    p_k3[:] = p_k4[:]
    tan_k1[:] = tan_k2[:]
    p_k4[:] = points[1,:]
    tan_k1 = p_k4 - p_k2
    tan_k1 *= strength
    for j in range(subdivs):
        out_view[index,:] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
        index += 1
    return out


def get_rotmat3f(angle, dir_vec):
    # vector = np.array(dir_vec, dtype=np.float32)
    assert(np.linalg.norm(dir_vec)>0.0)
    # angle = angle*np.pi/180.0
    # x, y, z = vector/np.linalg.norm(vector)
    x, y, z = dir_vec
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

def get_strand_vectors(p1, p2, p3):
    com123 = (p1 + p2 + p3) / 3.0
    com12 = (p1 - p2) / 2.0
    com23 = (p2 - p3) / 2.0
    vec1 = com123 - com12
    vec1 /= np.linalg.norm(vec1)
    vec2 = com123 - com23
    vec2 /= np.linalg.norm(vec2)
    up_vec = vec1 + vec2
    up_vec /= np.linalg.norm(up_vec)
    vec3 = p3 - p1
    side_vec = np.cross(up_vec, vec3)
    side_vec /= np.linalg.norm(side_vec)
    return up_vec, side_vec

def get_helix_vector(p1, p2, p3, p4):
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

def get_coil(spline, coil_rad=0.2, color=None):
    if color is None:
        color = [0.0, 1.0, 0.0]
    coil_points = np.array([[ 0.5, 0.866, 0.0], [ 1.0, 0.0, 0.0],
                            [ 0.5,-0.866, 0.0], [-0.5,-0.866, 0.0],
                            [-1.0, 0.0, 0.0], [-0.5, 0.866, 0.0]], dtype=np.float32)
    coil_points *= coil_rad
    coords = np.zeros([spline.shape[0]*6, 3], dtype=np.float32)
    normals = np.zeros([spline.shape[0]*6, 3], dtype=np.float32)
    colors = np.array([color]*spline.shape[0]*6, dtype=np.float32)
    for i in range(spline.shape[0] - 1):
        dir_vec = spline[i+1] - spline[i]
        dir_vec /= np.linalg.norm(dir_vec)
        align_vec = np.cross([0.0, 0.0, 1.0], dir_vec)
        align_vec /= np.linalg.norm(align_vec)
        angle = np.arccos(np.dot([0.0, 0.0, 1.0], dir_vec))
        rotmat = get_rotmat3f(angle, align_vec)
        for j, point in enumerate(coil_points):
            coords[i*6+j,:] = np.matmul(rotmat, point) + spline[i]
            normals[i*6+j,:] = coords[i*6+j,:] - spline[i]
    for i, point in enumerate(coil_points):
        coords[-6+i,:] = np.matmul(rotmat, point) + spline[-1]
        normals[-6+i,:] = coords[-6+i,:] - spline[-1]
    return coords, normals, colors

def get_helix(spline, spline_detail, helix_rad=0.2, color=None):
    if color is None:
        color = [1.0, 0.0, 0.0]
    coords = np.zeros([spline.shape[0]*6, 3], dtype=np.float32)
    normals = np.zeros([spline.shape[0]*6, 3], dtype=np.float32)
    colors = np.array([color]*coords.shape[0], dtype=np.float32)
    helix_vec = np.zeros(3, dtype=np.float32)
    for i in range(spline.shape[0] - spline_detail*3):
        helix_vec += get_helix_vector(spline[i], spline[i+spline_detail],
                 spline[i+spline_detail*2], spline[i+spline_detail*3])
        helix_vec /= np.linalg.norm(helix_vec)
        dir_vec = spline[i+1] - spline[i]
        side_vec = np.cross(dir_vec, helix_vec)
        side_vec /= np.linalg.norm(side_vec)
        coords[i*6] = spline[i] + helix_vec + side_vec * helix_rad / 2.0
        coords[i*6+1] = spline[i] + side_vec * helix_rad
        coords[i*6+2] = spline[i] - helix_vec + side_vec * helix_rad / 2.0
        coords[i*6+3] = spline[i] - helix_vec - side_vec * helix_rad / 2.0
        coords[i*6+4] = spline[i] - side_vec * helix_rad
        coords[i*6+5] = spline[i] + helix_vec - side_vec * helix_rad / 2.0
        for j in range(6):
            normals[i*6+j] = coords[i*6+j] - spline[i]
    for i in range(spline.shape[0] - spline_detail*3, spline.shape[0]):
        if i < spline.shape[0] - 1:
            dir_vec = spline[i+1] - spline[i]
            side_vec = np.cross(dir_vec, helix_vec)
            side_vec /= np.linalg.norm(side_vec)
        coords[i*6] = spline[i] + helix_vec + side_vec * helix_rad / 2.0
        coords[i*6+1] = spline[i] + side_vec * helix_rad
        coords[i*6+2] = spline[i] - helix_vec + side_vec * helix_rad / 2.0
        coords[i*6+3] = spline[i] - helix_vec - side_vec * helix_rad / 2.0
        coords[i*6+4] = spline[i] - side_vec * helix_rad
        coords[i*6+5] = spline[i] + helix_vec - side_vec * helix_rad / 2.0
        for j in range(6):
            normals[i*6+j] = coords[i*6+j] - spline[i]
    return coords, normals, colors

def get_strand(orig_spline, spline_detail, strand_rad=0.5, color=None):
    if color is None:
        color = [1.0, 1.0, 0.0]
    p1 = orig_spline[0]
    p2 = np.zeros(3, dtype=np.float32)
    for i in range(0, orig_spline.shape[0], spline_detail):
        p2 += orig_spline[i]
    p2 /= (orig_spline.shape[0]/spline_detail)
    p3 = orig_spline[-1]
    spline = bezier_curve(p1, p2, p3, orig_spline.shape[0])
    coords = np.zeros([spline.shape[0]*4, 3], dtype=np.float32)
    normals = np.zeros([spline.shape[0]*4, 3], dtype=np.float32)
    colors = np.array([color]*coords.shape[0], dtype=np.float32)
    strand_up = np.zeros(3, dtype=np.float32)
    strand_side = np.zeros(3, dtype=np.float32)
    strand_dir = 1
    for i in range(spline.shape[0] - spline_detail):
        if i < spline.shape[0] - spline_detail * 2 and i % spline_detail == 0:
            _vecs = get_strand_vectors(spline[i], spline[i+spline_detail], spline[i+spline_detail*2])
            strand_up += _vecs[0] * strand_dir
            # strand_side += _vecs[1] * strand_dir
            strand_up /= np.linalg.norm(strand_up)
            strand_side = np.cross(spline[i+1]-spline[i], strand_up)
            strand_side /= np.linalg.norm(strand_side)
            # strand_dir *= -1
        coords[i*4] = spline[i] + strand_up * strand_rad / 1.5 + strand_side * strand_rad
        coords[i*4+1] = spline[i] - strand_up * strand_rad / 1.5 + strand_side * strand_rad
        coords[i*4+2] = spline[i] - strand_up * strand_rad / 1.5 - strand_side * strand_rad
        coords[i*4+3] = spline[i] + strand_up * strand_rad / 1.5 - strand_side * strand_rad
        for j in range(4):
            normals[i*4+j] = coords[i*4+j] - spline[i]
    arrow_rads = np.linspace(strand_rad*2.5, 0.1, spline_detail)
    arros_inds = np.arange(spline.shape[0] - spline_detail, spline.shape[0], dtype=np.uint32)
    for i, r in zip(arros_inds, arrow_rads):
        # _vecs = get_strand_vectors(spline[i], spline[i+spline_detail], spline[i+spline_detail*2])
        # strand_up += _vecs[0] * strand_dir
        # strand_side += _vecs[1] * strand_dir
        # strand_up /= np.linalg.norm(strand_up)
        # strand_side /= np.linalg.norm(strand_side)
        # strand_dir *= -1
        coords[i*4] = spline[i] + strand_up * strand_rad / 1.5 + strand_side * r
        coords[i*4+1] = spline[i] - strand_up * strand_rad / 1.5 + strand_side * r
        coords[i*4+2] = spline[i] - strand_up * strand_rad / 1.5 - strand_side * r
        coords[i*4+3] = spline[i] + strand_up * strand_rad / 1.5 - strand_side * r
        for j in range(4):
            normals[i*4+j] = coords[i*4+j] - spline[i]
    return coords, normals, colors

def get_indexes(num_points, points_perring, offset, is_strand=False):
    size_i = (num_points//points_perring)*2*6*3 + 2*4*3
    indexes = np.zeros(size_i, dtype=np.uint32)
    # Add indices for the initial cap
    if is_strand:
        indexes[:6] = [0,1,2, 2,3,0]
    else:
        indexes[:12] = [0,1,2, 2,3,4, 4,5,0, 0,2,4]
    i = 12
    for r in range(num_points//points_perring-1):
        for p in range(points_perring-1):
            indexes[i] = r*points_perring+p
            indexes[i+1] = r*points_perring+p+1
            indexes[i+2] = (r+1)*points_perring+p
            i += 3
        indexes[i] = (r+1)*points_perring - 1
        indexes[i+1] = r*points_perring
        indexes[i+2] = (r+2)*points_perring - 1
        i += 3
        for p in range(points_perring-1):
            indexes[i] = (r+1)*points_perring+p
            indexes[i+1] = (r+1)*points_perring+p+1
            indexes[i+2] = r*points_perring+p+1
            i += 3
        indexes[i] = (r+2)*points_perring - 1
        indexes[i+1] = (r+1)*points_perring
        indexes[i+2] = r*points_perring
        i += 3
    a = num_points - points_perring
    if is_strand:
        indexes[-6:] = [a,a+1,a+2, a+2,a+3,a]
    else:
        indexes[-12:] = [a,a+1,a+2, a+2,a+3,a+4, a+4,a+5,a, a,a+2,a+4]
    indexes += offset
    return indexes


def make_normals(coords, indexes):
    normals = np.zeros(coords.shape, dtype=np.float32)
    for i in range(0, indexes.shape[0], 3):
        vec1 = coords[indexes[i+1]] - coords[indexes[i]]
        vec2 = coords[indexes[i+2]] - coords[indexes[i]]
        normal = np.cross(vec1, vec2)
        normal /= np.linalg.norm(normal)
        normals[indexes[i]] = np.copy(normal)
        normals[indexes[i+1]] = np.copy(normal)
        normals[indexes[i+2]] = np.copy(normal)
    return normals

def bezier_curve(p1, p2, p3, bezier_detail):
    points_mat = np.array([p1, p2, p3], dtype=np.float32)
    points = np.zeros([bezier_detail, 3], dtype=np.float32)
    for i, t in enumerate(np.linspace(0, 1, bezier_detail)):
        vec_t = np.array([(1-t)*(1-t), 2*t-2*t*t, t*t], dtype=np.float32)
        points[i,:] = np.matmul(vec_t, points_mat)
    return points


cpdef cartoon(float[:,:] bbone, float[:,:] calphas, int spline_detail=3, list ss_assigned=None):
    cdef Py_ssize_t sd = spline_detail
    spline = catmull_rom_spline(np.copy(calphas), calphas.shape[0], sd, strength=0.9)
    spline = np.array(spline, dtype=np.float32)
    # return spline
    secstruc = [(0,0,2), (1,2,13), (0,13,16), (2,16,20,np.identity(3)),
                (0,20,22), (2,22,26,np.identity(3)), (0,26,27)]
    # secstruc = [SS("coil",0,2,None), SS("helix",2,13,None), SS("coil",13,16,None),
    #             SS("strand",16,20,np.identity(3)), SS("coil",20,22,None),
    #             SS("strand",22,26,np.identity(3)), SS("coil",26,27,None)]
    
    cdef list coords = []
    cdef list normals = []
    cdef list colors = []
    cdef list indexes = []
    
    for ss in secstruc:
        if ss[0] == 0:
            if ss[1] == 0:
                if ss[2] == calphas.shape[0]:
                    data = get_coil(spline[ss[1]*sd:ss[2]*sd])
                else:
                    data = get_coil(spline[ss[1]*sd:ss[2]*sd+1])
            else:
                if ss[2] == calphas.shape[0]:
                    data = get_coil(spline[ss[1]*sd-1:ss[2]*sd])
                else:
                    data = get_coil(spline[ss[1]*sd-1:ss[2]*sd+1])
            
            _inds = get_indexes(data[0].shape[0], 6, len(coords)-1)
            indexes.extend(_inds)
            coords.extend(data[0])
            normals.extend(data[1])
            colors.extend(data[2])
        elif ss[0] == 1:
            # _inds = get_indexes((ss[2] - ss[1])*sd, 6, len(coords)-1)
            # indexes.extend(_inds)
            data = get_helix(spline[ss[1]*sd:ss[2]*sd], sd)
            _inds = get_indexes(data[0].shape[0], 6, len(coords)-1)
            indexes.extend(_inds)
            coords.extend(data[0])
            normals.extend(data[1])
            colors.extend(data[2])
        elif ss[0] == 2:
            # _inds = get_indexes((ss[2] - ss[1])*sd, 6, len(coords)-1)
            # indexes.extend(_inds)
            data = get_strand(spline[ss[1]*sd:ss[2]*sd], sd)
            _inds = get_indexes(data[0].shape[0], 4, len(coords)-1, is_strand=True)
            indexes.extend(_inds)
            coords.extend(data[0])
            normals.extend(data[1])
            colors.extend(data[2])
    normals = make_normals(coords, indexes)
    print("len:")
    print(spline.shape, coords.shape, normals.shape, colors.shape, indexes.shape)
    return coords, normals, indexes, colors



'''

# def calculate_secondary_structure(visObj):
#     """
#         First, the distances d2i, d3i and d4i between the (i - 1)th
#         residue and the (i + 1)th, the (i + 2)th and the (i + 3)th,
#         respectively, are computed from the cartesian coordinates
#         of the Ca carbons, as well as the angle ti and dihedral angle
#         ai defined by the Ca carbon triplet (i - 1, i , i + 1) and
#         quadruplet (i - 1, i, i + 1, i + 2), respectively.
        
        
#         Assignment parameters
#                                    Secondary structure
                                   
#                                    Helix        Strand
                                   
#         Angle T (°)               89 ± 12       124 ± 14
#         Dihedral angle a (°)      50 ± 20      -170 ± 4 5
                                               
#         Distance d2 (A)           5.5 ± 0.5    6.7 ± 0.6
#         Distance d3 (A)           5.3 ± 0.5    9.9 ± 0.9
#         Distance d4 (A)           6.4 ± 0.6    12.4 ± 1.1


#     """
#     if visObj.c_alpha_bonds == [] or visObj.c_alpha_atoms == []:
#         visObj.get_backbone_indexes()
    
#     for atom in visObj.c_alpha_atoms:
#         print(atom.index, atom.name, atom.bonds_indexes, atom.bonds)
    

#     size = len(visObj.c_alpha_bonds)
#     SSE_list  = "C"
#     SSE_list2 = []
    
    
#     block     = [0,0,1]
#     SS_before = 1
#     for i in range(1,size -2):
        
#         CA0 = visObj.c_alpha_bonds[i-1].atom_i # i - 1
#         CA1 = visObj.c_alpha_bonds[i-1].atom_j # i
        
#         CA2 = visObj.c_alpha_bonds[i].atom_i   # i
#         CA3 = visObj.c_alpha_bonds[i].atom_j   # i + 1
                                               
#         CA4 = visObj.c_alpha_bonds[i+1].atom_i # i + 1
#         CA5 = visObj.c_alpha_bonds[i+1].atom_j # i + 2
                                               
#         CA6 = visObj.c_alpha_bonds[i+2].atom_i # i + 2
#         CA7 = visObj.c_alpha_bonds[i+2].atom_j # i + 3
                                               
#         #CA8 = visObj.c_alpha_bonds[i+3].atom_i # i + 3 
#         #CA9 = visObj.c_alpha_bonds[i+3].atom_j #


#         if CA1 == CA2 and CA3 == CA4 and CA5 == CA6:
#             #print ("CA1 = CA2")
            
#             # distances
#             d2i  = CA0.coords(), CA3.coords()
#             d2i  = np.linalg.norm(d2i)
            
#             d3i  = CA0.coords(), CA5.coords()
#             d3i  = np.linalg.norm(d3i)
            
#             d4i  = CA0.coords(), CA7.coords()
#             d4i  = np.linalg.norm(d4i)
            
#             # angle
#             v0   = CA1.coords(),CA0.coords()
#             v1   = CA1.coords(), CA3.coords()
            
#             ti   = 57.295779513*(mop.angle(v0, v1))
            
#             # dihedral 
#             ai   = 57.295779513*(mop.dihedral(CA0.coords(), CA1.coords(), CA3.coords(), CA5.coords()))
            
            
            
#             SS = None
#             SS_char = None
            
#             if 77.0 <= ti <= 101 and 30 <= ai <= 70:
#                 #print(CA1.resi, CA1.name, CA1.resn, CA1.name, "H", d2i, d3i, d4i, ti,  ai)
#                 SS = 1
#                 SS_char = "H"

#             elif 5.0 <= d2i <= 6.0 and 4.8 <= d3i <= 5.8 and 5.8 <= d4i <= 7.0:
#                 SS = 1
#                 SS_char = "H"
            
#             elif 110.0 <= ti <= 138 and -215 <= ai <= -125:
#                 SS = 2
#                 SS_char = "S"
            
#             elif 6.1 <= d2i <= 7.3 and 9.0 <= d3i <= 10.8 and 11.3 <= d4i <= 13.5:
#                 SS = 1
#                 SS_char = "S"
            
#             """
#             if 5.0 <= d2i <= 6.0:
#                 #print("d2i", d2i)
                
#                 if 4.8 <= d3i <= 5.8:
#                     #print("d3i", d3i)

#                     if 5.8 <= d4i <= 7.0:
#                         #print("d4i", d4i)

#                         if 77.0 <= ti <= 101:
                            
#                             if 30 <= ai <= 70:
#                                 print(CA1.resi, CA1.name, CA1.resn, CA1.name, "H", d2i, d3i, d4i, ti,  ai)
#                                 SS = "H"
      
                     
#             if 6.1 <= d2i <= 7.3:
#                 #print("d2i", d2i)
                
#                 if 9.0 <= d3i <= 10.8:
#                     #print("d3i", d3i)

#                     if 11.3 <= d4i <= 13.5:
#                         #print("d4i", d4i)

#                         if 110.0 <= ti <= 138:
#                             if -215 <= ai <= -125:
#                                 print(CA1.resi, CA1.name, CA1.resn, CA1.name, "S", d2i, d3i, d4i, ti,  ai)
#                                 SS = "S"
#             """
            
#             if SS:
#                 pass
#             else:
#                 SS = 0 
#                 SS_char = "C"
#             print(CA1.resi, CA1.name, CA1.resn, CA1.name, SS, d2i, d3i, d4i, ti,  ai)
            
#             SSE_list += SS_char

            
#     SSE_list += "CCC"
#     print(SSE_list, len(SSE_list))
#     SSE_list = SSE_list.replace("CHCHC",  "CCCC")
#     SSE_list = SSE_list.replace("CHC",  "CCC")
#     SSE_list = SSE_list.replace("HCH",  "HHH")
#     SSE_list = SSE_list.replace("CHS",  "CCS")

#     SSE_list = SSE_list.replace("CHHC", "CCCC")
#     SSE_list = SSE_list.replace("CSSC", "CCCC")
#     SSE_list = SSE_list.replace("CSC",  "CCC")
#     SSE_list = SSE_list.replace("HSH",  "HHH")
#     SSE_list = SSE_list.replace("SHS",  "SSS")
#     SSE_list = SSE_list.replace("CHSC",  "CCCC")
#     print(SSE_list, len(SSE_list))
    
    
#     SSE_list2     = []
#     block         = [0,0,0]
#     SS_before     = "C"
    
#     counter = 1
#     for SS in SSE_list:
        
#         if SS == SS_before:
#             block[2] += 1
#         else:
#             SSE_list2.append(block)
#             SS_before = SS
#             print (block)
            
#             if SS == "C":
#                 SS_code = 0
            
#             elif SS == "H":
#                 SS_code = 1
            
#             else:
#                 SS_code = 2    
            
#             block = [SS_code, counter-1, counter]
            
#         counter += 1
#     SSE_list2.append(block)
#     print(SSE_list2)
#     return SSE_list2 

'''