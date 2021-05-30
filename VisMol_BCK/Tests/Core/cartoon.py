#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2021 Carlos Eduardo Sequeiros Borja <carseq@amu.edu.pl>
#  

import numpy as np

p = 0.6;
q = 0.8071;
COIL_POINTS = [ -p, -p, 0, p, -p, 0, p, p, 0, -p, p, 0 ]

HELIX_POINTS = [
  -6.0 * p, -0.9 * q, 0,
  -5.8 * p, -1.0 * q, 0,

   5.8 * p, -1.0 * q, 0,
   6.0 * p, -0.9 * q, 0,

   6.0 * p,  0.9 * q, 0,
   5.8 * p,  1.0 * q, 0,

  -5.8 * p,  1.0 * q, 0,
  -6.0 * p,  0.9 * q, 0
]

ARROW_POINTS = [
 -10.0 * p, -0.9 * q, 0,
  -9.8 * p, -1.0 * q, 0,

   9.8 * p, -1.0 * q, 0,
  10.0 * p, -0.9 * q, 0,

  10.0 * p,  0.9 * q, 0,
   9.8 * p,  1.0 * q, 0,

  -9.8 * p,  1.0 * q, 0,
 -10.0 * p,  0.9 * q, 0
]

arcDetail = 2.0

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
    out_len *= 3
    out = np.zeros(out_len, dtype=np.float32)
    index = 0
    dt = 1.0 / subdivs
    tan_k1 = np.zeros(3, dtype=np.float32)
    tan_k2 = np.zeros(3, dtype=np.float32)
    p_k1 = np.zeros(3, dtype=np.float32)
    p_k2 = np.zeros(3, dtype=np.float32)
    p_k3 = np.zeros(3, dtype=np.float32)
    p_k4 = np.zeros(3, dtype=np.float32)
    p_k2[:] = points[:3]
    p_k3[:] = points[3:6]
    if circular:
        p_k1[:] = points[-3:]
        tan_k1[:] = p_k3 - p_k1
        tan_k1 *= strength
    else:
        p_k1 = points[:3]
    i = 1
    e = num_points - 1
    while i < e:
        p_k4[0] = points[(i+1)*3]
        p_k4[1] = points[(i+1)*3+1]
        p_k4[2] = points[(i+1)*3+2]
        tan_k2[:] = p_k4 - p_k2
        tan_k2 *= strength
        for j in range(subdivs):
            out[index:index+3] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
            index += 3
        p_k1[:] = p_k2[:]
        p_k2[:] = p_k3[:]
        p_k3[:] = p_k4[:]
        tan_k1[:] = tan_k2[:]
        i += 1
    if circular:
        p_k4[0] = points[0]
        p_k4[1] = points[1]
        p_k4[2] = points[3]
        tan_k1 = p_k4 - p_k2
        tan_k1 *= strength
    else:
        tan_k1 = np.zeros(3, dtype=np.float32)
    for j in range(subdivs):
        out[index:index+3] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
        index += 3
    if not circular:
        out[index:index+3] = points[(num_points-1)*3:(num_points-1)*3+3]
        return out
    p_k1[:] = p_k2[:]
    p_k2[:] = p_k3[:]
    p_k3[:] = p_k4[:]
    tan_k1[:] = tan_k2[:]
    p_k4[:] = points[3:6]
    tan_k1 = p_k4 - p_k2
    tan_k1 *= strength
    for j in range(subdivs):
        out[index:index+3] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
        index += 3
    return out

def smoother_3p():
    pass

calphas = np.loadtxt("cas.txt")
calphas = calphas.flatten()

spline = catmull_rom_spline(calphas, len(calphas)//3, 1)
print(calphas.shape, spline.shape)
print(calphas)
print(spline)