import pyglet
from pyglet.gl import *
from pyglet.math import Mat4, Vec3

from scripts.primitives import CustomGroup, TexturedGroup

class RenderWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        # 카메라 기본 파라미터
        self.cam_eye = Vec3(0, 2, 4)
        self.cam_target = Vec3(0, 0, 0)
        self.cam_vup = Vec3(0, 1, 0)
        self.view_mat = None

        self.z_near = 0.1
        self.z_far = 100
        self.fov = 60
        self.proj_mat = None

        self.shapes = []
        self.setup()

        self.animate = False

    def setup(self) -> None:
        self.set_minimum_size(width=400, height=300)
        self.set_mouse_visible(True)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        self.view_mat = Mat4.look_at(
            self.cam_eye, self.cam_target, self.cam_vup)
        self.proj_mat = Mat4.perspective_projection(
            aspect=self.width/self.height,
            z_near=self.z_near,
            z_far=self.z_far,
            fov=self.fov)

    def on_draw(self) -> None:
        self.clear()
        self.batch.draw()

    def update(self, dt) -> None:
        view_proj = self.proj_mat @ self.view_mat
        for shape in self.shapes:
            if self.animate:
                rotate_angle = dt
                rotate_axis = Vec3(0, 1, 0)
                rotate_mat = Mat4.from_rotation(angle=rotate_angle, vector=rotate_axis)
                shape.transform_mat @= rotate_mat
            shape.shader_program['view_proj'] = view_proj

    def on_resize(self, width, height):
        glViewport(0, 0, *self.get_framebuffer_size())
        self.proj_mat = Mat4.perspective_projection(
            aspect=width/height,
            z_near=self.z_near,
            z_far=self.z_far,
            fov=self.fov)
        return pyglet.event.EVENT_HANDLED

    def add_shape(self, transform, vertices, indices, colors):
        shape_group = CustomGroup(transform, len(self.shapes))
        shape_group.indexed_vertices_list = shape_group.shader_program.vertex_list_indexed(
            len(vertices) // 3,
            GL_TRIANGLES,
            batch=self.batch,
            group=shape_group,
            indices=indices,
            vertices=('f', vertices),
            colors=('Bn', colors)
        )
        self.shapes.append(shape_group)

    def add_textured_shape(self, transform, vertices, indices, tex_coords, texture):
        shape_group = TexturedGroup(transform, len(self.shapes), texture)
        shape_group.indexed_vertices_list = shape_group.shader_program.vertex_list_indexed(
            len(vertices) // 3,
            GL_TRIANGLES,
            batch=self.batch,
            group=shape_group,
            indices=indices,
            vertices=('f', vertices),
            texCoords=('f', tex_coords)
        )
        self.shapes.append(shape_group)

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()
