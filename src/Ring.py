from Body import Body
import math
import numpy as np


class Ring:
    # Valores default
    D_N_BODIES = 360
    BODIES_RADIUS_K = 1.

    def __init__(self, r_pos, r_radius, r_charge):
        self.r_pos = r_pos
        self.r_radius = r_radius
        self.r_charge = r_charge
        self.set_n_bodies(Ring.D_N_BODIES)
        self.d_mass = 1
        self.generate_bodies()

    # Calcula valores relacionados com o nro de corpos
    def set_n_bodies(self, n_bodies):
        self.n_bodies = n_bodies
        self.ds = 2*math.pi/self.n_bodies
        self.r_bodies = (2 * math.pi * self.r_radius /
                         (self.n_bodies * 2)) * Ring.BODIES_RADIUS_K
        self.q_bodies = self.r_charge / self.n_bodies

    def draw(self, g_manager):
        for body in self.bodies_v:
            body.draw(g_manager)

    # Genera vetor com posicoes de cada pedaco do anel
    def generate_bodies(self):
        self.bodies_v = []
        n = 0
        while n < self.n_bodies:
            pos = [self.r_pos[0] + self.r_radius * math.cos(n*self.ds),
                   self.r_pos[1] + self.r_radius * math.sin(n*self.ds),
                   self.r_pos[2]]
            self.bodies_v.append(
                Body(n, self.r_bodies, self.d_mass, pos, [0, 0, 0], self.q_bodies))
            n += 1

    # Calcula campo eletrico gerado pelo anel completo
    def get_electric_field(self, pos):
        e_v = np.array([0., 0., 0.])
        for body in self.bodies_v:
            e_v += body.get_electric_field(pos)
        return np.round(e_v, 14)
