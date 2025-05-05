import loader
import OpenGL.GL as opengl
import numpy as np
import glm
import math
import matriz


class Model():
    ## valores reais do objeto
    pos = np.zeros(3)
    scale = np.ones(3)
    rotation = np.zeros(3)
    angle = 0
    
    
    ## valores de incremento no objeto
    add_pos = np.zeros(3)
    add_scale = np.zeros(3)
    add_rotation = np.zeros(3)
    add_angle = 0
    
    visible=True
    
    
    
    def __init__(self, vertice_inicial:int, qtd_vertices:int,texture_id:int):
        self.verticeInicial  = vertice_inicial
        self.quantosVertices = qtd_vertices
        self.texture_id=texture_id
        
        
    def modify(self, add_pos:np.ndarray=np.zeros(3),add_rot:np.ndarray=np.zeros(3),add_scale:np.ndarray=np.zeros(3),angle:float=0,
               instant_angle=False,
               instant_pos=False,
               instant_scale=False):
        """
        Prepara uma modificação para o objeto, que será 
        feita de fato quando for chamado o método draw
        """
        if instant_pos:
            self.pos += add_pos
        else:
            self.pos = add_pos
            
        if instant_scale:
            self.scale += add_scale
        else:
            self.scale = add_scale
            
        if instant_angle:
            self.rotation += add_rot
        else:
            self.rotation = add_rot
        
        self.add_angle += angle
    def reset(self):
        self.add_pos = np.zeros(3)
        self.add_rotation = np.zeros(3)
        self.add_scale = np.ones(3)
        self.add_angle = 0
        
    
    
    
    def draw(self, program):
        mat_model = matriz.model_matrix(self.angle, self.pos, self.rotation, self.scale)
        loc_model = opengl.glGetUniformLocation(program, "model")
        opengl.glUniformMatrix4fv(loc_model, 1, opengl.GL_TRUE, mat_model)
            
        #define id da textura do modelo
        opengl.glBindTexture(opengl.GL_TEXTURE_2D, self.texture_id)
        
        # desenha o modelo
        opengl.glDrawArrays(opengl.GL_TRIANGLES, self.verticeInicial, self.quantosVertices) ## renderizando
