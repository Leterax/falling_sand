#version 460

#define LX 0
#define LY 0
#define W 0
#define H 0

layout (local_size_x = LX, local_size_y = LY) in;
layout(rgba8ui, binding=0) readonly uniform uimage2D fromTex;
layout(rgba8ui, binding=1) writeonly uniform uimage2D destTex;

void main() {

    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    uvec4 particle = imageLoad(fromTex, texelPos);

    if (particle.z == 1) {
        if ((imageLoad(fromTex, texelPos + ivec2(0, -1)).z == 0) && ((texelPos + ivec2(0, -1)).y >= 0)) {
            imageStore(destTex, texelPos + ivec2(0, -1), particle);
            imageStore(destTex, texelPos, uvec4(0, 0, 0, 0));
        }
        else {
            imageStore(destTex, texelPos, particle);
        }
    }
}