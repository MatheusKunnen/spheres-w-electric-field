# @autor: Matheus Kunnen Ledesma - matheusl.2000@alunos.utfpr.edu.br

import numpy as np
import math

from VectorUtils import VectorUtils

class ChargeLines:

    DEFAULT_K_LINE = .25
    K_RADIUS = 1.5

    def __init__(self, max_distance, max_iterations, k_line = None):
        self.max_distance = max_distance
        self.max_iterations = max_iterations
        self.k_line = k_line if k_line != None else ChargeLines.DEFAULT_K_LINE
        self.l_bodies = []
        self.l_lines = []

    def generate_lines(self, min_e=0.000001):
        print("Generate Lines...Starting")
        # Reset variables
        self.l_lines = []
        init_points = []
        # Generate start points for the lines
        for body in self.l_bodies:
            # Using only positive charges to avoid generating redundant lines
            if body.b_charge < 0:
                continue
            init_points += body.get_charge_lines_init(2.)
        # Generate line for each point
        for point in init_points:
            # Start line
            line = []
            line.append(np.array(point))
            i = 0
            is_running = True
            while is_running: 
                p = np.array([0., 0., 0.])
                # Calculate de electric field
                for body in self.l_bodies:
                    p +=  body.get_electric_field(line[i])
                # Round to remove artifacts of too small numbers
                p = np.round(p, 15)
                norm = VectorUtils.norm(p)
                # Stops if electric field gets too weak
                if norm < min_e:
                    break
                # Get direction of the electric field & adjust its length
                if norm > self.k_line:
                    p = self.dir(p) * self.k_line

                # print(p) # DEBUG
                # Add point to line
                line.append(line[i] + p)
                i += 1
                # Checks max num iterations & distance from origin
                is_running =  i < self.max_iterations and self.norm_2(line[i]) < self.max_distance**2
                if is_running:
                    # Stops if any line enters in a body
                    for body in self.l_bodies:
                        if body.is_inside(line[i], 2.):
                            is_running = False
                            break
            # Add line to lines list
            self.l_lines.append(line)
        print(len(self.l_lines), "lines generated...")
        print("Generate Lines...Finished")

    def draw(self, g_manager):
        for line in self.l_lines:
            g_manager.draw_line(line)

    def add_body(self, body):
        self.l_bodies.append(body)

    # Obs: it shouldn't be here and it's ugly, but it works :)
    def dir(self, vec):
        return np.array(vec * 1. / np.linalg.norm(vec))

    # Obs: another method that shouldn't be here, but life is short
    def norm_2(self, vec):
        return (math.pow(vec[0], 2) + pow(vec[1], 2) + pow(vec[2], 2))