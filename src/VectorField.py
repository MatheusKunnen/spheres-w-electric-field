# @author: Matheus Kunnen Ledesma
import numpy as np

class VectorField:

    def __init__(self, size, dp):
        self.size = np.round(size, 0)
        self.dp = np.array(dp)
        self.v_norm = 0.5
        self.vectors_pos_l = []
        self.vectors_dir_l = []
        self.vector_color = np.array([0., .5, .5, 1.])
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

    def draw(self, g_manager):
        for v_pos, v_dir in zip(self.vectors_pos_l, self.vectors_dir_l):
            g_manager.draw_vector(v_pos, v_dir, self.vector_color)