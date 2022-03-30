#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  OGLshaders.py
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


v_impostor_sph_BCK = """
#version 330
precision highp float;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec3 vert_color;
in float vert_radius;

uniform vec3 u_campos;

out vec3 geom_color;
out vec3 geom_coord;
out vec3 geom_center;
out vec3 geom_cam;
out float geom_radius;

void main() {
    geom_color = vert_color;
    geom_coord = (view_mat * model_mat * vec4(vert_coord, 1.0)).xyz;
    geom_center = (view_mat * model_mat * vec4(vert_coord, 1.0)).xyz;
    geom_cam = u_campos;
    geom_radius = vert_radius;
}
"""

g_impostor_sph_BCK = """
#version 330

layout (points) in;
layout (triangle_strip, max_vertices = 18) out;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 geom_color[];
in vec3 geom_coord[];
in vec3 geom_center[];
in vec3 geom_cam[];
in float geom_radius[];

out vec3 frag_color;
out vec3 frag_coord;
out vec3 frag_center;
out vec3 frag_cam;
out float frag_radius;

vec3 p_1 = vec3(-1.0,-1.0,-1.0);
vec3 p_2 = vec3(-1.0,-1.0, 1.0);
vec3 p_3 = vec3( 1.0,-1.0, 1.0);
vec3 p_4 = vec3( 1.0,-1.0,-1.0);
vec3 p_5 = vec3(-1.0, 1.0,-1.0);
vec3 p_6 = vec3(-1.0, 1.0, 1.0);
vec3 p_7 = vec3( 1.0, 1.0, 1.0);
vec3 p_8 = vec3( 1.0, 1.0,-1.0);

void main(){
    vec3 point1 = geom_coord[0] + p_1 * geom_radius[0];
    vec3 point2 = geom_coord[0] + p_2 * geom_radius[0];
    vec3 point3 = geom_coord[0] + p_3 * geom_radius[0];
    vec3 point4 = geom_coord[0] + p_4 * geom_radius[0];
    vec3 point5 = geom_coord[0] + p_5 * geom_radius[0];
    vec3 point6 = geom_coord[0] + p_6 * geom_radius[0];
    vec3 point7 = geom_coord[0] + p_7 * geom_radius[0];
    vec3 point8 = geom_coord[0] + p_8 * geom_radius[0];
    
    gl_Position = proj_mat * vec4(point1, 1.0);
    frag_color = geom_color[0];
    frag_coord = point1;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point6, 1.0);
    frag_color = geom_color[0];
    frag_coord = point6;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point2, 1.0);
    frag_color = geom_color[0];
    frag_coord = point2;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point7, 1.0);
    frag_color = geom_color[0];
    frag_coord = point7;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point3, 1.0);
    frag_color = geom_color[0];
    frag_coord = point3;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point8, 1.0);
    frag_color = geom_color[0];
    frag_coord = point8;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point4, 1.0);
    frag_color = geom_color[0];
    frag_coord = point4;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point5, 1.0);
    frag_color = geom_color[0];
    frag_coord = point5;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point1, 1.0);
    frag_color = geom_color[0];
    frag_coord = point1;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point6, 1.0);
    frag_color = geom_color[0];
    frag_coord = point6;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    
    EndPrimitive();
    gl_Position = proj_mat * vec4(point1, 1.0);
    frag_color = geom_color[0];
    frag_coord = point1;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point2, 1.0);
    frag_color = geom_color[0];
    frag_coord = point2;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point4, 1.0);
    frag_color = geom_color[0];
    frag_coord = point4;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point3, 1.0);
    frag_color = geom_color[0];
    frag_coord = point3;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    EndPrimitive();

    gl_Position = proj_mat * vec4(point5, 1.0);
    frag_color = geom_color[0];
    frag_coord = point5;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point6, 1.0);
    frag_color = geom_color[0];
    frag_coord = point6;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point8, 1.0);
    frag_color = geom_color[0];
    frag_coord = point8;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(point7, 1.0);
    frag_color = geom_color[0];
    frag_coord = point7;
    frag_center = geom_center[0];
    frag_cam = vec3(view_mat * model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    EndPrimitive();
}
"""

