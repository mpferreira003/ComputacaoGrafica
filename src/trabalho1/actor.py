import area
import math
import random
from OpenGL.GL import *


class Meteoro(area.Area):
    def __init__(self,n_vertices:int=7,
                 radius_base=0.4,
                 radius_diff=0.2,
                 animate_move_step=0.001,
                 animate_angle_step=0.01,
                 pos=None
                 ):
        """
        Faz uma area circular de n_vertices com raio variável
        """
        self.animate_move_step = animate_move_step
        self.animate_angle_step = animate_angle_step
        if pos is None:
            self._x = (random.random()-0.5)*0.8*2
            self._y = (random.random()-0.5)*0.8*2
        else:
            self._x = pos[0]
            self._y = pos[1]
        
        vertices = []
        for angle in range(0,360,360//n_vertices):
            angle_radians = math.radians(angle)
            radius = radius_base + (random.random()-0.5)*radius_diff*2
            
            point = (math.cos(angle_radians)*(radius),
                     math.sin(angle_radians)*(radius))
            vertices.append(point)
        super().__init__(vertices, GL_TRIANGLE_FAN,(0.6,0.2,0.0))
    
    def animate(self):
        self.modify(y=-self.animate_move_step,angle=self.animate_angle_step)
        
        

class Star(area.Area):
    animation_step = 0 ## controla a quantidade de steps a serem feitas
    animation_state = False ## controla se a estrela está aumentando ou diminuindo
    
    
    def __init__(self,n_vertices:int=5,
                 intern_radius=0.1,
                 extern_radius=0.4, 
                 animation_max_steps = 10,
                 pos = None):
        """
        Faz duas áreas circulares e pega os vértices dos triângulos de forma dividida entre elas
        """
        if pos is None:
            self.modify(x=(random.random()-0.5)*0.8*2,
                        y=(random.random()-0.5)*0.8*2,
                        instant_pos=True)
        else:
            self._x = pos[0]
            self._y = pos[1]
        
        self.animation_max_steps = animation_max_steps
        self.animation_increment = 1/animation_max_steps
        angle_step = 360//n_vertices
        
        intern_circle_points = []
        for angle in range(0,360,angle_step):
            angle_radians = math.radians(angle)
            point = (math.cos(angle_radians)*(intern_radius),
                     math.sin(angle_radians)*(intern_radius))
            intern_circle_points.append(point)
        
        extern_circle_points = []
        for angle in range(0+angle_step//2,360+angle_step//2,angle_step):
            angle_radians = math.radians(angle)
            point = (math.cos(angle_radians)*(extern_radius),
                     math.sin(angle_radians)*(extern_radius))
            extern_circle_points.append(point)
        
        vertices = []
        for i in range(n_vertices):
            vertices.append(intern_circle_points[i])
            vertices.append(intern_circle_points[(i+1)%n_vertices])
            vertices.append(extern_circle_points[i])
        print("Len vertices star: ",len(vertices))
        super().__init__(vertices, GL_TRIANGLES,(1.0,1.0,1.0))
        
        
    ## Método que é chamado na main para animar o objeto
    def animate(self):    
        if self.animation_state:
            self.animation_step-=1
            if self.animation_step-1<=0:
                self.animation_state=False
                
            self.modify(sx=self.animation_increment, sy=self.animation_increment)
        else:
            self.animation_step+=1
            if self.animation_step+1>=self.animation_max_steps:
                self.animation_state=True
            self.modify(sx=-self.animation_increment, sy=-self.animation_increment)