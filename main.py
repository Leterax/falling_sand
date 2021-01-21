import moderngl as mgl
import moderngl_window as mglw
from moderngl_window.geometry import quad_fs
from pathlib import Path
import numpy as np
from moderngl_window.utils.scheduler import Scheduler
import time


class SandSim(mglw.WindowConfig):
    gl_version = (4, 6)
    window_size = (1280, 720)
    world_size = (500, 10)
    resizable = False
    resource_dir = Path(__file__).parent.resolve()

    local_size = (1, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scheduler = Scheduler(self.timer)
        self.fs_quad = quad_fs()

        self.display_program = self.load_program("display.glsl")
        self.display_program["texture0"] = 2

        self.cs = self.load_compute_shader(
            "compute.glsl", {"H": self.world_size[0], "W": self.world_size[1]}
        )

        blank_world = np.full((*self.world_size, 4), (0, 0, 0, 0), dtype=np.uint32)

        self.world_a = self.ctx.texture(
            self.world_size, 4, data=blank_world, dtype="u4"
        )
        self.world_b = self.ctx.texture(
            self.world_size, 4, data=blank_world, dtype="u4"
        )

        self.world_a.filter = mgl.NEAREST, mgl.NEAREST
        self.world_b.filter = mgl.NEAREST, mgl.NEAREST

        self.world_a.write(
            np.array([1, 0, 0, 0] * (5 * 1)).astype("u4"), viewport=(0, 3, 1, 5),
        )

        # schedule the compute shader
        self.scheduler.run_every(self.run_cs, 1 / 60)  # 5x per second
        self.toggle = False

    def run_cs(self):
        # print(f"running cs, bindings: {not self.toggle}, {self.toggle}")
        # calculate group and local size
        nx, ny, nz = (
            self.world_size[0] // self.local_size[0],
            self.world_size[1] // self.local_size[1],
            1,
        )
        self.world_a.bind_to_image(self.toggle)
        self.world_b.bind_to_image(not self.toggle)
        self.cs.run(nx, ny, nz)

        if self.toggle:
            self.world_a.use(2)
        else:
            self.world_b.use(2)

        self.toggle = not self.toggle

    def render(self, ttime, frametime):
        time.sleep(1 / 20)
        # self.scheduler.execute()
        self.run_cs()
        self.fs_quad.render(self.display_program)


SandSim.run()
