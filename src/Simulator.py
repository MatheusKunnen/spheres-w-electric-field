import numpy as np
import random as rand
import concurrent.futures
from Body import Body


class Simulator:

    momentum = 0.  # Momento total do sistema

    b_pos = []  # Vetor de posicoes
    b_vel = []  # Vetor de velocidades
    v_med = []  # Vetor da velocidade media
    r_cm = []   # Vecor do cm do sistema
    b_status = []  # Estado das bolas

    def __init__(self, n_balls, b_radius, c_length, dt, max_v0):
        self.n_balls = n_balls
        self.b_radius = b_radius
        self.time = 0
        self.c_length = c_length
        self.dt = dt
        self.max_v0 = max_v0
        self.c_limit = self.c_length/2 - self.b_radius
        self.d_min = self.b_radius * 2
        self.d_min2 = self.d_min*self.d_min
        self.generate_bodies()

    def generate_bodies(self):
        count = 0
        self.l_bodies = []  # Lista de esferas
        dx = dy = dz = 3.  # Variação da distancia entre esferas
        x = y = z = -self.c_length/2 + self.d_min

        while count < self.n_balls:

            vel_a = np.array([rand.randrange(-self.max_v0, self.max_v0),
                              rand.randrange(-self.max_v0,
                                             self.max_v0),
                              rand.randrange(-self.max_v0, self.max_v0)])
            vel_b = np.array([rand.randrange(-self.max_v0, self.max_v0),
                              rand.randrange(-self.max_v0,
                                             self.max_v0),
                              rand.randrange(-self.max_v0, self.max_v0)])

            pos_a = np.array([round(x, 3), round(y, 3), round(z, 3)])
            pos_b = np.array([round(-x, 3), round(y, 3), round(-z, 3)])

            self.l_bodies.append(Body(count+1, self.b_radius, pos_a, vel_a))
            self.l_bodies.append(Body(count+2, self.b_radius, pos_b, vel_b))

            x += dx*self.b_radius

            if abs(x) > abs(self.c_length/2 - 3*self.b_radius):
                dx *= -1
                y += dy*self.b_radius

                if abs(y) > abs(self.c_length/2 - 3*self.b_radius):
                    dy *= -1
                    z += dz*self.b_radius

            count += 2

    def update(self):
        self.move()
        self.sort_bodies()
        self.check_collisions()
        self.calculate_dynamics()

    def move(self):
        for body in self.l_bodies:
            body.move(self.dt)
            body.check_wall_collision(self.c_limit)

    def sort_bodies(self):
        self.l_bodies.sort(key=self.sort_body)

    def sort_body(self, body):
        return body.b_pos[0]

    def check_collisions(self):
        for b1 in range(0, self.n_balls - 1):
            for b2 in range(b1 + 1, self.n_balls):
                d_pos = self.l_bodies[b1].b_pos - self.l_bodies[b2].b_pos
                if d_pos[0] <= self.d_min:
                    if d_pos[1] <= self.d_min and d_pos[2] <= self.d_min:
                        if self.sqrNorm(self.l_bodies[b1].b_pos - self.l_bodies[b2].b_pos) <= self.d_min2:
                            self.on_collision(b1, b2)
                else:
                    break

    def sqrNorm(self, vector):
        sqr_norm = 0
        for num in vector:
            sqr_norm += num*num
        return sqr_norm

    def on_collision(self, b1, b2):
        self.l_bodies[b1].b_collisioned = True
        self.l_bodies[b2].b_collisioned = True
        normal = (self.l_bodies[b1].b_pos - self.l_bodies[b2].b_pos) / np.linalg.norm(
            self.l_bodies[b1].b_pos - self.l_bodies[b2].b_pos)  # Direcao normal da colisao
        # Velocidade relativa entre os corpos
        v_r = self.l_bodies[b1].b_vel - self.l_bodies[b2].b_vel
        # Velocidade relativa na direcao normal da colisao
        v_normal = np.dot(v_r, normal) * normal
        self.l_bodies[b1].b_vel = self.l_bodies[b1].b_vel - v_normal
        self.l_bodies[b2].b_vel = self.l_bodies[b2].b_vel + v_normal

    def calculate_dynamics(self):
        self.momentum = 0
        self.v_med = np.array([0., 0., 0.])
        self.r_cm = np.array([0., 0., 0.])
        for i in range(self.n_balls - 1):
            self.momentum += np.linalg.norm(self.l_bodies[i].b_vel)
            self.v_med = np.add(self.v_med, self.l_bodies[i].b_vel)
            self.r_cm = np.add(self.r_cm, self.l_bodies[i].b_pos)
        self.v_med = self.v_med / self.n_balls
        self.r_cm = self.r_cm / self.n_balls
