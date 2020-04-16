# @author: Matheus Kunnen Ledesma
import numpy as np

from Queue import Queue

class Graph:

    # General Constansts
    SCALE_K = 0.98

    def __init__(self, title, axes, max_points, g_size, g_pos):
        self.title = title
        self.axes = axes
        self.max_points = max_points
        self.g_size = g_size
        self.g_pos = g_pos
        self.points_queue = Queue(self.max_points)
        self.max_v = np.array([0., 0.])
        self.min_v = np.array([0., 0.])
        self.g_scale = np.array([1., 1.])
        #self.test_data()

    # Test data in DEBUG
    def test_data(self):
        for i in range(0, 40):
          self.put(np.array([i/2., i*i/2.]))

    # Add point to graph
    def put(self, point):
        self.points_queue.put(point)

    # Draw graph
    def draw(self, g_manager):
        if self.points_queue.is_empty():
            return
        self.update_edge_values()
        self.update_scale()
        g_manager.draw_2d_graph(self.g_pos, self.g_size, self.g_scale, self.min_v, self.points_queue.elements, self.get_caption())

    # Return graph's caption
    def get_caption(self):
        return f"{self.title} | {round(self.min_v[0],2)} < {self.axes[0]} < {round(self.max_v[0],2)} | {round(self.min_v[1],2)} < {self.axes[1]} < {round(self.max_v[1],2)}"

    # Updates min & max values of each axis
    def update_edge_values(self):
        self.max_v = np.array(self.points_queue.elements[0]) if not self.points_queue.is_empty() else np.array([0., 0.])
        self.min_v = np.array(self.points_queue.elements[0]) if not self.points_queue.is_empty() else np.array([0., 0.])
        for point in self.points_queue.elements:
            # print("MIN MAX POINT", self.min_v, self.max_v, point)
            for i, val in enumerate(point):
                if val > self.max_v[i]:
                    # print("MAX CHANGED ", self.max_v[i], " -> ", val)
                    self.max_v[i] = float(val)
                if val < self.min_v[i]:
                    # print("MIN CHANGED ", self.min_v[i], " -> ", val)
                    self.min_v[i] = float(val)
    
    # Updates scale factor for graph for each axis
    def update_scale(self):
        delta_v = self.max_v - self.min_v
        self.g_scale[0] = float(self.g_size[0])*Graph.SCALE_K/delta_v[0]
        self.g_scale[1] = float(self.g_size[1])*Graph.SCALE_K/delta_v[1]
        #print("MAX MIN DELTA SCALE", self.max_v, self.min_v, delta_v, self.g_scale)

