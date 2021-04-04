#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2021 Carlos Eduardo Sequeiros Borja <carseq@amu.edu.pl>
#  

vertex_shader = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;

in vec3 vert_coord;
in vec3 vert_color;

out vec3 sh_color;

void main()
{
   sh_color = vert_color;
   //gl_Position = vec4(vert_coord, 1.0);
   //gl_Position = camera * vec4(vert_coord, 1);
   gl_Position = projection_mat * view_mat * model_mat * vec4(vert_coord, 1);
}
"""
 
fragment_shader = """
#version 330

in vec3 sh_color;

out vec4 final_color;

void main()
{
   final_color = vec4(sh_color, 1.0);
}
"""