f_impostor_sph_BCK = """
#version 330
#extension GL_EXT_frag_depth: enable
precision highp float;

struct Light {
    vec3 position;
    //vec3 color;
    vec3 intensity;
    //vec3 specular_color;
    float ambient_coef;
    float shininess;
};

uniform Light my_light;

uniform mat4 proj_mat;
//uniform float u_depth;

in vec3 frag_color;
in vec3 frag_coord;
in vec3 frag_center;
in vec3 frag_cam;
in float frag_radius;

out vec4 final_color;

float sph_intersect(vec3 ro, vec3 rd, vec3 sph, float rad){
    vec3 oc = ro - sph;
    float b = dot(oc, rd);
    float c = dot(oc, oc) - rad*rad;
    float h = b*b - c;
    if( h<0.0 ) return -1.0;
    return -b - sqrt(h);
}

float sph_intersect(vec3 ro, vec3 rd, vec3 sph, float rad){
    vec3 eye_to_sph = sph - ro;
    float p = dot(eye_to_sph, rd);
    vec3 p_coord = ro + rd * p;
    float b = length(p_coord - sph);
    if( b > rad ) return -1.0;
    return p - sqrt(rad*rad - b*b);
}

void main() {
    vec3 ray_orig = frag_cam;
    vec3 ray_dir = normalize(frag_coord - frag_cam);
    float dist_to_sph = sph_intersect(ray_orig, ray_dir, frag_center, frag_radius);
    if (dist_to_sph < 0.0) discard;
    vec3 coord_on_sph = ray_orig + ray_dir * dist_to_sph;
    vec3 normal = normalize(coord_on_sph - frag_center);
    vec3 vert_to_light = normalize(my_light.position - coord_on_sph);
    
    // Ambient Component
    vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
    
    // Diffuse component
    float diffuse_coef = max(0.0, dot(normal, vert_to_light));
    vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
    //final_color = vec4(ambient + diffuse, 1.0);
    
    //vec4 depth = proj_mat * vec4(frag_center + normal * frag_radius, 1.0);
    //gl_FragDepthEXT = depth.z/depth.w;
    //vec4 depth = proj_mat * vec4(coord_on_sph, 1.0);
    //gl_FragDepthEXT = depth.z/depth.w;
    
    final_color = vec4(ambient + diffuse, 1.0);
}
"""

v_cubes = """
#version 330
precision highp float;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec3 vert_color;
in float vert_radius;

//uniform vec3 u_campos;

out vec3 geom_color;
out vec3 geom_center;
out float geom_radius;

void main() {
    geom_color = vert_color;
    geom_center = vert_coord;
    geom_radius = vert_radius;
}
"""

g_cubes = """
#version 330

layout (points) in;
layout (triangle_strip, max_vertices = 18) out;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 geom_color[];
in vec3 geom_center[];
in float geom_radius[];

out vec3 frag_color;

vec3 p_1 = vec3(-1.0,-1.0,-1.0);
vec3 p_2 = vec3(-1.0,-1.0, 1.0);
vec3 p_3 = vec3( 1.0,-1.0, 1.0);
vec3 p_4 = vec3( 1.0,-1.0,-1.0);
vec3 p_5 = vec3(-1.0, 1.0,-1.0);
vec3 p_6 = vec3(-1.0, 1.0, 1.0);
vec3 p_7 = vec3( 1.0, 1.0, 1.0);
vec3 p_8 = vec3( 1.0, 1.0,-1.0);

void main(){
    vec3 point1 = geom_center[0] + p_1 * geom_radius[0];
    vec3 point2 = geom_center[0] + p_2 * geom_radius[0];
    vec3 point3 = geom_center[0] + p_3 * geom_radius[0];
    vec3 point4 = geom_center[0] + p_4 * geom_radius[0];
    vec3 point5 = geom_center[0] + p_5 * geom_radius[0];
    vec3 point6 = geom_center[0] + p_6 * geom_radius[0];
    vec3 point7 = geom_center[0] + p_7 * geom_radius[0];
    vec3 point8 = geom_center[0] + p_8 * geom_radius[0];
    
    gl_Position = proj_mat * view_mat * model_mat * vec4(point1, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point6, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point2, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point7, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point3, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point8, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point4, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point5, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point1, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point6, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    EndPrimitive();
    
    gl_Position = proj_mat * view_mat * model_mat * vec4(point1, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point2, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point4, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point3, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    EndPrimitive();
    
    gl_Position = proj_mat * view_mat * model_mat * vec4(point5, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point6, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point8, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point7, 1.0);
    frag_color = geom_color[0];
    EmitVertex();
    EndPrimitive();
}
"""

