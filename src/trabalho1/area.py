import utils.posmath as posmath
import numpy as np
import utils.vertice as vertice
import utils.shaders as shaders
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
    visible=True
    pivot = 'z'
    
    def __init__(self,vertices,draw_method,color):
        self.mat_transform = np.eye(4,dtype=np.float32) ## considera que o objeto está no 0,0, com 0 graus e escala 1
        
        ## aplica um preprocessamento para objetos 2d, colocando 0 no eixo z
        if len(vertices[0])==2: ## caso seja um objeto 2d
            self.vertices = [(v[0],v[1],0) for v in vertices]
        else:
            self.vertices = vertices
        self.draw_method = draw_method
        self.color = color
        self.i_idx = None
        self.len_vertices = None
    def modify(self, x=0, y=0, sx=0, sy=0, 
               angle=0,pivot='z',
               instant_angle=False,
               instant_pos=False,
               instant_scale=False):
        """
        Prepara uma modificação para o objeto, que será 
        feita de fato quando for chamado o método draw
        """
        if instant_pos:
            # self.tx = 0
            # self.ty = 0
            self._x = x
            self._y = y
        else:
            self.tx = x
            self.ty = y
        
        if instant_scale:
            self._sx = sx
            self._sy = sy
        else:
            # self.tsx = 0
            # self.tsy = 0
            self.tsx = sx
            self.tsy = sy
        
        if instant_angle:
            # self.tangle = 0
            self._angle = angle
        else:
            self.tangle = angle
        
        self.pivot = pivot
    
    def reset(self):
        self.tx = 0
        self.ty = 0
        self.tsx = 0
        self.tsy = 0
        self.tangle = 0
        self.pivot='z'
    
    def prepare_to_draw(self):
        """
        Cria a matriz de transformação com base no que foi requisitado
        pelo modify (por meio da apply_on_matrix)
        """
        self._x += self.tx
        self._y += self.ty
        self._sx += self.tsx
        self._sy += self.tsy
        self._angle += self.tangle
        
        
        
        matriz_transformacao = self.apply_on_matrix()
        
        self.reset()
        
        return matriz_transformacao
    
    def apply_on_matrix(self):
        """
        Método que obtém a matriz de transformação com base no que foi definido no modify
        """
        if (self.tangle or self.tsx or self.tsy):
            ## escala, faz rotação e move (no mesmo eixo)
            # print("## escala, faz rotação e move (no mesmo eixo)")
            T = posmath.get_transl_matrix(self._x, self._y)
            S = posmath.get_scale_matrix(self._sx, self._sy, 1.0)
            R = posmath.get_rot_matrix(self._angle,pivot=self.pivot)
            self.mat_transform = (T @ (S @ (R)))
            self._x += self.tx
            self._y += self.ty
        
        elif (self.tx or self.ty):
            ## apenas move
            # print("## apenas move")
            self.mat_transform = posmath.get_transl_matrix(self._x, self._y)
            self._x += self.tx
            self._y += self.ty    
        return self.mat_transform
    
    
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
            len_vertices = len(area.vertices)
            area.i_idx = idx_init
            area.len_vertices = len_vertices
            idx_init+=len_vertices
            all_vertices.extend(area.vertices)
        vertices = vertice.create_vertice_array(len(all_vertices))
        vertices[shaders.SN_POSITION_NAME] = all_vertices
        return vertices
    
    @classmethod
    def draw_objects(cls,areas,loc_color,loc_matriz,just_triangles=False):
        """
        Desenha todos as areas visíveis na tela
        Args:
            areas:list[Area] - todas as áreas
            loc_color - vertex de cor
            loc_matriz - vertex da matriz
            just_triangles - caso seja true, mostra apenas os triangulos
        """
        if just_triangles:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE) ## ative esse comando para enxergar os triângulos
        else:
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        for area in areas:
            if area.visible:
                # Chama o método draw da instância para obter a matriz de transformação e aplica ela nos pontos
                matriz_transformacao = area.prepare_to_draw()
                glUniformMatrix4fv(loc_matriz, 1, GL_TRUE, matriz_transformacao)
                
                # Desenha de fato
                glUniform4f(loc_color, area.color[0], area.color[1], area.color[2], 1.0) ### modifica a cor do objeto
                glDrawArrays(area.draw_method, area.i_idx, area.len_vertices) ## desenha os pontos
        