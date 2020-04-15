# @author: Matheus Kunnen Ledesma

import math
import numpy as np

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class OpenGLManager:
    """ General parameters """
    display_size = (1200, 800)  # Tamanho da janela a abrir
    sphere_slices = 10          # Divisioes das bolas (> -> Maior Qualidade)
    text_pos = (10, 750)        # Posicao inicial do texto
    text_dP = 175               # Distancia entre linhas do texto
    D_RENDER_DISTANCE = 100     # Distancia maxima de renderizado
    STROKE_W = 2.               # Tamanho de Linhas
    """ Ilumination parameters """
    # Posicao da fonte de iluminacao
    LIGHT_ZERO_POSITION = [0, 0, 24, .5]
    # Cor da fonte de iluminacao
    LIGHT_ZERO_COLOR = [1., 1., 1., 1.]
    # Posicao da fonte de iluminacao ambiente
    LIGHT_ZERO_AMBIENT = [1., 1., 1., .1]
    # Cor da fonte de direta?
    LIGHT_ZERO_SPECULAR = [1., 1., 1., .5]

    """ Camera parameters """
    cam_pos = [0, 0, 0]     # Posicao da camera (visao)
    cam_rot = [0, 0, 0]     # Rotacao da camera
    # Rotacao da camera no eixo x (visao)
    camera_rot_x = 30.
    # Rotacao da camera no eixo y (visao)
    camera_rot_y = 30.

    """ Colors """
    COLOR_BLACK = [0., 0., 0., 1.]
    COLOR_WHITE = [1., 1., 1., 1.]
    cube_color = [1., 0., 0., 1.]                       # Cor do frame do Cubo
    vector_color = [1, 1, 1, 1]             # Cor da esfera
    # Cor da sombra da esfera
    sphere_diffuse_color = [.01, .01, .01, 1.]
    sphere_ambient_color = [.1, .1, .1, .1]             # Cor da esfera
    # Cor da reflexão da esfera
    sphere_specular_color = [.01, .01, .01, 1.1]
    sphere_collision_diffuse_color = [1., .0, 0., 1.]   # Cor das bolas
    sphere_collision_ambient_color = [.5, .0,
                                      0., .1]   # Cor ambiente? das bolas

    def __init__(self, display_title, bg_color=COLOR_WHITE):
        self.running = False
        self.display_title = display_title
        self.render_distance = OpenGLManager.D_RENDER_DISTANCE
        self.bg_color = np.array(bg_color)
        self.captions = []
        self.init_colors()

    def init_colors(self):
        self.vector_color = self.text_color = self.p_color = np.array([1., 1., 1., 2.]) - self.bg_color
         

    def init_display(self):
        if self.running:
            return True
        # Init Window
        pygame.init()
        pygame.display.set_mode(
            self.display_size, pygame.DOUBLEBUF | OPENGL)
        pygame.display.set_caption(self.display_title)
        pygame.display.gl_set_attribute(GL_ACCELERATED_VISUAL, True)
        # Config window
        glClearColor(self.bg_color[0], self.bg_color[1],
                     self.bg_color[2], self.bg_color[3])
        glShadeModel(GL_SMOOTH)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glCullFace(GL_BACK)
        # Init light
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.LIGHT_ZERO_AMBIENT)
        glLightfv(GL_LIGHT0, GL_POSITION, self.LIGHT_ZERO_POSITION)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.LIGHT_ZERO_COLOR)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.LIGHT_ZERO_SPECULAR)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.5)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.01)
        glEnable(GL_LIGHT0)

        # Init Camera
        glMatrixMode(GL_PROJECTION)
        gluPerspective(
            45, (self.display_size[0] / self.display_size[1]), 0.1, self.render_distance)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        # Pos Camera
        self.set_cam_pos(self.cam_pos)
        self.rotate_cam(self.cam_rot)

        self.running = True
        return True

    def set_cam_pos(self, cam_pos):
        self.cam_pos = cam_pos
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(cam_pos[0], cam_pos[1], cam_pos[2])
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    def move_cam(self, cam_move):
        # init model view matrix
        glLoadIdentity()

        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        glTranslatef(cam_move[0], cam_move[1], cam_move[2])

        # apply rotation
        glRotatef(self.cam_rot[0], 1., 0., 0.)
        glRotatef(self.cam_rot[1], 0., 1., 0.)

        # multiply the current matrix by the get the new view matrix and store the final vie matrix
        glMultMatrixf(self.viewMatrix)
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # apply view matrix
        glPopMatrix()
        glMultMatrixf(self.viewMatrix)

    def rotate_cam(self, cam_rot):
        self.cam_rot = cam_rot
        # init model view matrix
        glLoadIdentity()

        # apply the look up and down
        glRotatef(cam_rot[0], 1., 0., 0.)
        glRotatef(cam_rot[1], 0., 1., 0.)

        # multiply the current matrix by the get the new view matrix and store the final vie matrix
        glMultMatrixf(self.viewMatrix)
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)


    def clear_buffer(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def swap_buffers(self):
        glutSwapBuffers()
        pygame.display.flip()

    def wait(self, time):
        pygame.time.wait(int(time))

    def draw_captions(self):
        """ Set 2D mode"""
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0.0, self.display_size[0], 0.0, self.display_size[1])
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glLineWidth(OpenGLManager.STROKE_W)
        glTranslatef(self.text_pos[0], self.text_pos[1], 0)
        glScalef(0.1, 0.1, 0.1)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.text_color)
        for i, caption in enumerate(self.captions):
            glPushMatrix()
            glTranslatef(0,
                         - i*self.text_dP, 0)
            for j in range(len(caption)):
                glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN,
                                    ord(caption[j]))
            glPopMatrix()

        """ Making sure we can render 3d again """
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def draw_solid_sphere(self, sphere_pos, sphere_radius, sphere_ambient_color=sphere_ambient_color):
        glPushMatrix()
        K = 1.5
        glMaterialfv(GL_FRONT, GL_AMBIENT, sphere_ambient_color)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [
                     sphere_ambient_color[0]*K,
                     sphere_ambient_color[1]*K,
                     sphere_ambient_color[2]*K,
                     1])
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.sphere_specular_color)
        glTranslatef(sphere_pos[0], sphere_pos[1], sphere_pos[2])
        glutSolidSphere(sphere_radius, self.sphere_slices, self.sphere_slices)
        glPopMatrix()

    def draw_cube_frame(self, cube_length, cube_color=cube_color):
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, cube_color)
        glTranslatef(0, 0, 0)
        glutWireCube(cube_length)
        glPopMatrix()

    def draw_vector(self, p_0, p_1):
        glPushMatrix()
        # Config stroke
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.p_color)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)
        glLineWidth(OpenGLManager.STROKE_W)
        # Draw Stroke
        glBegin(GL_LINES)
        glVertex3f(p_0[0], p_0[1], p_0[2])
        glVertex3f(p_0[0]+p_1[0], p_0[1]+p_1[1], p_0[2]+p_1[2])
        glEnd()
        # Draw Point
        glTranslatef(p_0[0]+p_1[0], p_0[1]+p_1[1], p_0[2]+p_1[2])
        glutSolidSphere(.005, self.sphere_slices, self.sphere_slices)
        glPopMatrix()