f_cubes = """
#version 330
#extension GL_EXT_frag_depth: enable
precision highp float;

in vec3 frag_color;

out vec4 final_color;

void main() {
    final_color = vec4(frag_color, 1.0);
}
"""


v_impostor_cyl = """
#version 330
precision highp float;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec3 vert_color;
in float vert_radius;

uniform vec3 u_campos;

out vec3 geom_color;
out vec3 geom_coord;
out vec3 geom_center;
out vec3 geom_cam;
out float geom_radius;

void main() {
    geom_color = vert_color;
    geom_coord = vert_coord;
    geom_center = vert_coord;
    geom_cam = u_campos;
    geom_radius = vert_radius;
}
"""

g_impostor_cyl = """
#version 330

layout (lines) in;
layout (triangle_strip, max_vertices = 18) out;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 geom_color[];
in vec3 geom_coord[];
in vec3 geom_center[];
in vec3 geom_cam[];
in float geom_radius[];

out vec3 frag_color;
out vec3 frag_coord;
out vec3 frag_pA;
out vec3 frag_pB;
out vec3 frag_cam;
out float frag_radius;

void main(){
    vec3 AB_dir = normalize(geom_coord[1] - geom_coord[0]);
    vec3 side_dir = normalize(geom_cam[0] - geom_coord[0]);
    vec3 base_dir = normalize(cross(AB_dir, side_dir));
    side_dir = normalize(cross(AB_dir, base_dir));
    
    float rad_fac = geom_radius[0] * 1.415;
    vec3 base_1 = geom_coord[0] + base_dir * rad_fac - AB_dir * rad_fac;
    vec3 base_2 = geom_coord[0] + side_dir * rad_fac - AB_dir * rad_fac;
    vec3 base_3 = geom_coord[0] - base_dir * rad_fac - AB_dir * rad_fac;
    vec3 base_4 = geom_coord[0] - side_dir * rad_fac - AB_dir * rad_fac;
    vec3 top_1 = geom_coord[1] + base_dir * rad_fac + AB_dir * rad_fac;
    vec3 top_2 = geom_coord[1] + side_dir * rad_fac + AB_dir * rad_fac;
    vec3 top_3 = geom_coord[1] - base_dir * rad_fac + AB_dir * rad_fac;
    vec3 top_4 = geom_coord[1] - side_dir * rad_fac + AB_dir * rad_fac;
    
    mat4 pvm_mat = proj_mat * view_mat * model_mat;
    mat4 vm_mat = model_mat;
    
    gl_Position = pvm_mat * vec4(base_1, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(vm_mat * vec4(base_1, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(top_1, 1.0);
    frag_color = geom_color[1];
    frag_coord = vec3(vm_mat * vec4(top_1, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(base_2, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(vm_mat * vec4(base_2, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(top_2, 1.0);
    frag_color = geom_color[1];
    frag_coord = vec3(vm_mat * vec4(top_2, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(base_3, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(vm_mat * vec4(base_3, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(top_3, 1.0);
    frag_color = geom_color[1];
    frag_coord = vec3(vm_mat * vec4(top_3, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(base_4, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(vm_mat * vec4(base_4, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(top_4, 1.0);
    frag_color = geom_color[1];
    frag_coord = vec3(vm_mat * vec4(top_4, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(base_1, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(vm_mat * vec4(base_1, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(top_1, 1.0);
    frag_color = geom_color[1];
    frag_coord = vec3(vm_mat * vec4(top_1, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    
    EndPrimitive();
    gl_Position = pvm_mat * vec4(base_1, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(vm_mat * vec4(base_1, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(base_2, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(vm_mat * vec4(base_2, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(base_4, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(vm_mat * vec4(base_4, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(base_3, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(vm_mat * vec4(base_3, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[0], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    EndPrimitive();

    gl_Position = pvm_mat * vec4(top_1, 1.0);
    frag_color = geom_color[1];
    frag_coord = vec3(vm_mat * vec4(top_1, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(top_2, 1.0);
    frag_color = geom_color[1];
    frag_coord = vec3(vm_mat * vec4(top_2, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(top_4, 1.0);
    frag_color = geom_color[1];
    frag_coord = vec3(vm_mat * vec4(top_4, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = pvm_mat * vec4(top_3, 1.0);
    frag_color = geom_color[1];
    frag_coord = vec3(vm_mat * vec4(top_3, 1.0));
    frag_pA = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_pB = vec3(vm_mat * vec4(geom_center[1], 1.0));
    frag_cam = vec3(vm_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    EndPrimitive();
}
"""

