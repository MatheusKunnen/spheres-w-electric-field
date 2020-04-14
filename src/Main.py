# @desc: Sphere Elastic Collisions Simulator
# @autor: Matheus Kunnen Ledesma - matheusl.2000@alunos.utfpr.edu.br

import numpy as np
from OpenGLManager import OpenGLManager

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Body import Body
from Ring import Ring
import time
import math


class Main:
    # General parameters
    DEBUG = True
    ROT_K = 1.
    MOVE_K = .1

    # Simulator parameters
    ring_v = []

    def __init__(self):
        self.is_running = False
        self.is_paused = True
        self.dt = 1/60.0
        self.target_dt = 1/30.0
        self.move_vector = np.array([0., 0., 0.])
        self.rot_vector = np.array([0., 0., 0.])
        self.g_manager = OpenGLManager("Electric Field")
        self.t_total = 0
        self.cam_pos = np.array([0, 30, -10])
        self.cam_rot = np.array([0, 0, 0])
        self.body = Body(1, .1, 1, np.array(
            [.1, 0, 0]), np.array([0, 0, 2]), -10)
        self.ring = Ring(np.array([0, 0, 0]), 10, 320)
        self.E = np.array([0., 0., 0.])

    def run(self):
        self.is_running = self.g_manager.init_display()
        self.g_manager.set_cam_pos(self.cam_pos)

        while self.is_running:
            t1 = time.time()
            self.g_manager.clear_buffer()
            self.check_events()
            if not self.is_paused:
                self.update()
            self.draw()
            self.g_manager.swap_buffers()
            t2 = time.time()
            self.update_dt(t1, t2)

    def draw(self):
        self.draw_hud()
        self.body.draw(self.g_manager)
        self.ring.draw(self.g_manager)

    def update(self):
        self.E = self.ring.get_electric_field(self.body.b_pos)
        self.body.b_aceleration = self.E * \
            (self.body.b_charge/self.body.b_mass)
        self.body.update(self.dt)

    def draw_hud(self):
        txt_status = "Paused" if self.is_paused else "Running"
        self.g_manager.captions = [
            "-> General Parameters",
            f"       FPS: {round(1/self.dt,0)}",
            f"Cam. dPos.: {np.round(self.cam_pos, 2)}",
            f"Cam. dRot.: {np.round(self.body.b_pos, 2)}",
            f"Status: {txt_status}", "",
            "-> Central Body ",
            f"   P: {np.round(self.body.b_pos, 3)}",
            f"  dP: {np.round(self.body.b_vel, 3)}",
            f"d^2P: {np.round(self.body.b_aceleration, 3)}",
            f"E(P): {np.round(self.E, 3)}"]
        self.g_manager.draw_captions()

    def update_dt(self, t1, t2):
        self.dt = t2 - t1
        self.t_total += self.dt
        if self.dt > self.target_dt:
            pass
            # print(f"FPS {round(1/self.dt,1)} | {round((self.dt - self.target_dt)/self.target_dt,1)} frames missed")
        else:
            self.g_manager.wait(self.target_dt - self.dt)

    def draw_sphere_ring(self):
        r_ring = 10
        ds = math.pi/32
        r = (2 * math.pi * r_ring / (32 * 2)) * 0.5
        # print(r)
        n = 0
        while n <= 2*math.pi:
            self.g_manager.draw_solid_sphere(
                [r_ring*math.cos(n), r_ring*math.sin(n), 0], r)
            n += ds

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move_vector = [
                        Main.MOVE_K, 0., 0.] if event.type == pygame.KEYDOWN else [0., 0., 0.]
                    # self.g_manager.move_cam()
                elif event.key == pygame.K_RIGHT:
                    self.move_vector = [
                        -Main.MOVE_K, 0., 0.] if event.type == pygame.KEYDOWN else [0., 0., 0.]
                elif event.key == pygame.K_DOWN:
                    self.move_vector = [
                        0., Main.MOVE_K, 0.] if event.type == pygame.KEYDOWN else [0., 0., 0.]
                elif event.key == pygame.K_UP:
                    self.move_vector = [
                        0., -Main.MOVE_K, 0.] if event.type == pygame.KEYDOWN else [0., 0., 0.]
                elif event.key == pygame.K_q:
                    self.move_vector = [
                        0., 0., Main.MOVE_K] if event.type == pygame.KEYDOWN else [0., 0., 0.]
                elif event.key == pygame.K_e:
                    self.move_vector = [
                        0., 0., -Main.MOVE_K] if event.type == pygame.KEYDOWN else [0., 0., 0.]
                elif event.key == pygame.K_a:
                    self.rot_vector = [
                        0., -Main.ROT_K, 0.] if event.type == pygame.KEYDOWN else [0., 0., 0.]
                elif event.key == pygame.K_d:
                    self.rot_vector = [
                        0., Main.ROT_K, 0.] if event.type == pygame.KEYDOWN else [0., 0., 0.]
                elif event.key == pygame.K_w:
                    self.rot_vector = [
                        -Main.ROT_K, 0., 0.] if event.type == pygame.KEYDOWN else [0., 0., 0.]
                elif event.key == pygame.K_s:
                    self.rot_vector = [
                        Main.ROT_K, 0., 0.] if event.type == pygame.KEYDOWN else [0., 0., 0.]
                elif event.key == pygame.K_PAGEUP and c_simulator.dt < .2:
                    pass
                elif event.key == pygame.K_PAGEDOWN and c_simulator.dt > .01:
                    pass
                    # c_simulator.dt = c_simulator.dt - .01
                elif event.key == pygame.K_p and event.type == pygame.KEYDOWN:
                    self.is_paused = not self.is_paused
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                quit()
        self.cam_pos = [self.cam_pos[0] + self.move_vector[0], self.cam_pos[1] +
                        self.move_vector[1], self.cam_pos[2] + self.move_vector[2]]
        self.cam_rot = [self.cam_rot[0] + self.rot_vector[0], self.cam_rot[1] +
                        self.rot_vector[1], self.cam_rot[2] + self.rot_vector[2]]
        self.g_manager.move_cam(self.move_vector)
        self.g_manager.rotate_cam(self.rot_vector)


main = Main()
main.run()
a = np.array([1, 1, 1])
b = np.array([2, 1, 4])
print(a)
print(b)
a = a * 1.5
b = b * 5.3
c = a + b
print(a)
print(b)
print(c)
