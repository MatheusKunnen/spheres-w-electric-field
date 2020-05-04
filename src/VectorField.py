# @autor: Matheus Kunnen Ledesma - matheusl.2000@alunos.utfpr.edu.br

import numpy as np
from VectorUtils import VectorUtils

class VectorField:

    K_VECTOR = 0.5

    def __init__(self, size, dp, l_bodies, color=[.75, .5, .05, 1.]):
        self.size = np.round(size, 0)
        self.dp = np.array(dp)
        self.v_norm = 0.5
        self.l_bodies = l_bodies
        self.draw_control = True
        self.draw_plane = size[2]
        self.vectors_pos_l = []
        self.vectors_dir_l = []
        self.vector_color = np.array(color)
        self.init_vectors_pos()

    def init_vectors_pos(self):
        self.vectors_pos_l = []
        self.vectors_dir_l = []
        x = - self.size[0]
        while x <= self.size[0]:
            y = - self.size[1]
            while y <= self.size[1]:
                z = -self.size[2]
                while z <= self.size[2]:
                    self.vectors_pos_l.append(np.array([x, y, z]))
                    self.vectors_dir_l.append(np.array([.5, 0., 0.]))
                    z += self.dp[2]
                y += self.dp[1]
            x += self.dp[0]
        # print("VECTORS LEN ", len(self.vectors_pos_l))
        
    def update_vectors(self):
        print("Generating Vectors...")
        self.vectors_dir_l = []
        for point in self.vectors_pos_l:
            # Initial electric field
            e_vec = np.array([0., 0., 0.])
            # Calculate electric field
            for body in self.l_bodies:
                e_vec += body.get_electric_field(point)
            e_norm = VectorUtils.norm(e_vec)
            # Checks if the field is not 0
            if np.round(e_norm, 15) == 0:
                self.vectors_dir_l.append(np.array([0., 0., 0.]))
            else:
                e_dir = e_vec / e_norm
                self.vectors_dir_l.append(e_dir * VectorField.K_VECTOR)
        print(len(self.vectors_pos_l), "Vectors Generated...")

    def set_draw_control(self, draw_control):
        self.draw_control = draw_control

    def move_draw_plane(self, dp):
        if dp > 0:
            self.draw_plane += self.dp[2]
        else:
            self.draw_plane -= self.dp[2]

    def draw(self, g_manager):
        if not self.draw_control:
            for v_pos, v_dir in zip(self.vectors_pos_l, self.vectors_dir_l):
                g_manager.draw_vector(v_pos, v_dir, self.vector_color)
        else:
            for v_pos, v_dir in zip(self.vectors_pos_l, self.vectors_dir_l):
                if v_pos[2] == self.draw_plane:
                    g_manager.draw_vector(v_pos, v_dir, self.vector_color)