f_impostor_cyl = """
#version 330
#extension GL_EXT_frag_depth: enable
precision highp float;

struct Light {
    vec3 position;
    //vec3 color;
    vec3 intensity;
    //vec3 specular_color;
    float ambient_coef;
    float shininess;
};

uniform Light my_light;

uniform mat4 proj_mat;
//uniform float u_depth;

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

in vec3 frag_color;
in vec3 frag_coord;
in vec3 frag_pA;
in vec3 frag_pB;
in vec3 frag_cam;
in float frag_radius;

out vec4 final_color;

float caps_intersect( vec3 p, vec3 a, vec3 b, float r ){
  vec3 pa = p - a;
  vec3 ba = b - a;
  float h = clamp( dot(pa,ba)/dot(ba,ba), 0.0, 1.0 );
  return length( pa - ba*h ) - r;
}

vec3 caps_normal( vec3 p, vec3 a, vec3 b, float r ){
  vec3 pa = p - a;
  vec3 ba = b - a;
  float h = clamp( dot(pa,ba)/dot(ba,ba), 0.0, 1.0 );
  return ( pa - ba*h ) / r;
}
float capIntersect( in vec3 ro, in vec3 rd, in vec3 pa, in vec3 pb, in float ra ){
    vec3  ba = pb - pa;
    vec3  oa = ro - pa;
    float baba = dot(ba,ba);
    float bard = dot(ba,rd);
    float baoa = dot(ba,oa);
    float rdoa = dot(rd,oa);
    float oaoa = dot(oa,oa);
    float a = baba      - bard*bard;
    float b = baba*rdoa - baoa*bard;
    float c = baba*oaoa - baoa*baoa - ra*ra*baba;
    float h = b*b - a*c;
    if( h >= 0.0 )
    {
        float t = (-b-sqrt(h))/a;
        float y = baoa + t*bard;
        // body
        if( y>0.0 && y<baba ) return t;
        // caps
        vec3 oc = (y <= 0.0) ? oa : ro - pb;
        b = dot(rd,oc);
        c = dot(oc,oc) - ra*ra;
        h = b*b - c;
        if( h>0.0 ) return -b - sqrt(h);
    }
    return -1.0;
}
void main() {
    vec3 ray_orig = frag_cam;
    vec3 ray_dir = normalize(frag_coord - frag_cam);
    float dist_to_caps = capIntersect(ray_orig, ray_dir, frag_pA, frag_pB, frag_radius);
    if (dist_to_caps < 0.0) discard;
    //final_color = vec4(dist_to_caps,0,0, length(frag_color));
    
    vec3 coord_on_caps = frag_cam + ray_dir * dist_to_caps;
    vec3 normal = normalize(caps_normal(frag_coord, frag_pA, frag_pB, frag_radius));
    vec3 vert_to_light = normalize(my_light.position - coord_on_caps);
    
    // Ambient Component
    vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
    
    // Diffuse component
    float diffuse_coef = max(0.0, dot(normal, vert_to_light));
    vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
    //final_color = vec4(ambient + diffuse, 1.0);
    
    //vec4 depth = proj_mat * vec4(frag_center + normal * frag_radius, 1.0);
    //gl_FragDepthEXT = depth.z/depth.w;
    //vec4 depth = proj_mat * vec4(coord_on_caps, 1.0);
    //gl_FragDepth = depth.z/depth.w;
    final_color = vec4(ambient + diffuse, 1.0);
}
"""


