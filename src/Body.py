# @author: Matheus Kunnen Ledesma

import math
import numpy as np


class Body:
    # Constate de Coulomb
    K_C = 8.9875517873681764e9
    COLOR_RED = [.5, .01, .01, 1.0]
    COLOR_BLUE = [.01, .01, .5, 1.0]

    def __init__(self, b_id, b_radius, b_mass, b_pos, b_vel, b_charge):
        self.b_id = b_id
        self.b_radius = b_radius
        self.b_mass = b_mass
        self.b_pos = b_pos
        self.b_vel = b_vel
        self.b_charge = b_charge
        self.b_color = Body.COLOR_RED if self.b_charge > 0 else Body.COLOR_BLUE
        self.b_aceleration = np.array([0., 0., 0.])

    def update(self, dt):
        # Atualiza velocidade do corpo
        self.b_vel = self.b_vel + self.b_aceleration*dt
        # Atualiza posicao do corpo
        self.b_pos = self.b_pos + self.b_vel*dt  # + .5*self.b_aceleration*dt*dt

    def draw(self, g_manager, draw_vel_vector = False):
        g_manager.draw_solid_sphere(self.b_pos, self.b_radius, self.b_color)
        if draw_vel_vector:
            g_manager.draw_vector(self.b_pos, self.b_vel)

    def get_electric_field(self, p_pos):
        d = self.norm_e(np.array(p_pos - self.b_pos))
        if d <= self.b_radius:
            return np.array([0., 0., 0.])
        e = np.array(p_pos - self.b_pos)/math.sqrt(d) # Versor do campo eletrico
        k = self.b_charge / d # Modulo do campo eletrico
        return e * k

    def norm_e(self, v):
        return (math.pow(v[0], 2) + pow(v[1], 2) + pow(v[2], 2))
