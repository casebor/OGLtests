#!/usr/bin/env python

import math
import numpy as np
import ctypes
import camera as cam

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import OpenGL
from OpenGL import GL
from OpenGL.GL import shaders

global degrees
degrees = np.float32(0)

class MyGLProgram():
    def __init__(self, vertex, fragment):
        self.glarea = Gtk.GLArea.new()
        self.glarea.connect("realize", self.initialize)
        self.glarea.connect("render", self.render)
        self.vertex_shader = vertex
        self.fragment_shader = fragment
        self.model_mat = self.view_mat = self.proj_mat = np.identity(4, dtype=np.float32)
        
    def initialize(self, otro):
        self.glarea.set_has_depth_buffer(True)
        self.glarea.set_has_alpha(True)
        self.flag = True
    
    def load_shaders(self):
        my_vertex = shaders.compileShader(self.vertex_shader, GL.GL_VERTEX_SHADER)
        my_fragment = shaders.compileShader(self.fragment_shader, GL.GL_FRAGMENT_SHADER)
        self.program = shaders.compileProgram(my_vertex, my_fragment)
        self.load_data()
        self.flag = False
    
    def render(self, area, context):
        if self.flag:
            self.load_shaders()
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        #print self.program, 'rendereing'
        GL.glUseProgram(self.program)
        
        global degrees
        model = np.identity(4, dtype=np.float32)
        view = np.identity(4, dtype=np.float32)
        proj = np.identity(4, dtype=np.float32)
        model = cam.my_glRotateYf(model, degrees)
        view = cam.my_glTranslatef(view, np.array([0,0,-3],dtype=np.float32))
        aloc = self.glarea.get_allocation()
        w = np.float32(aloc.width)
        h = np.float32(aloc.height)
        proj = cam.my_gluPerspectivef(proj, 30, w/h, 0.1, 10.0)
        
        self.model = GL.glGetUniformLocation(self.program, 'model_mat')
        GL.glUniformMatrix4fv(self.model, 1, GL.GL_FALSE, model)
        self.view = GL.glGetUniformLocation(self.program, 'view_mat')
        GL.glUniformMatrix4fv(self.view, 1, GL.GL_FALSE, view)
        self.proj = GL.glGetUniformLocation(self.program, 'projection_mat')
        GL.glUniformMatrix4fv(self.proj, 1, GL.GL_FALSE, proj)
        
        # Extern line
        u_linewidth = 2
        # Intern line
        u_antialias = 2
        u_size = 1
        uni_ulinewidth = GL.glGetUniformLocation(self.program, 'u_linewidth')
        GL.glUniform1fv(uni_ulinewidth, 1, u_linewidth)
        uni_uantialias = GL.glGetUniformLocation(self.program, 'u_antialias')
        GL.glUniform1fv(uni_uantialias, 1, u_antialias)
        uni_usize = GL.glGetUniformLocation(self.program, 'u_size')
        GL.glUniform1fv(uni_usize, 1, u_size)
        
        GL.glBindVertexArray(self.vertex_array_object)
        if self.coords is None:
            pass
        else:
            GL.glDrawArrays(GL.GL_POINTS, 0, int(len(self.coords)/3))
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
        #degrees += 1
        #if degrees >= 360:
            #degrees = np.float32(0)
    
    def load_data(self):
        self.vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vertex_array_object)
        
        self.coords = 0.45 * np.random.randn(30000, 3)
        self.colors = np.random.uniform(0.85, 1.00, (30000, 4))
        a_size = np.random.uniform(.1, .2, 10000)
        
        self.coords = np.array([1.0, 1.0, 0.0,
                                0.0, 1.0, 0.0,
                                1.0, 0.0, 0.0,
                               -1.0, 0.0, 0.0,
                               -1.0, 1.0, 0.0,
                               -1.0,-1.0, 0.0,
                                0.0,-1.0, 0.0,
                                1.0,-1.0, 0.0,
                                0.0, 0.0, 0.0],dtype=np.float32)
        self.colors = np.array([1.0, 0.0, 0.0,
                                1.0, 1.0, 0.0,
                                1.0, 0.0, 1.0,
                                0.0, 0.0, 1.0,
                                0.0, 1.0, 0.0,
                                0.0, 1.0, 1.0,
                                0.0, 1.0, 0.0,
                                0.0, 1.0, 0.0,
                                0.0, 1.0, 0.0],dtype=np.float32)
        GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        
        coords_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coords_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.coords.itemsize*len(self.coords), self.coords, GL.GL_STATIC_DRAW)
        position = GL.glGetAttribLocation(self.program, 'coordinate')
        GL.glEnableVertexAttribArray(position)
        GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.coords.itemsize, ctypes.c_void_p(0))
        
        colors_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, colors_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.colors.itemsize*len(self.colors), self.colors, GL.GL_STATIC_DRAW)
        gl_colors = GL.glGetAttribLocation(self.program, 'my_color')
        GL.glEnableVertexAttribArray(gl_colors)
        GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.colors.itemsize, ctypes.c_void_p(0))
        
        #a_size = np.array([50.0, 30.0, 40.0, 50.0, 38.0, 30.0, 40.0, 50.0, 38.0],dtype=np.float32)
        a_size = np.array([50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0],dtype=np.float32)
        size_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, size_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, a_size.itemsize*len(a_size), a_size, GL.GL_STATIC_DRAW)
        att_asize = GL.glGetAttribLocation(self.program, 'a_size')
        GL.glEnableVertexAttribArray(att_asize)
        GL.glVertexAttribPointer(att_asize, 1, GL.GL_FLOAT, GL.GL_FALSE, a_size.itemsize, ctypes.c_void_p(0))
        
        a_fg_color = [0, 0, 0, 1]*int(len(self.coords)/3)
        a_fg_color = np.array(a_fg_color, dtype=np.float32)
        afgcol_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, afgcol_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, a_fg_color.itemsize*len(a_fg_color), a_fg_color, GL.GL_STATIC_DRAW)
        att_afgcolor = GL.glGetAttribLocation(self.program, 'a_fg_color')
        GL.glEnableVertexAttribArray(att_afgcolor)
        GL.glVertexAttribPointer(att_afgcolor, 4, GL.GL_FLOAT, GL.GL_FALSE, 4*a_fg_color.itemsize, ctypes.c_void_p(0))
        
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(position)
        GL.glDisableVertexAttribArray(gl_colors)
        GL.glDisableVertexAttribArray(att_asize)
        GL.glDisableVertexAttribArray(att_afgcolor)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)


