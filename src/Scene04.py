# @autor: Matheus Kunnen Ledesma - matheusl.2000@alunos.utfpr.edu.br

import numpy as np
import time
import math
import concurrent.futures
import pygame

from Consts import Consts
from OpenGLManager import OpenGLManager
from Body import Body
from Graph import Graph
from VectorField import VectorField
from FieldLines import FieldLines

class Scene04:


    def __init__(self):
        # Init General Parameters
        self.ring_v = []
        self.is_running = False
        self.is_paused = True
        self.dt = 1/60.0
        self.dt_k = 1.
        self.target_dt = 1/30.0
        self.t_total = 0
        self.controlled_body_enabled = False
        self.hud_enabled = True
        self.graphs_enabled = False
        self.vector_field_enabled = False
        self.line_charges_enabled = True

        # Init Bodies
        self.init_bodies()
        
        # Init Graphics Manager
        self.g_manager = OpenGLManager("Sphere in a Electric Field | Scene 04 | By: Matheus Kunnen ")
        self.move_vector = np.array([0., 0., 0.])
        self.rot_vector = np.array([0., 0., 0.])
        self.cam_pos = np.array([0, 20, -5])
        self.cam_rot = np.array([-40, 0, 0])
        self.g_manager.cam_pos = self.cam_pos
        self.g_manager.cam_rot = self.cam_rot

        # Init Graphs
        self.init_graphs()

        # Init Vector Field (Graphical R)
        self.init_vector_field()

        # Init charge lines
        self.init_field_lines()

    def init_bodies(self):
        Q = 10
        self.l_bodies = []
        # Body(self, b_id, b_radius, b_mass, b_pos, b_vel, b_charge):
        # Init controlled body
        self.controlled_body = Body(0, 0.1, 1., np.array([.0, .0, 0.]), np.array([0., 0., 0.]), Q * 0.01)
        self.E = np.array([0., 0., 0.])
        self.F = (0., 0., 0.)
        # Init bodies
        self.l_bodies.append(Body(2, .5, 1., np.array([4., 0., 4.]), np.array([0., 0., 0.]), Q))
        self.l_bodies.append(Body(2, .5, 1., np.array([4., 0., -4.]), np.array([0., 0., 0.]), -Q))
        self.l_bodies.append(Body(2, .5, 1., np.array([-4., 0., 4.]), np.array([0., 0., 0.]), -Q))
        self.l_bodies.append(Body(2, .5, 1., np.array([-4., 0., -4.]), np.array([0., 0., 0.]), Q))

    def init_graphs(self):
        graphs_s = [600, 80]
        graphs_offset = [-10, -20]
        n_points = 1000
        n = 1
        self.graph_f_x = Graph("Fx x t", ["t", "Fx"], n_points, 
                            np.array(graphs_s), 
                            np.array([self.g_manager.display_size[0] - graphs_s[0] +  graphs_offset[0], 
                            self.g_manager.display_size[1] - n*graphs_s[1] + n*graphs_offset[1]]))
        n += 1
        self.graph_f_y = Graph("Fy x t", ["t", "Fy"], n_points, 
                            np.array(graphs_s), 
                            np.array([self.g_manager.display_size[0] - graphs_s[0] + graphs_offset[0], 
                            self.g_manager.display_size[1] - n*graphs_s[1] + n*graphs_offset[1]]))
        n += 1
        self.graph_f_z = Graph("Fz x t", ["t", "Fz"], n_points, 
                            np.array(graphs_s), 
                            np.array([self.g_manager.display_size[0] - graphs_s[0] - 10, 
                            self.g_manager.display_size[1] - n*graphs_s[1] - n*20]))
        
    def init_vector_field(self):
        print("Init Vector Field...Starting")
        self.v_field = VectorField([8., 8., 8.], [1., 1., .5], l_bodies=self.l_bodies)
        self.v_field.vectors_dir_l = []
        self.update_vector_field()
        print("Init Vector Field...Finished")

    def init_field_lines(self):
        # Create charge line obj
        self.field_lines = FieldLines(160., 10000, .1, [1., 1.])
        # Add bodies
        for body in self.l_bodies:
            self.field_lines.add_body(body)
        # Generate Lines
        self.field_lines.generate_lines(min_e=0.0001)
        
    def run(self):
        self.is_running = self.g_manager.init_display()
        self.t_total = 0
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
        self.draw_graphs()
        self.draw_bodies()
        if self.vector_field_enabled:
            self.v_field.draw(self.g_manager)
        if self.line_charges_enabled:
            self.field_lines.draw(self.g_manager)

    def draw_bodies(self):
        for body in self.l_bodies:
            body.draw(self.g_manager)
        if self.controlled_body_enabled:
            self.controlled_body.draw(self.g_manager, True)
            # Draw force vector
            self.g_manager.draw_vector(self.controlled_body.b_pos, self.F, [1., 0., .8, 1.]) 

    def draw_graphs(self):
        if not self.graphs_enabled:
            return
        self.graph_f_x.draw(self.g_manager)
        self.graph_f_y.draw(self.g_manager)
        self.graph_f_z.draw(self.g_manager)

    def update(self):
        self.E = np.array([0., 0., 0.])
        for body in self.l_bodies:
            self.E += body.get_electric_field(self.controlled_body.b_pos)
        self.F = self.E * self.controlled_body.b_charge
        self.controlled_body.update(self.dt*self.dt_k)
        self.update_graphs()
    
    def update_graphs(self):
        self.graph_f_x.put(np.array([float(self.t_total), float(self.F[0])]))
        self.graph_f_y.put(np.array([float(self.t_total), float(self.F[1])]))
        self.graph_f_z.put(np.array([float(self.t_total), float(self.F[2])]))
        
        
    def update_vector_field(self):
        print("Generating Vectors...")
        for pos in self.v_field.vectors_pos_l:
            e_vec = np.array([0., 0., 0.])
            for body in self.l_bodies:
                e_vec += body.get_electric_field(pos)
            e_norm = math.sqrt(self.controlled_body.norm_e(e_vec))
            if e_norm == 0:
                self.v_field.vectors_dir_l.append(np.array([0., 0., 0.]))
                # continue
            else:
                e_dir = e_vec / e_norm
                self.v_field.vectors_dir_l.append(e_dir)
        print(len(self.v_field.vectors_pos_l), "Vectors Generated...")
    
            

    def draw_hud(self):
        if not self.hud_enabled:
            return
        txt_status = "Paused" if self.is_paused else "Running"
        self.g_manager.captions = [
            "-> General Parameters",
            f"    FPS: {round(1/self.dt,0)}",
            f"Runtime: {round(self.t_total, 3)}s.",
            f"   Play: x{round(self.dt_k,1)}",
            f"Cam. dP: {np.round(self.cam_pos, 2)}",
            f"Cam. dR: {np.round(self.cam_rot, 2)}",
            f" Status: {txt_status}", "",
            "-> Controlled Body ",
            f"     P: {np.round(self.controlled_body.b_pos, 3)}",
            # f"     V: {np.round(self.controlled_body.b_vel, 3)}",
            # f"     A: {np.round(self.controlled_body.b_aceleration, 3)}",
            f"  E(P): {np.round(self.E, 3)}",
            f"     Q: {np.round(self.controlled_body.b_charge, 3)}", ""
            # "-> Body 1",
            # f"     P: {np.round(self.body_1.b_pos, 3)}",
            # f"Radius: {round(self.body_1.b_radius,3)}",
            # f"     Q: {round(self.body_1.b_charge,3)}", "",
            # "-> Body 2",
            # f"     P: {np.round(self.body_2.b_pos, 3)}",
            # f"Radius: {round(self.body_2.b_radius,3)}",
            # f"     Q: {round(self.body_2.b_charge,3)}",
            ]
        self.g_manager.draw_captions()

    def update_dt(self, t1, t2):
        self.dt = t2 - t1
        self.t_total += self.dt if not self.is_paused else 0.
        if self.dt > self.target_dt:
            pass#print(f"FPS {round(1/self.dt,1)} | {round((self.dt - self.target_dt)/self.target_dt,1)} frames missed")
        else:
            self.g_manager.wait(self.target_dt - self.dt)

    def get_sim_dt(self):
        return self.target_dt*Consts.DT_K

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move_vector[0] = Consts.MOVE_K if event.type == pygame.KEYDOWN else 0.
                elif event.key == pygame.K_RIGHT:
                    self.move_vector[0] = - Consts.MOVE_K if event.type == pygame.KEYDOWN else 0.
                elif event.key == pygame.K_DOWN:
                    self.move_vector[1] = Consts.MOVE_K if event.type == pygame.KEYDOWN else 0.
                elif event.key == pygame.K_UP:
                    self.move_vector[1] = - Consts.MOVE_K if event.type == pygame.KEYDOWN else 0.
                elif event.key == pygame.K_q:
                    self.move_vector[2] = Consts.MOVE_K if event.type == pygame.KEYDOWN else 0.
                elif event.key == pygame.K_e:
                    self.move_vector[2] = - Consts.MOVE_K if event.type == pygame.KEYDOWN else 0.
                elif event.key == pygame.K_a:
                    self.rot_vector[1] = - Consts.ROT_K if event.type == pygame.KEYDOWN else 0.
                elif event.key == pygame.K_d:
                    self.rot_vector[1] = Consts.ROT_K if event.type == pygame.KEYDOWN else 0.
                elif event.key == pygame.K_w:
                    self.rot_vector[0] = - Consts.ROT_K if event.type == pygame.KEYDOWN else 0.
                elif event.key == pygame.K_s:
                    self.rot_vector[0] = Consts.ROT_K if event.type == pygame.KEYDOWN else 0.  
                elif event.key == pygame.K_h and event.type == pygame.KEYDOWN:
                    self.hud_enabled = not self.hud_enabled
                elif event.key == pygame.K_v and event.type == pygame.KEYDOWN:
                    self.vector_field_enabled = not self.vector_field_enabled
                elif event.key == pygame.K_PAGEUP and event.type == pygame.KEYDOWN:
                    self.dt_k += Consts.DT_K
                elif event.key == pygame.K_PAGEDOWN and event.type == pygame.KEYDOWN and round(self.dt_k - Consts.DT_K,1) > 0:
                    self.dt_k -= Consts.DT_K
                elif event.key == pygame.K_p and event.type == pygame.KEYDOWN:
                    self.is_paused = not self.is_paused
                elif event.key == pygame.K_g and event.type == pygame.KEYDOWN:
                    self.graphs_enabled = not self.graphs_enabled
                elif event.key == pygame.K_l and event.type == pygame.KEYDOWN:
                    self.line_charges_enabled = not self.line_charges_enabled
                elif event.key == pygame.K_b and event.type == pygame.KEYDOWN:
                    self.controlled_body_enabled = not self.controlled_body_enabled
                elif event.key == pygame.K_b and event.type == pygame.KEYDOWN:
                    self.v_field.set_draw_control(not self.v_field.draw_control)
                elif event.key == pygame.K_k and event.type == pygame.KEYDOWN:
                    self.v_field.move_draw_plane(1.)
                elif event.key == pygame.K_m and event.type == pygame.KEYDOWN:
                    self.v_field.move_draw_plane(-1.)
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                quit()
        if self.is_paused:
            self.cam_pos = [self.cam_pos[0] + self.move_vector[0], self.cam_pos[1] +
                            self.move_vector[1], self.cam_pos[2] + self.move_vector[2]]
            self.cam_rot = [self.cam_rot[0] + self.rot_vector[0], self.cam_rot[1] +
                            self.rot_vector[1], self.cam_rot[2] + self.rot_vector[2]]
            self.g_manager.move_cam(self.move_vector)
            self.g_manager.rotate_cam(self.rot_vector)
        else:
            self.controlled_body.b_pos = self.controlled_body.b_pos + self.move_vector 