v_glumpy = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

uniform vec3 u_campos;

in vec3 vert_coord;
in vec3 vert_color;
in float vert_radius;
float hw_ratio;

out float frag_radius;
out float frag_dot_size;
out vec3 frag_color;
out vec4 frag_coord;

void main (void){
    hw_ratio = proj_mat[0][0] * proj_mat[1][1];
    frag_color = vert_color;
    frag_radius = vert_radius;
    frag_coord = view_mat * model_mat * vec4(vert_coord, 1.0);
    gl_Position = proj_mat * frag_coord;
    vec4 p = proj_mat * vec4(vert_radius, vert_radius, frag_coord.z, frag_coord.w);
    frag_dot_size = 256.0 * hw_ratio * vert_radius / p.w;
    gl_PointSize = frag_dot_size;
}
"""

f_glumpy = """
#version 330

struct Light {
   vec3 position;
   //vec3 color;
   vec3 intensity;
   //vec3 specular_color;
   float ambient_coef;
   float shininess;
};

uniform Light my_light;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in float frag_radius;
in float frag_dot_size;
in vec3 frag_color;
in vec4 frag_coord;

out vec4 final_color;

vec4 outline(float distance, float linewidth, float antialias, vec4 fg_color, vec4 bg_color){
    vec4 frag_color;
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);
    
    if( border_distance < 0.0 )
        frag_color = fg_color;
    else if( signed_distance < 0.0 )
        frag_color = mix(bg_color, fg_color, sqrt(alpha));
    else {
        if( abs(signed_distance) < (linewidth/2.0 + antialias) ) {
            frag_color = vec4(fg_color.rgb, fg_color.a * alpha);
        } else {
            discard;
        }
    }
    return frag_color;
}

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

void main(){
    //vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    //float distance = length(P*frag_dot_size) - frag_dot_size/2;
    //vec2 texcoord = gl_PointCoord* 2.0 - vec2(1.0);
    //float x = texcoord.x;
    //float y = texcoord.y;
    //float d = 1.0 - x*x - y*y;
    //if (d <= 0.0) discard;
    //
    //float z = sqrt(d);
    //vec4 pos = frag_coord;
    //pos.z += frag_radius*z;
    //pos = proj_mat * pos;
    //gl_FragDepth = 0.5*(pos.z / pos.w)+0.5;
    //vec3 normal = vec3(x,-y,z);
    //vec4 color = calculate_color(normal, frag_coord.xyz, frag_color);
    //final_color = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color);

    vec2 p = gl_PointCoord - vec2(0.5);
    float lp = length(p);
    if (lp > 0.5) discard;
    float lco = sqrt(0.5*0.5 - lp*lp);
    vec4 coord_on_sph = proj_mat * vec4(p.x, p.y, lco, 1);
    vec3 normal = normalize(coord_on_sph.xyz - frag_coord.xyz);
    //gl_FragDepth = coord_on_sph.z / coord_on_sph.w;
    final_color = calculate_color(normal, coord_on_sph.xyz, frag_color);
}
"""

v_cartoon = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec3 vert_norm;
in vec3 vert_color;

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_norm;

void main(){
    mat4 modelview = view_mat * model_mat;
    gl_Position = proj_mat * modelview * vec4(vert_coord, 1.0);
    frag_coord = vec3(modelview * vec4(vert_coord, 1.0));
    frag_color = vert_color;
    frag_norm = mat3(transpose(inverse(model_mat))) * vert_norm;
}
"""
f_cartoon = """
#version 330

struct Light {
    vec3 position;
    //vec3 color;
    vec3 intensity;
    //vec3 specular_color;
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

void main(){
    final_color = calculate_color(frag_norm, frag_coord, frag_color);
}
"""