vert_sh = """
#version 120
// Uniforms
// ------------------------------------
uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;
uniform float u_linewidth;
uniform float u_antialias;
uniform float u_size;
// Attributes
// ------------------------------------
attribute vec3  coordinate;
attribute vec4  a_fg_color;
attribute vec4  my_color;
attribute float a_size;
// Varyings
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;
void main (void) {
    v_size = a_size * u_size;
    v_linewidth = u_linewidth;
    v_antialias = u_antialias;
    v_fg_color  = a_fg_color;
    v_bg_color  = my_color;
    gl_Position = projection_mat * view_mat * model_mat * vec4(coordinate,1.0);
    gl_PointSize = v_size + 2*(v_linewidth + 1.5*v_antialias);
}
"""

frag_sh = """
#version 120
// Constants
// ------------------------------------
// Varyings
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;
// Functions
// ------------------------------------
// ----------------
float disc(vec2 P, float size)
{
    float r = length((P.xy - vec2(0.5,0.5))*size);
    r -= v_size/2;
    return r;
}
// ----------------
float arrow_right(vec2 P, float size)
{
    float r1 = abs(P.x -.50)*size + abs(P.y -.5)*size - v_size/2;
    float r2 = abs(P.x -.25)*size + abs(P.y -.5)*size - v_size/2;
    float r = max(r1,-r2);
    return r;
}
// ----------------
float ring(vec2 P, float size)
{
    float r1 = length((gl_PointCoord.xy - vec2(0.5,0.5))*size) - v_size/2;
    float r2 = length((gl_PointCoord.xy - vec2(0.5,0.5))*size) - v_size/4;
    float r = max(r1,-r2);
    return r;
}
// ----------------
float clober(vec2 P, float size)
{
    const float PI = 3.14159265358979323846264;
    const float t1 = -PI/2;
    const vec2  c1 = 0.2*vec2(cos(t1),sin(t1));
    const float t2 = t1+2*PI/3;
    const vec2  c2 = 0.2*vec2(cos(t2),sin(t2));
    const float t3 = t2+2*PI/3;
    const vec2  c3 = 0.2*vec2(cos(t3),sin(t3));
    float r1 = length((gl_PointCoord.xy- vec2(0.5,0.5) - c1)*size);
    r1 -= v_size/3;
    float r2 = length((gl_PointCoord.xy- vec2(0.5,0.5) - c2)*size);
    r2 -= v_size/3;
    float r3 = length((gl_PointCoord.xy- vec2(0.5,0.5) - c3)*size);
    r3 -= v_size/3;
    float r = min(min(r1,r2),r3);
    return r;
}
// ----------------
float square(vec2 P, float size)
{
    float r = max(abs(gl_PointCoord.x -.5)*size,
                  abs(gl_PointCoord.y -.5)*size);
    r -= v_size/2;
    return r;
}
// ----------------
float diamond(vec2 P, float size)
{
    float r = abs(gl_PointCoord.x -.5)*size + abs(gl_PointCoord.y -.5)*size;
    r -= v_size/2;
    return r;
}
// ----------------
float vbar(vec2 P, float size)
{
    float r1 = max(abs(gl_PointCoord.x -.75)*size,
                   abs(gl_PointCoord.x -.25)*size);
    float r3 = max(abs(gl_PointCoord.x -.5)*size,
                   abs(gl_PointCoord.y -.5)*size);
    float r = max(r1,r3);
    r -= v_size/2;
    return r;
}
// ----------------
float hbar(vec2 P, float size)
{
    float r2 = max(abs(gl_PointCoord.y -.75)*size,
                   abs(gl_PointCoord.y -.25)*size);
    float r3 = max(abs(gl_PointCoord.x -.5)*size,
                   abs(gl_PointCoord.y -.5)*size);
    float r = max(r2,r3);
    r -= v_size/2;
    return r;
}
// ----------------
float cross(vec2 P, float size)
{
    float r1 = max(abs(gl_PointCoord.x -.75)*size,
                   abs(gl_PointCoord.x -.25)*size);
    float r2 = max(abs(gl_PointCoord.y -.75)*size,
                   abs(gl_PointCoord.y -.25)*size);
    float r3 = max(abs(gl_PointCoord.x -.5)*size,
                   abs(gl_PointCoord.y -.5)*size);
    float r = max(min(r1,r2),r3);
    r -= v_size/2;
    return r;
}
// Main
// ------------------------------------
void main()
{
    float size = v_size +2*(v_linewidth + 1.5*v_antialias);
    float t = v_linewidth/2.0-v_antialias;
    float r = disc(gl_PointCoord, size);
    // float r = square(gl_PointCoord, size);
    // float r = ring(gl_PointCoord, size);
    // float r = arrow_right(gl_PointCoord, size);
    // float r = diamond(gl_PointCoord, size);
    // float r = cross(gl_PointCoord, size);
    // float r = clober(gl_PointCoord, size);
    // float r = hbar(gl_PointCoord, size);
    // float r = vbar(gl_PointCoord, size);
    float d = abs(r) - t;
    if( r > (v_linewidth/2.0+v_antialias))
    {
        discard;
    }
    else if( d < 0.0 )
    {
       gl_FragColor = v_fg_color;
    }
    else
    {
        float alpha = d/v_antialias;
        alpha = exp(-alpha*alpha);
        if (r > 0)
            gl_FragColor = vec4(v_fg_color.rgb, alpha*v_fg_color.a);
        else
            gl_FragColor = mix(v_bg_color, v_fg_color, alpha);
    }
}
"""

