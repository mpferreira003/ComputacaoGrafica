import posmath
import numpy as np
import vertice
import shaders
from OpenGL.GL import *

class Area():

    _x = 0
    _y = 0
    _angle = 0

    tx = 0
    ty = 0
    tangle = 0

    def __init__(self,vertices,draw_method,color):
        self.x,self.y = 0, 0 ## considera que o objeto foi instanciado no 0,0
        self.mat_transform = np.eye(4) ## considera que o objeto está no 0,0, com 0 graus e escala 1
        self.vertices = vertices
        self.draw_method = draw_method
        self.color = color
    def modify(self, x, y, angle):
        self.tx = x
        self.ty = y
        self.tangle = angle

    def reset(self):
        self.tx = 0
        self.ty = 0
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

    def transform(self):
        """
        Aplica a transformação em todos os vértices
        """
        ## desloca para o 0,0
        
        ## volta para o x,y 
    
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
    def get_draw_schema(cls, area_list):
        """
        a partir de uma lista de áreas, retorna o esquema de como 
        desenhar elas.
        
        Args:
            area_list:list[Area] - lista das áreas
        Return:
            draw_schema:list[tuple] - lista de tuplas no formato (init,fim,draw_method,color)]
            vertices - lista dos vertices a serem usados para desenho
        """
        draw_schema = []
        all_vertices = []
        idx_init = 0
        for area in area_list:
            idx_final = len(area.vertices)
            draw_schema.append((idx_init,idx_final,area.draw_method,area.color))
            all_vertices.extend(area.vertices)
            idx_init=idx_final+1
            
        vertices = vertice.create_vertice_array(len(all_vertices))
        vertices[shaders.SN_POSITION_NAME] = all_vertices
        return draw_schema,vertices
    
    @classmethod
    def draw_objects(cls,draw_schema,loc_color,just_triangles=False):
        if just_triangles:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE) ## ative esse comando para enxergar os triângulos
    
        for i_idx,f_idx,dmethod,(R,G,B) in draw_schema:
            glDrawArrays(dmethod, i_idx, f_idx) ## desenha os pontos
            glUniform4f(loc_color, R, G, B, 1.0) ### modifica a cor do objeto
        