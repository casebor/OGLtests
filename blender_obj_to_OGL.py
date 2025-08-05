#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  vaos.py
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
from sys import argv

def make_normals(coords, indexes):
    normals = []
    for i in range(0, indexes.shape[0], 3):
        vec1 = coords[indexes[i+1]] - coords[indexes[i]]
        vec2 = coords[indexes[i+2]] - coords[indexes[i+1]]
        normal = np.cross(vec1,vec2)
        normal /= np.linalg.norm(normal)
        normals.append(normal)
        normals.append(normal)
        normals.append(normal)
    return normals

def parse_obj(obj_filename):
    temp_v = []
    temp_n = []
    temp_uv = []
    indexes = []
    with open(obj_filename, "r") as objstream:
        for line in objstream:
            if line[:2] == "v ":
                chunks = line.strip().split()
                x = float(chunks[1])
                y = float(chunks[2])
                z = float(chunks[3])
                temp_v.append([x, y, z])
            elif line[:3] == "vt ":
                chunks = line.strip().split()
                u = float(chunks[1])
                v = float(chunks[2])
                temp_uv.append([u, v])
            elif line[:3] == "vn ":
                chunks = line.strip().split()
                x = float(chunks[1])
                y = float(chunks[2])
                z = float(chunks[3])
                temp_n.append([x, y, z])
            # elif line[:2] == "f ":
            #     chunks = line.strip().split()
            #     for i in range(1, len(chunks)-2):
            #         indexes.append([chunks[i], chunks[i+1], chunks[i+2]])
            elif line[:2] == "f ":
                chunks = line.strip().split()
                if len(chunks) == 4:
                    indexes.append([chunks[1], chunks[2], chunks[3]])
                elif len(chunks) == 5:
                    indexes.append([chunks[1], chunks[2], chunks[3]])
                    indexes.append([chunks[3], chunks[4], chunks[1]])
    vertices = []
    normals = []
    uv_coords = []
    for index in indexes:
        for point in index:
            i, j, k = [int(x)-1 for x in point.split("/")]
            vertices.append(temp_v[i])
            uv_coords.append(temp_uv[j])
            normals.append(temp_n[k])
    vertices = np.array(vertices ,dtype=np.float32)
    uv_coords = np.array(uv_coords ,dtype=np.float32)
    normals = np.array(normals, dtype=np.float32)
    indexes = np.arange(vertices.shape[0], dtype=np.uint32)
    com = np.mean(vertices, axis=0)
    vertices -= com
    # print(vertices.shape, normals.shape, uv_coords.shape, indexes.shape)
    return vertices, normals, uv_coords, indexes

def parse_obj_smooth(obj_filename):
    """ Here we asume that the vertices use always the same normal """
    vertices = []
    normals = []
    uv_coords = []
    indexes = []
    with open(obj_filename, "r") as objstream:
        for line in objstream:
            if line[:2] == "v ":
                chunks = line.strip().split()
                x = float(chunks[1])
                y = float(chunks[2])
                z = float(chunks[3])
                vertices.append([x, y, z])
            elif line[:3] == "vt ":
                chunks = line.strip().split()
                u = float(chunks[1])
                v = float(chunks[2])
                uv_coords.append([u, v])
            elif line[:3] == "vn ":
                chunks = line.strip().split()
                x = float(chunks[1])
                y = float(chunks[2])
                z = float(chunks[3])
                normals.append([x, y, z])
            elif line[:2] == "f ":
                chunks = line.strip().split()
                for i in range(1, len(chunks)-2):
                    for j in range(3):
                        a = int(chunks[i+j].split("/")[0])-1
                        indexes.append(a)
    vertices = np.array(vertices ,dtype=np.float32)
    uv_coords = np.array(uv_coords ,dtype=np.float32)
    normals = np.array(normals, dtype=np.float32)
    indexes = np.array(indexes, dtype=np.uint32)
    return vertices, normals, uv_coords, indexes


if __name__ == '__main__':
    coords, normals, uv_coords, indexes = parse_obj(argv[1])
    print(coords.shape)
    print(normals.shape)
    print(uv_coords.shape)
    print(indexes.shape)
