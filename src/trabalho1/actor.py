import area
import math
from OpenGL.GL import *


class Meteoro(area.Area):
    def __init__(self,n_vertices:int,radius_base=0.04,radius_diff=0.01):
        """
        Faz uma area circular de n_vertices com raio variável
        """
        
        vertices = []
        for angle in range(0,360,360//n_vertices):
            rad = math.radians(angle)
            point = (math.cos(rad),math.sin(rad))
            vertices.append(point)
        super().__init__(vertices, GL_TRIANGLE_FAN,(0.7,0.0,0.2))

class Star(area.Area):
    def __init__(self,n_vertices:int,radius=0.04):
        """
        Faz uma area circular de n_vertices, raio fixo e com método de triangle
        """
        vertices = []
        for angle in range(0,360,360//n_vertices):
            rad = math.radians(angle)
            point = (math.cos(rad),math.sin(rad))
            vertices.append(point)
        super().__init__(vertices, GL_TRIANGLE_FAN,(0.7,0.0,0.2))