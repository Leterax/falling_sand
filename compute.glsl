#version 460

#define LOCAL_X 0
#define LOCAL_Y 0

// Particle:
// r: type - 0 wall, 1 air, 2 sand

layout (local_size_x = LOCAL_X, local_size_y = LOCAL_Y) in;
layout(rgba32ui, binding=0) uniform uimage2D fromTex;
layout(rgba32ui, binding=1) uniform uimage2D destTex;

void main() {
    uvec4 air = uvec4(0, 0, 0, 0);

    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    uvec4 particle = imageLoad(fromTex, texelPos);

    ivec2 right_pos = texelPos + ivec2(1, 0);
    uvec4 right = imageLoad(fromTex, right_pos);

    if (particle.r != 1) {
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