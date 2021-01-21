#version 460

#define W 0
#define H 0

// Particle:
// r: type - 0 wall, 1 air, 2 sand
// g:
// b: 


layout (local_size_x = 16, local_size_y = 16) in;
layout(rgba32ui, binding=0) uniform uimage2D fromTex;
layout(rgba32ui, binding=1) uniform uimage2D destTex;

void main() {
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    uvec4 particle = imageLoad(fromTex, texelPos);

    uvec4 air = uvec4(0, 0, 0, 0);

    ivec2 right_pos = texelPos + ivec2(1, 0);
    uvec4 right = imageLoad(fromTex, right_pos);
    // uvec4 above = imageLoad(fromTex, texelPos + ivec2(0, 1));
    // uvec4 left = imageLoad(fromTex, texelPos + ivec2(-1, 0));
    // uvec4 right = imageLoad(fromTex, texelPos + ivec2(1, 0));
    if (particle.r == 0) {
        // just store the particle, we dont care about it!
        imageStore(destTex, texelPos, particle);
    }
    if (particle.r == 1) {
        // if there is air below us, move and delete old
        if (right == air) {
            imageStore(destTex, right_pos, particle);
            imageStore(destTex, texelPos, air);
        }
        else {
            imageStore(destTex, texelPos, particle); 
        }
    }
}