v_texture =  """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec2 vert_uv;

out vec2 frag_uv;

void main(){
    gl_Position = proj_mat * view_mat * model_mat * vec4(vert_coord, 1.0);
    frag_uv = vert_uv;
}
"""
f_texture = """
#version 330

uniform sampler2D font_texture;

const float width = 0.5;
const float edge = 0.01;
uniform vec3 font_color;

in vec2 frag_uv;

out vec4 final_color;

void main(){
    float distance = 1.0 - texture(font_texture, frag_uv).a;
    float alpha = 1.0 - smoothstep(width, width + edge, distance);
    if (alpha<=0.0)
        discard;
    final_color = vec4(font_color, alpha);
}
"""

v_text =  """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec2 vert_uv;

out vec2 frag_uv;

void main(){
    gl_Position = proj_mat * view_mat * model_mat * vec4(vert_coord, 1.0);
    frag_uv = vert_uv;
}
"""
f_text = """
#version 330

uniform sampler2D font_texture;

const float width = 0.5;
const float edge = 0.05;
uniform vec3 font_color;

in vec2 frag_uv;

out vec4 final_color;

void main(){
    float distance = 1.0 - texture(font_texture, frag_uv).a;
    float alpha = 1.0 - smoothstep(width, width + edge, distance);
    if (alpha<=0.0)
        discard;
    final_color = vec4(font_color, alpha);
}
"""

v_diamonds = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec4 vert_uv;

out vec4 geom_coord;
out vec4 geom_uv;

void main(){
    geom_coord = view_mat * model_mat * vec4(vert_coord, 1);
    geom_uv = vert_uv;
}
"""
g_diamonds = """
#version 330

layout (points) in; // Name for use is gl_in[] is default for GLSL
layout (triangle_strip, max_vertices = 4) out;

uniform mat4 proj_mat;

in vec4 geom_coord[];
in vec4 geom_uv[];

out vec3 frag_color;
out vec2 frag_uv;

void main(){
    vec4 offset = vec4(-0.5, 0.5, 0.0, 0.0);
    vec4 vertPos = offset + geom_coord[0];
    gl_Position = proj_mat * vertPos;
    frag_uv = vec2(geom_uv[0].r, geom_uv[0].b);
    EmitVertex();
    offset = vec4(-0.5,-0.5, 0.0, 0.0);
    vertPos = offset + geom_coord[0];
    gl_Position = proj_mat * vertPos;
    frag_uv = vec2(geom_uv[0].r, geom_uv[0].a);
    EmitVertex();
    offset = vec4(0.5,0.5, 0.0, 0.0);
    vertPos = offset + geom_coord[0];
    gl_Position = proj_mat * vertPos;
    frag_uv = vec2(geom_uv[0].g, geom_uv[0].b);
    EmitVertex();
    offset = vec4(0.5,-0.5, 0.0, 0.0);
    vertPos = offset + geom_coord[0];
    gl_Position = proj_mat * vertPos;
    frag_uv = vec2(geom_uv[0].g, geom_uv[0].a);
    EmitVertex();
    EndPrimitive();
}
"""
f_diamonds = """
#version 330

uniform sampler2D font_texture;

const float width = 0.5;
const float edge = 0.05;
uniform vec3 font_color;

in vec2 frag_uv;

out vec4 final_color;