vertex_shader = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;
uniform float u_linewidth;
uniform float u_antialias;
uniform float u_size;

in vec3 coordinate;
in vec3 my_color;
in float a_size;
attribute vec4  a_fg_color;

varying float v_size;
varying float v_linewidth;
varying float v_antialias;
varying vec4 v_bg_color;
varying vec4 v_fg_color;

void main(){
   v_size = a_size * u_size;
   v_linewidth = u_linewidth;
   v_antialias = u_antialias;
   v_bg_color = vec4(my_color, 1.0);
   v_fg_color  = a_fg_color;
   gl_Position = projection_mat * view_mat * model_mat * vec4(coordinate, 1);
   gl_PointSize = v_size + 2*(v_linewidth + 1.5*v_antialias);
}
"""
 
fragment_shader = """
#version 330

out vec4 final_color;
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;
// ------------------------------------
float disc(vec2 P, float size)
{
    float r = length((P.xy - vec2(0.5,0.5))*size);
    r -= v_size/2;
    return r;
}

// ----------------
float arrow_right(vec2 P, float size)
{
    float r1 = abs(P.x -.50)*size + abs(P.y -.5)*size - v_size/2;
    float r2 = abs(P.x -.25)*size + abs(P.y -.5)*size - v_size/2;
    float r = max(r1,-r2);
    return r;
}
// ----------------
float ring(vec2 P, float size)
{
    float r1 = length((gl_PointCoord.xy - vec2(0.5,0.5))*size) - v_size/2;
    float r2 = length((gl_PointCoord.xy - vec2(0.5,0.5))*size) - v_size/4;
    float r = max(r1,-r2);
    return r;
}
// ----------------
float clober(vec2 P, float size)
{
    const float PI = 3.14159265358979323846264;
    const float t1 = -PI/2;
    const vec2  c1 = 0.2*vec2(cos(t1),sin(t1));
    const float t2 = t1+2*PI/3;
    const vec2  c2 = 0.2*vec2(cos(t2),sin(t2));
    const float t3 = t2+2*PI/3;
    const vec2  c3 = 0.2*vec2(cos(t3),sin(t3));
    float r1 = length((gl_PointCoord.xy- vec2(0.5,0.5) - c1)*size);
    r1 -= v_size/3;
    float r2 = length((gl_PointCoord.xy- vec2(0.5,0.5) - c2)*size);
    r2 -= v_size/3;
    float r3 = length((gl_PointCoord.xy- vec2(0.5,0.5) - c3)*size);
    r3 -= v_size/3;
    float r = min(min(r1,r2),r3);
    return r;
}
// ----------------
float square(vec2 P, float size)
{
    float r = max(abs(gl_PointCoord.x -.5)*size,
                  abs(gl_PointCoord.y -.5)*size);
    r -= v_size/2;
    return r;
}
// ----------------
float diamond(vec2 P, float size)
{
    float r = abs(gl_PointCoord.x -.5)*size + abs(gl_PointCoord.y -.5)*size;
    r -= v_size/2;
    return r;
}
// ----------------
float vbar(vec2 P, float size)
{
    float r1 = max(abs(gl_PointCoord.x -.75)*size,
                   abs(gl_PointCoord.x -.25)*size);
    float r3 = max(abs(gl_PointCoord.x -.5)*size,
                   abs(gl_PointCoord.y -.5)*size);
    float r = max(r1,r3);
    r -= v_size/2;
    return r;
}
// ----------------
float hbar(vec2 P, float size)
{
    float r2 = max(abs(gl_PointCoord.y -.75)*size,
                   abs(gl_PointCoord.y -.25)*size);
    float r3 = max(abs(gl_PointCoord.x -.5)*size,
                   abs(gl_PointCoord.y -.5)*size);
    float r = max(r2,r3);
    r -= v_size/2;
    return r;
}
// ----------------
float cross(vec2 P, float size)
{
    float r1 = max(abs(gl_PointCoord.x -.75)*size,
                   abs(gl_PointCoord.x -.25)*size);
    float r2 = max(abs(gl_PointCoord.y -.75)*size,
                   abs(gl_PointCoord.y -.25)*size);
    float r3 = max(abs(gl_PointCoord.x -.5)*size,
                   abs(gl_PointCoord.y -.5)*size);
    float r = max(min(r1,r2),r3);
    r -= v_size/2;
    return r;
}

void main(){
   float size = v_size +2*(v_linewidth + 1.5*v_antialias);
   float t = v_linewidth/2.0-v_antialias;
   
   // gl_PointCoord is the pixel in the coordinate
   float r = disc(gl_PointCoord, size);
   float d = abs(r) - t;
   
   // This if else statement makes the circle ilusion
   if( r > (v_linewidth/2.0+v_antialias)){
      discard;
   }
   else if( d < 0.0 ){
      final_color = v_fg_color;
   }
   else{
      float alpha = d/v_antialias;
      alpha = exp(-alpha*alpha);
      if (r > 0)
         final_color = v_fg_color;
      else
         final_color = mix(v_bg_color, v_fg_color, alpha);
   }
}
"""

#test = MyGLProgram(vert_sh, frag_sh)
test = MyGLProgram(vertex_shader, fragment_shader)
wind = Gtk.Window()
wind.add(test.glarea)

wind.connect("delete-event", Gtk.main_quit)
wind.show_all()
Gtk.main()





























