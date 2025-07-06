import pyglet
from pyglet import window
from pyglet.window import mouse, key
from pyglet.math import Mat4, Vec3

import math

class Control:
    def __init__(self, window):
        self.window = window
        window.on_key_press = self.on_key_press
        window.on_key_release = self.on_key_release
        window.on_mouse_motion = self.on_mouse_motion
        window.on_mouse_drag = self.on_mouse_drag
        window.on_mouse_press = self.on_mouse_press
        window.on_mouse_release = self.on_mouse_release
        window.on_mouse_scroll = self.on_mouse_scroll

        # 카메라 파라미터 초기값
        self.camera_azim = 0.0 # 좌우 회전
        self.camera_elev = 0.2 # 상하 회전
        self.camera_dist = 3.0 # 카메라와 중심 사이의 기본 거리

        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.dragging = False

        self.update_camera()

    def update_camera(self):
        eye_x = self.camera_dist * math.cos(self.camera_elev) * math.sin(self.camera_azim)
        eye_y = self.camera_dist * math.sin(self.camera_elev)
        eye_z = self.camera_dist * math.cos(self.camera_elev) * math.cos(self.camera_azim)
        self.window.cam_eye = Vec3(eye_x, eye_y, eye_z)
        self.window.cam_target = Vec3(0, 0, 0)
        self.window.cam_vup = Vec3(0, 1, 0)
        self.window.view_mat = Mat4.look_at(self.window.cam_eye, self.window.cam_target, self.window.cam_vup)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == key.SPACE:
            self.window.animate = not self.window.animate

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.dragging = True
            self.last_mouse_x = x
            self.last_mouse_y = y

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.dragging = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragging and (buttons & mouse.LEFT):
            sensitivity = 0.01
            self.camera_azim += dx * sensitivity
            self.camera_elev += dy * sensitivity
            max_elev = math.radians(89.0)
            if self.camera_elev > max_elev:
                self.camera_elev = max_elev
            if self.camera_elev < -max_elev:
                self.camera_elev = -max_elev
            self.update_camera()
        self.last_mouse_x = x
        self.last_mouse_y = y

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.camera_dist -= scroll_y * 0.2
        if self.camera_dist < 0.5:
            self.camera_dist = 0.5
        if self.camera_dist > 50.0:
            self.camera_dist = 50.0
        self.update_camera()
