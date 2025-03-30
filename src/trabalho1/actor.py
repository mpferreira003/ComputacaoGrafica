import area
import math
import random
from OpenGL.GL import *


class Meteoro(area.Area):
    def __init__(self,n_vertices:int=7,radius_base=0.4,radius_diff=0.2):
        """
        Faz uma area circular de n_vertices com raio variável
        """
        
        vertices = []
        for angle in range(0,360,360//n_vertices):
            angle_radians = math.radians(angle)
            radius = radius_base + (random.random()-0.5)*radius_diff
            
            point = (math.cos(angle_radians)*(radius),
                     math.sin(angle_radians)*(radius))
            vertices.append(point)
        super().__init__(vertices, GL_TRIANGLE_FAN,(0.6,0.2,0.0))

class Star(area.Area):
    def __init__(self,n_vertices:int=5,intern_radius=0.1,extern_radius=0.4):
        """
        Faz duas áreas circulares e pega os vértices dos triângulos de forma dividida entre elas
        """
        angle_step = 360//n_vertices
        
        intern_circle_points = []
        for angle in range(0,360,angle_step):
            angle_radians = math.radians(angle)
            point = (math.cos(angle_radians)*(intern_radius),
                     math.sin(angle_radians)*(intern_radius))
            intern_circle_points.append(point)
        
        extern_circle_points = []
        for angle in range(0+angle_step,360+angle_step,angle_step):
            angle_radians = math.radians(angle)
            point = (math.cos(angle_radians)*(extern_radius),
                     math.sin(angle_radians)*(extern_radius))
            extern_circle_points.append(point)
        
        vertices = []
        for i in range(n_vertices):
            vertices.append(intern_circle_points[i])
            vertices.append(intern_circle_points[(i+2)%n_vertices])
            vertices.append(extern_circle_points[i])
        super().__init__(vertices, GL_TRIANGLES,(1.0,1.0,1.0))