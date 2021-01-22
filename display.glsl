#version 460

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;
out vec2 uv0;

void main() {
    gl_Position = vec4(in_position, 1);
    uv0 = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform usampler2D texture0;
in vec2 uv0;

void main() {
    uvec4 particle = texture(texture0, uv0);
    if (particle.z == 1) { // sand
        fragColor = vec4(1., .5, 0., 1.);
    }
    else { // not sand
        fragColor = vec4(.5, .5, .5, 1.);
    }
}
#endif