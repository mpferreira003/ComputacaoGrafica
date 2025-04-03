import area
import math
import random
import numpy as np
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
            self._x = (random.random()-0.5)*2
            self._y = (random.random()-0.5)*2
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
        """
        realiza um step para baixo
        """
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
        Faz duas áreas circulares (um interno e externo) e pega os vértices dos
          triângulos de forma dividida entre elas
        """
        if pos is None:
            self.modify(x=(random.random()-0.5)*2,
                        y=(random.random()-0.5)*2,
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
        super().__init__(vertices, GL_TRIANGLES,(1.0,1.0,1.0))
        
        
    ## Método que é chamado na main para animar o objeto
    def animate(self):    
        """
        Tem um contador que varia de 0 a self.animation_max_steps, fazendo ciclos de 
        aumentar e diminuir e alterando o escale nesse meio tempo
        """
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
            
            
## Objeto 3d
class Shot(area.Area):
    def __init__(self,head_length=2,body_length=7,size_div=100,
                 animate_move_step=0.01):
        """
        Veja a imagem do Shot para entender como estão sendo 
        feitos os vértices
        """
        self.animate_move_step = animate_move_step
        self.visible = False
        
        ## cálculo das distâncias do corpo
        part1 = 0
        part2 = part1 + head_length
        part3 = part2 + body_length
        part4 = part3 + head_length
        self.total_length = part4
        
        vertices = [
            (+0,part1,+0), ## base do tiro (0)
            
            (-1,part2,-1), ## quadrado inferior do tiro (1-4)
            (-1,part2,+1),
            (+1,part2,+1),
            (+1,part2,-1),
            
            (-1,part3,-1), ## quadrado superior do tiro (5-8)
            (-1,part3,+1),
            (+1,part3,+1),
            (+1,part3,-1),
            
            (+0,part4,+0) ## cabeça do tiro (9)
        ]
        
        ## marca as conexões que vão ter no objeto
        triangles = [
            ## triangulos da pirâmide inferior
            (0,1,2),
            (0,2,3),
            (0,3,4),
            (0,4,1),
            
            ## triangulos da pirâmide superior
            (9,5,6),
            (9,6,7),
            (9,7,8),
            (9,8,5),
            
            ## corpo do tiro
            ## direito
            (1,2,5), 
            (2,5,6),
            
            ## esquerdo
            (4,3,8),
            (3,8,7),
            
            ## superior
            (2,3,6),
            (3,6,7),
            
            ## inferior
            (1,4,5),
            (4,5,8)
        ]
        
        aux = []
        for triangle in triangles:
            i,j,k = triangle
            aux.append(vertices[i])
            aux.append(vertices[j])
            aux.append(vertices[k])
        
        
        vertices = np.array(aux,dtype='float64')
        vertices[:,0] -= (part4/2)  ## deixa o tiro no centro
        vertices /= size_div ## deixa o tiro pequeno
        vertices = vertices.tolist()
        super().__init__(vertices, GL_TRIANGLES,(0.8,0.8,0.0))
        
    def animate(self,ship_pos):
        """
        Fica indo pra cima, mas quando passa um pouco, volta pra 
        posição que está a nave
        """
        if self._y > 1.2:
            ## faz o tiro voltar para a posição da nave
            self._x = ship_pos[0]
            self._y = ship_pos[1]
        self.modify(y=self.animate_move_step)
     
## Objeto 3d   
class Ship(area.Area):
    def __init__(self,back_length=0.06,frontal_length=0.08,body_size=0.04,
                 animate_move_step=0.01):
        """
        Veja o esquema da nave para entender os pontos
        """
        self.animate_move_step = animate_move_step
        self._y = -0.75
        
        points = [
            (0,0,0), ## centro do corpo
            
            ## corpo principal
            (-body_size,-back_length,-body_size),
            (-body_size,-back_length,+body_size),
            (+body_size,-back_length,+body_size),
            (+body_size,-back_length,-body_size),
            
            (0,frontal_length,0) ## cabeça da nave
            
        ]
        
        ## Marcação das conexões dos triângulos
        triangles = [
            ## conexões da parte de dentro
            (0,1,2),
            (0,2,3),
            (0,3,4),
            (0,4,1),
            
            ## conexões da parte de fora
            (5,1,2),
            (5,2,3),
            (5,3,4),
            (5,4,1),
        ]
        
        vertices = []
        for triangle in triangles:
            i,j,k = triangle
            vertices.append(points[i])
            vertices.append(points[j])
            vertices.append(points[k])
        
        super().__init__(vertices, GL_TRIANGLES,(0.6,0.0,0.4))
    def animate(self,side):
        """
        Pode mover a nave tanto para a direita quanto pra esquerda
        """
        if side==0:
            pass
        elif side == -1:
            ## se move pra um lado
            self.modify(x=-self.animate_move_step,pivot='y',angle=0.1)
        elif side == 1:
            ## se move pro outro lado
            self.modify(x=+self.animate_move_step,pivot='y',angle=-0.1)
    def current_pos(self):
        return (self._x,self._y)
    

class Shield(area.Area):
    def __init__(self,n_vertices=80,shield_radius=0.2,external_radius=0.02):
        """
        Faz dois círculos, um interno e um externo, e conecta os pontos 
        através do STRIP
        """
        self.visible = False
        r1 = shield_radius
        r2 = r1 + external_radius
        
        circle1 = []
        for angle in range(0,360+90,(360+90)//n_vertices):
            angle_radians = math.radians(angle)
            
            point = (math.cos(angle_radians)*(r1),
                     math.sin(angle_radians)*(r1))
            circle1.append(point)
        
        circle2 = []
        for angle in range(0,360+90,(360+90)//n_vertices):
            angle_radians = math.radians(angle)
            
            point = (math.cos(angle_radians)*(r2),
                     math.sin(angle_radians)*(r2))
            circle2.append(point)
        
        vertices = []
        for i in range(n_vertices):
            vertices.append(circle1[i])
            vertices.append(circle2[i])
        super().__init__(vertices, GL_TRIANGLE_STRIP,(0.0,0.3,0.9))
        
    def animate(self,ship_pos):
        """
        Move o escudo para a posição da nave
        """
        if True:
            ## faz o tiro voltar para a posição da nave
            self._x = ship_pos[0]
            self._y = ship_pos[1]
        self.modify(y=0.001)