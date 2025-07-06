import pyglet
from pyglet.math import Mat4, Vec3

from scripts.render import RenderWindow
from scripts.primitives import Cube, Sphere, TexturedCube
from scripts.control import Control

def create_plane(scale: Vec3, pos: Vec3, rgba=(255, 255, 255, 255)):
    plane = Cube(scale)
    colors = []
    for _ in range(8):
        colors.extend(rgba)
    transform = Mat4.from_translation(pos)
    return plane.vertices, plane.indices, colors, transform

if __name__ == '__main__':
    width = 1280
    height = 720

    renderer = RenderWindow(width, height, "Assignment #2", resizable=True)
    renderer.set_location(200, 200)

    # 카메라 위치 설정
    renderer.cam_eye = Vec3(0, 2, 15)
    renderer.cam_target = Vec3(0, 0, 0)
    renderer.cam_vup = Vec3(0, 1, 0)
    renderer.view_mat = Mat4.look_at(renderer.cam_eye, renderer.cam_target, renderer.cam_vup)

    controller = Control(renderer)

    controller.camera_dist = 15.0
    controller.camera_azim = 0.0
    controller.camera_elev = 0.2
    controller.update_camera()

    # Cornell Box (10x10x10, 두께 0.1)
    # 왼쪽 벽 (빨간색)
    lw_vertices, lw_indices, lw_colors, lw_transform = create_plane(
        scale=Vec3(0.1, 10, 10),
        pos=Vec3(-5, 0, 0),
        rgba=(255, 0, 0, 255)
    )
    renderer.add_shape(lw_transform, lw_vertices, lw_indices, lw_colors)

    # 오른쪽 벽 (초록색)
    rw_vertices, rw_indices, rw_colors, rw_transform = create_plane(
        scale=Vec3(0.1, 10, 10),
        pos=Vec3(5, 0, 0),
        rgba=(0, 255, 0, 255)
    )
    renderer.add_shape(rw_transform, rw_vertices, rw_indices, rw_colors)

    # 뒷벽 (흰색)
    bw_vertices, bw_indices, bw_colors, bw_transform = create_plane(
        scale=Vec3(10, 10, 0.1),
        pos=Vec3(0, 0, -5),
        rgba=(255, 255, 255, 255)
    )
    renderer.add_shape(bw_transform, bw_vertices, bw_indices, bw_colors)

    # 바닥
    floor_vertices, floor_indices, floor_colors, floor_transform = create_plane(
        scale=Vec3(10, 0.1, 10),
        pos=Vec3(0, -5, 0),
        rgba=(255, 255, 255, 255)
    )
    renderer.add_shape(floor_transform, floor_vertices, floor_indices, floor_colors)

    # 천장
    ceiling_vertices, ceiling_indices, ceiling_colors, ceiling_transform = create_plane(
        scale=Vec3(10, 0.1, 10),
        pos=Vec3(0, 5, 0),
        rgba=(255, 255, 255, 255)
    )
    renderer.add_shape(ceiling_transform, ceiling_vertices, ceiling_indices, ceiling_colors)

    # 천장 중앙의 광원
    light_vertices, light_indices, light_colors, light_transform = create_plane(
        scale=Vec3(2, 0.25, 2),
        pos=Vec3(0, 4.95, 0),
        rgba=(255, 255, 200, 255)
    )
    renderer.add_shape(light_transform, light_vertices, light_indices, light_colors)

    # Box (4×4×4, 텍스처-box.png)
    texture_path = "./textures/box.png"
    box_image = pyglet.image.load(texture_path)
    box_texture = box_image.get_texture()
    tbox_scale = Vec3(4, 4, 4)
    tbox_obj = TexturedCube(tbox_scale)
    tbox_transform = Mat4.from_translation(Vec3(-2.5, -2.95, -2.5))
    renderer.add_textured_shape(
        transform=tbox_transform,
        vertices=tbox_obj.vertices,
        indices=tbox_obj.indices,
        tex_coords=tbox_obj.tex_coords,
        texture=box_texture
    )

    # Sphere (반지름 2, 단색 파란색)
    sphere_obj = Sphere(stacks=30, slices=30, scale=2.0)
    sphere_transform = Mat4.from_translation(Vec3(2.5, -2.95, 2.5))
    num_vertices = len(sphere_obj.vertices) // 3
    sphere_colors = []
    for _ in range(num_vertices):
        sphere_colors.extend([0, 0, 255, 255])
    renderer.add_shape(sphere_transform, sphere_obj.vertices, sphere_obj.indices, sphere_colors)

    renderer.run()
