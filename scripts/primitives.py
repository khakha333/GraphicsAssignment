import pyglet
from pyglet.gl import *
from pyglet.math import Mat4, Vec3
import math

import scripts.shader as shader

# 단색과 텍스처 다르게 그룹화
# 기본 단색 그룹
class CustomGroup(pyglet.graphics.Group):
    def __init__(self, transform_mat: Mat4, order):
        super().__init__(order)
        self.shader_program = shader.create_program(
            shader.vertex_source_default, shader.fragment_source_default
        )
        self.transform_mat = transform_mat
        self.indexed_vertices_list = None
        self.shader_program.use()

    def set_state(self):
        self.shader_program.use()
        self.shader_program['model'] = self.transform_mat

    def unset_state(self):
        self.shader_program.stop()

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.order == other.order and
                self.parent == other.parent)

    def __hash__(self):
        return hash(self.order)

# 텍스처 그룹
class TexturedGroup(pyglet.graphics.Group):
    def __init__(self, transform_mat: Mat4, order, texture):
        super().__init__(order)
        self.shader_program = shader.create_program(
            shader.vertex_source_tex, shader.fragment_source_tex
        )
        self.transform_mat = transform_mat
        self.indexed_vertices_list = None
        self.texture = texture
        self.shader_program.use()

    def set_state(self):
        self.shader_program.use()
        self.shader_program['model'] = self.transform_mat
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(self.texture.target, self.texture.id)
        self.shader_program['myTexture'] = 0

    def unset_state(self):
        self.shader_program.stop()
        glBindTexture(self.texture.target, 0)

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.order == other.order and
                self.parent == other.parent)

    def __hash__(self):
        return hash(self.order)

class Cube:
    def __init__(self, scale=1.0):
        # 8개 정점 (-0.5 ~ 0.5 범위)
        self.vertices = [
            -0.5, -0.5,  0.5,  
             0.5, -0.5,  0.5,  
             0.5,  0.5,  0.5,  
            -0.5,  0.5,  0.5,  
            -0.5, -0.5, -0.5,  
             0.5, -0.5, -0.5,  
             0.5,  0.5, -0.5,  
            -0.5,  0.5, -0.5
        ]
        if isinstance(scale, (int, float)):
            scale = Vec3(scale, scale, scale)
        self.vertices = [scale[idx % 3] * x for idx, x in enumerate(self.vertices)]
        self.indices = [
            0,1,2, 2,3,0,
            4,7,6, 6,5,4,
            4,5,1, 1,0,4,
            6,7,3, 3,2,6,
            5,6,2, 2,1,5,
            7,4,0, 0,3,7
        ]

class Sphere:
    def __init__(self, stacks, slices, scale=1.0):
        self.vertices = []
        self.indices = []
        self.colors = []

        if isinstance(scale, (int, float)):
            sx = sy = sz = scale
        else:
            sx, sy, sz = scale.x, scale.y, scale.z

        for i in range(stacks):
            phi0 = 0.5 * math.pi - (i * math.pi) / stacks
            phi1 = 0.5 * math.pi - ((i + 1) * math.pi) / stacks
            y0 = sy * math.sin(phi0)
            r0 = sx * math.cos(phi0)
            y1 = sy * math.sin(phi1)
            r1 = sx * math.cos(phi1)
            for j in range(slices):
                theta0 = (j * 2 * math.pi) / slices
                theta1 = ((j + 1) * 2 * math.pi) / slices

                x0 = r0 * math.cos(theta0)
                z0 = r0 * math.sin(theta0)
                x1 = r1 * math.cos(theta0)
                z1 = r1 * math.sin(theta0)
                x2 = r1 * math.cos(theta1)
                z2 = r1 * math.sin(theta1)
                x3 = r0 * math.cos(theta1)
                z3 = r0 * math.sin(theta1)

                if i != stacks - 1:
                    self.vertices.extend([x0, y0, z0,  x1, y1, z1,  x2, y1, z2])
                    col = (int(abs(math.cos(phi0))*255),
                           int(abs(math.cos(theta0))*255),
                           int(abs(math.sin(phi0))*255),
                           255)
                    self.colors.extend(col)
                    self.colors.extend(col)
                    self.colors.extend(col)
                if i != 0:
                    self.vertices.extend([x2, y1, z2,  x3, y0, z3,  x0, y0, z0])
                    self.colors.extend(col)
                    self.colors.extend(col)
                    self.colors.extend(col)
        num_vertices = len(self.vertices) // 3
        self.indices = list(range(num_vertices))

class TexturedCube:
    def __init__(self, scale=1.0):
        if isinstance(scale, (int, float)):
            sx = sy = sz = scale
        else:
            sx, sy, sz = scale.x, scale.y, scale.z

        self.vertices = [
            -0.5*sx, -0.5*sy,  0.5*sz,
             0.5*sx, -0.5*sy,  0.5*sz,
             0.5*sx,  0.5*sy,  0.5*sz,
            -0.5*sx,  0.5*sy,  0.5*sz,

             0.5*sx, -0.5*sy, -0.5*sz,
            -0.5*sx, -0.5*sy, -0.5*sz,
            -0.5*sx,  0.5*sy, -0.5*sz,
             0.5*sx,  0.5*sy, -0.5*sz,

            -0.5*sx, -0.5*sy, -0.5*sz,
            -0.5*sx, -0.5*sy,  0.5*sz,
            -0.5*sx,  0.5*sy,  0.5*sz,
            -0.5*sx,  0.5*sy, -0.5*sz,

             0.5*sx, -0.5*sy,  0.5*sz,
             0.5*sx, -0.5*sy, -0.5*sz,
             0.5*sx,  0.5*sy, -0.5*sz,
             0.5*sx,  0.5*sy,  0.5*sz,

            -0.5*sx, -0.5*sy, -0.5*sz,
             0.5*sx, -0.5*sy, -0.5*sz,
             0.5*sx, -0.5*sy,  0.5*sz,
            -0.5*sx, -0.5*sy,  0.5*sz,
 
            -0.5*sx,  0.5*sy,  0.5*sz,
             0.5*sx,  0.5*sy,  0.5*sz,
             0.5*sx,  0.5*sy, -0.5*sz,
            -0.5*sx,  0.5*sy, -0.5*sz,
        ]

        self.tex_coords = [
            0,0, 1,0, 1,1, 0,1,
            0,0, 1,0, 1,1, 0,1,
            0,0, 1,0, 1,1, 0,1,
            0,0, 1,0, 1,1, 0,1,
            0,0, 1,0, 1,1, 0,1,
            0,0, 1,0, 1,1, 0,1,
        ]

        self.indices = []
        for i in range(6):
            start = i * 4
            self.indices += [start, start+1, start+2, start+2, start+3, start]
