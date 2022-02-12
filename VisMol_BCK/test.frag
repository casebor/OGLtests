
#ifdef GL_ES
precision mediump float;
#endif

#define PI 3.14159265359

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

float plot(vec2 st, float pct){
  return  smoothstep( pct-0.02, pct, st.y) -
          smoothstep( pct, pct+0.02, st.y);
}

vec3 get_circle(vec2 pos, float radius){
    float circle = sqrt(pow(pos.x,2.) + pow(pos.y,2.));
    circle = smoothstep(radius+0.01, radius, circle);
    return vec3(circle);
}

float raySphereIntersect(vec3 r0, vec3 rd, vec3 frag_coord, float frag_radius){
    float a = dot(rd, rd);
    vec3 s0_r0 = r0 - frag_coord;
    float b = 2.0 * dot(rd, s0_r0);
    float c = dot(s0_r0, s0_r0) - (frag_radius * frag_radius);
    float disc = b*b - 4.0*a*c;
    if (disc <= 0.0) {
        return -1.0;
    }
    return (-b - sqrt(disc))/(2.0*a);
}

float near = 0.1;
float far = 1.0;

void main() {
    vec2 st = gl_FragCoord.xy/u_resolution;
    vec3 canvas = vec3(0.);
    
    vec3 c1 = vec3(0.2, 0.5, 0.0);
    vec3 c2 = vec3(0.3, 0.2, 0.1);
    vec3 c3 = vec3(0.7, 0.7, 0.2);
    
    float depth_c1 = (-c1.z - near) / (far - near);
    float depth_c2 = (-c2.z - near) / (far - near);
    float depth_c3 = (-c3.z - near) / (far - near);
    
    vec3 circle1 = get_circle(st - c1.xy, 0.15);
    vec3 circle2 = get_circle(st - c2.xy, 0.25);
    vec3 circle3 = get_circle(st - c3.xy, 0.30);
    
    // circle1 = vec3(circle1.xy, depth_c1);
    // circle2 = vec3(circle2.xy, depth_c2);
    // circle3 = vec3(circle3.xy, depth_c3);
    
    circle1 += vec3(depth_c1);
    circle2 += vec3(depth_c2);
    circle3 += vec3(depth_c3);
    
    circle1 *= vec3(1.0, 0.0, 0.0);
    circle2 *= vec3(0.0, 1.0, 0.0);
    circle3 *= vec3(0.0, 0.0, 1.0);
    
    canvas += circle1;
    canvas += circle2;
    canvas += circle3;
    
    gl_FragColor = vec4(canvas,1.0);
}
