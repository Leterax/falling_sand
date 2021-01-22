import moderngl as mgl
import moderngl_window as mglw
from moderngl_window.geometry import quad_fs
from pathlib import Path
import numpy as np
import imageio
import time
import OpenGL.GL as gl


class SandSim(mglw.WindowConfig):
    gl_version = (4, 6)
    window_size = (640, 640)
    world_size = (250, 250)
    aspect_ratio = None
    resizable = False
    resource_dir = Path(__file__).parent.resolve()

    local_size = (16, 16)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fs_quad = quad_fs(normals=False)

        self.display_program = self.load_program("display.glsl")
        self.display_program["texture0"] = 2

        self.cs = self.load_compute_shader(
            "compute.glsl",
            {
                "LX": self.local_size[0],
                "LY": self.local_size[1],
                "W": self.world_size[0],
                "H": self.world_size[1],
            },
        )

        empty = np.zeros((*self.world_size, 4), dtype="u1")
        self.world_a = self.ctx.texture(self.world_size, 4, data=empty, dtype="u1")
        self.world_b = self.ctx.texture(self.world_size, 4, data=empty, dtype="u1")
        self.world_a.filter = mgl.NEAREST, mgl.NEAREST
        self.world_b.filter = mgl.NEAREST, mgl.NEAREST

        # draw a line of sand vertically
        self.world_a.write(
            np.array(np.random.random(size=(1500, 4)) + 0.5).astype("u1"),
            viewport=(100, 100, 100, 15),
        )

        self.fbo_a = self.ctx.framebuffer(color_attachments=(self.world_a,))
        self.fbo_b = self.ctx.framebuffer(color_attachments=(self.world_b,))

        # toggle to switch between textures
        self.toggle = False

    def run_cs(self):
        # calculate group and local size
        nx, ny, nz = (
            self.world_size[0] // self.local_size[0],
            self.world_size[1] // self.local_size[1],
            1,
        )
        self.world_a.bind_to_image(self.toggle, read=not self.toggle, write=self.toggle)
        self.world_b.bind_to_image(
            not self.toggle, read=self.toggle, write=not self.toggle
        )
        # gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)
        self.cs.run(nx, ny, nz)
        # gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

        if self.toggle:
            self.world_a.use(2)
            self.fbo_b.clear()
        else:
            self.world_b.use(2)
            self.fbo_a.clear()

        self.toggle = not self.toggle

    def render(self, ttime, frametime):
        self.run_cs()
        # gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)
        self.fs_quad.render(self.display_program)


SandSim.run()