void main(){
    float distance = 1.0 - texture(font_texture, frag_uv).a;
    float alpha = 1.0 - smoothstep(width, width + edge, distance);
    if (alpha<=0.0)
        discard;
    final_color = vec4(font_color, alpha);
}
"""

v_instances = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec3 vert_color;
in vec3 vert_instance;
in float vert_radius;

vec3 vert_norm;

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_norm;

void main(){
    mat4 modelview = view_mat * model_mat;
    vec3 offset_coord = vert_coord * vert_radius + vert_instance;
    gl_Position = proj_mat * modelview * vec4(offset_coord, 1.0);
    
    vert_norm = normalize(offset_coord - vert_instance);
    frag_coord = vec3(modelview * vec4(offset_coord, 1.0));
    frag_norm = mat3(transpose(inverse(model_mat))) * vert_norm;
    frag_color = vert_color;
}
"""
f_instances = """
#version 330

struct Light {
   vec3 position;
   //vec3 color;
   vec3 intensity;
   //vec3 specular_color;
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

void main(){
    final_color = calculate_color(frag_norm, frag_coord, frag_color);
}
"""

v_billboard = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec3 vert_color;
in float vert_radius;

uniform vec3 u_campos;

out vec3 geom_coord;
out vec3 geom_color;
out float geom_radius;
out vec3 geom_cam;

void main(){
    geom_coord = (view_mat * model_mat * vec4(vert_coord, 1)).xyz;
    geom_color = vert_color;
    geom_radius = vert_radius;
    geom_cam = (view_mat * model_mat * vec4(u_campos, 1)).xyz;
}
"""
g_billboard = """
#version 330

layout (points) in; // Name for use is gl_in[] is default for GLSL
layout (triangle_strip, max_vertices = 4) out;

uniform mat4 proj_mat;

in vec3 geom_coord[];
in vec3 geom_color[];
in float geom_radius[];
in vec3 geom_cam[];

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_center;
out vec3 frag_cam;
out float frag_radius;

void main(){
    float scale_r = geom_radius[0] * sqrt(2.0);
    vec3 p_1 = vec3(-1.0,-1.0, 1.0) * scale_r;
    vec3 p_2 = vec3(-1.0, 1.0, 1.0) * scale_r;
    vec3 p_3 = vec3( 1.0,-1.0, 1.0) * scale_r;
    vec3 p_4 = vec3( 1.0, 1.0, 1.0) * scale_r;
    
    frag_coord = geom_coord[0] + p_1;
    frag_color = geom_color[0];
    frag_center = geom_coord[0];
    frag_cam = geom_cam[0];
    frag_radius = geom_radius[0];
    gl_Position = proj_mat * vec4(frag_coord, 1.0);
    EmitVertex();
    frag_coord = geom_coord[0] + p_2;
    frag_color = geom_color[0];
    frag_center = geom_coord[0];
    frag_cam = geom_cam[0];
    frag_radius = geom_radius[0];
    gl_Position = proj_mat * vec4(frag_coord, 1.0);
    EmitVertex();
    frag_coord = geom_coord[0] + p_3;
    frag_color = geom_color[0];
    frag_center = geom_coord[0];
    frag_cam = geom_cam[0];
    frag_radius = geom_radius[0];
    gl_Position = proj_mat * vec4(frag_coord, 1.0);
    EmitVertex();
    frag_coord = geom_coord[0] + p_4;
    frag_color = geom_color[0];
    frag_center = geom_coord[0];
    frag_cam = geom_cam[0];
    frag_radius = geom_radius[0];
    gl_Position = proj_mat * vec4(frag_coord, 1.0);
    EmitVertex();
    EndPrimitive();
}
"""
f_billboard = """
#version 330
#extension GL_EXT_frag_depth: enable
precision highp float;

struct Light {
    vec3 position;
    //vec3 color;
    vec3 intensity;
    //vec3 specular_color;
    float ambient_coef;
    float shininess;
};

uniform Light my_light;

uniform mat4 proj_mat;
//uniform float u_depth;

in vec3 frag_color;
in vec3 frag_coord;
in vec3 frag_center;
in vec3 frag_cam;
in float frag_radius;

out vec4 final_color;

float sph_intersect(vec3 ro, vec3 rd, vec3 sph, float rad){
    vec3 eye_to_sph = sph - ro;
    float p = dot(eye_to_sph, rd);
    vec3 p_coord = ro + rd * p;
    float b = length(p_coord - sph);
    if( b > rad ) return -1.0;
    return p - sqrt(rad*rad - b*b);
}

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

