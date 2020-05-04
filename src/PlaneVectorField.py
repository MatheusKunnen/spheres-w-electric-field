# @autor: Matheus Kunnen Ledesma - matheusl.2000@alunos.utfpr.edu.br

import numpy as np
from VectorUtils import VectorUtils

class PlaneVectorField:

    DEFAULT_V_COLOR = np.array([.8, .8, .8, 1.])

    def __init__(self, size, dp, l_bodies, color = None):
        self.size = size
        self.dp = dp
        self.l_bodies = l_bodies
        self.color = np.array(color) if color is not None else PlaneVectorField.DEFAULT_V_COLOR
        self.init_vectors_pos()
        self.update_vectors()

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
            if e_norm == 0:
                self.vectors_dir_l.append(np.array([0., 0., 0.]))
            else:
                e_dir = e_vec / e_norm
                self.vectors_dir_l.append(e_dir)
        print(len(self.vectors_pos_l), "Vectors Generated...")

    def move(self, dir, update_vectors=True):
        self.pos += dir
        self.init_vectors_pos()
        if update_vectors:
            self.update_vectors()

    def draw(self, g_manager):
        for v_pos, v_dir in zip(self.vectors_pos_l, self.vectors_dir_l):
            g_manager.draw_vector(v_pos, v_dir, self.color)


