import posmath
import numpy as np
import vertice
import shaders
from OpenGL.GL import *


class Area():
    
    ## valores reais do objeto
    _x = 0
    _y = 0
    _sx = 1
    _sy = 1
    _angle = 0
    
    
    ## valores de incremento no objeto
    tx = 0
    ty = 0
    tsx = 0
    tsy = 0
    tangle = 0
    
    def __init__(self,vertices,draw_method,color):
        self.x,self.y = 0, 0 ## considera que o objeto foi instanciado no 0,0
        self.mat_transform = np.eye(4) ## considera que o objeto está no 0,0, com 0 graus e escala 1
        self.vertices = vertices
        self.draw_method = draw_method
        self.color = color
        self.i_idx = None
        self.f_idx = None
    def modify(self, x, y, sx, sy, angle,
               instant_angle=False,
               instant_pos=False,
               instant_scale=False):
        """
        Prepara uma modificação para o objeto, que será 
        feita de fato quando for chamado o método draw
        """
        if instant_pos:
            self.tx = 0
            self.ty = 0
            self._x = x
            self._y = y
        else:
            self.tx = x
            self.ty = y
        
        if instant_scale:
            self._sx = sx
            self._sy = sy
        else:
            self.tsx = 0
            self.tsy = 0
            self.tsx = sx
            self.tsy = sy
        
        if instant_angle:
            self.tangle = 0
            self._angle = angle
        else:
            self.tangle = angle
    
    def reset(self):
        self.tx = 0
        self.ty = 0
        self.tsx = 0
        self.tsy = 0
        self.tangle = 0

    def draw(self):
        self._x += self.tx
        self._y += self.ty
        self._angle += self.tangle

        matriz_transformacao = np.array([    1.0, 0.0, 0.0, 0.0, 
                                    0.0, 1.0, 0.0, 0.0, 
                                    0.0, 0.0, 1.0, 0.0, 
                                    0.0, 0.0, 0.0, 1.0], np.float32)
        if(self.tangle):
            matriz_transformacao = self.rotateOn()
        
        self.reset()
        
        return matriz_transformacao
    
    def move(self,x,y,relative=True):
        pass
    def rotateOn(self):
        # 1. Translação para a origem
        pos = posmath.get_transl_matrix(-self._x, -self._y)
        
        # 2. Rotação em torno da origem
        rotation = posmath.get_rot_matrix(self._angle)
        
        # 3. Translação de volta para a posição original
        pos_anti = posmath.get_transl_matrix(self._x, self._y)
        
        # Combina as matrizes: pos_anti @ rotation @ pos
        # return pos_anti @ rotation @ pos
        return  (pos_anti @ (rotation @ (pos)))
    
    @classmethod
    def get_world_vertices(cls, area_list):
        """
        a partir de uma lista de áreas, retorna a lista global de vértices
        
        Args:
            area_list:list[Area] - lista das áreas
        Return:
            vertices - lista dos vertices a serem usados para desenho
        """
        
        all_vertices = []
        idx_init = 0
        for area in area_list:
            idx_final = len(area.vertices)
            area.i_idx = idx_init
            area.f_idx = idx_final
            all_vertices.extend(area.vertices)
            idx_init=idx_final+1
            
        vertices = vertice.create_vertice_array(len(all_vertices))
        vertices[shaders.SN_POSITION_NAME] = all_vertices
        return vertices
    
    @classmethod
    def draw_objects(cls,areas,loc_color,loc_matriz,just_triangles=False):
        if just_triangles:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE) ## ative esse comando para enxergar os triângulos
    
        for area in areas:
            # Chama o método draw da instância para obter a matriz de transformação e aplica ela nos pontos
            matriz_transformacao = area.draw()
            glUniformMatrix4fv(loc_matriz, 1, GL_TRUE, matriz_transformacao)
            
            # Desenha de fato
            glDrawArrays(area.draw_method, area.i_idx, area.f_idx) ## desenha os pontos
            glUniform4f(loc_color, area.color[0], area.color[1], area.color[2], 1.0) ### modifica a cor do objeto
        