void main(){
    vec3 ray_orig = frag_cam;
    vec3 ray_dir = normalize(frag_coord - frag_cam);
    float dist_to_sph = sph_intersect(ray_orig, ray_dir, frag_center, frag_radius);
    if (dist_to_sph < 0.0) discard;
    vec3 coord_on_sph = ray_orig + ray_dir * dist_to_sph;
    vec3 normal = normalize(coord_on_sph - frag_center);
    //vec4 depth = proj_mat * vec4(coord_on_sph, 1.0);
    //gl_FragDepth = depth.z / depth.w;
    
    //vec3 temp = frag_center - frag_cam;
    //dist_to_sph = dot(coord_on_sph, normalize(temp));
    //gl_FragDepth = dist_to_sph / length(temp);
    
    final_color = calculate_color(normal, coord_on_sph, frag_color);
}
"""


v_impostor_sph = """
#version 330
precision highp float;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

uniform vec3 u_campos;

in vec3 vert_coord;
in vec3 vert_color;
in vec3 vert_center;
in float vert_radius;

out vec3 frag_color;
out vec3 frag_coord;
out vec3 frag_center;
out vec3 frag_cam;
out float frag_radius;

void main() {
    gl_Position = proj_mat * view_mat * model_mat * vec4(vert_coord, 1.0);
    frag_coord = (view_mat * model_mat * vec4(vert_coord, 1.0)).xyz;
    frag_center = (view_mat * model_mat * vec4(vert_center, 1.0)).xyz;
    frag_radius = vert_radius;
    frag_color = vert_color;
    frag_cam = (view_mat * model_mat * vec4(u_campos, 1.0)).xyz;
}
"""

f_impostor_sph = """
#version 330
#extension GL_EXT_frag_depth: enable
precision highp float;

struct Light {
    vec3 position;
    //vec3 color;
    vec3 intensity;
    //vec3 specular_color;
    float ambient_coef;
    float shininess;
};

uniform mat4 proj_mat;
uniform Light my_light;

in vec3 frag_color;
in vec3 frag_coord;
in vec3 frag_center;
in vec3 frag_cam;
in float frag_radius;

out vec4 final_color;

float sph_intersect(vec3 ro, vec3 rd, vec3 sph, float rad){
    vec3 eye_to_sph = sph - ro;
    float p = dot(eye_to_sph, rd);
    vec3 p_coord = ro + rd * p;
    float b = length(p_coord - sph);
    if( b > rad ) return -1.0;
    return p - sqrt(rad*rad - b*b);
}

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
    vec3 ray_orig = frag_cam;
    vec3 ray_dir = normalize(frag_coord - frag_cam);
    float dist_to_sph = sph_intersect(ray_orig, ray_dir, frag_center, frag_radius);
    if (dist_to_sph < 0.0) discard;
    vec3 coord_on_sph = ray_orig + ray_dir * dist_to_sph;
    vec3 normal = normalize(coord_on_sph - frag_center);
    
    final_color = calculate_color(normal, coord_on_sph, frag_color);
    vec4 depth = proj_mat * vec4(frag_center + normal * frag_radius, 1.0);
    gl_FragDepthEXT = depth.z/depth.w;
    //vec4 depth = proj_mat * vec4(coord_on_sph, 1.0);
    //gl_FragDepthEXT = depth.z/depth.w;
}
"""

v_simple = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec3 vert_norm;
in vec3 vert_color;

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_norm;

void main() {
    mat4 modelview = view_mat * model_mat;
    gl_Position = proj_mat * modelview * vec4(vert_coord, 1.0);
    frag_coord = vec3(modelview * vec4(vert_coord, 1.0));
    frag_color = vert_color;
    frag_norm = mat3(transpose(inverse(model_mat))) * vert_norm;
}
"""
f_simple = """
#version 330

struct Light {
    vec3 position;
    //vec3 color;
    vec3 intensity;
    //vec3 specular_color;
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