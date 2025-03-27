import posmath
import numpy as np
from OpenGL.GL import glClear, glClearColor, GL_COLOR_BUFFER_BIT

class Area():

    _x = 0
    _y = 0
    _angle = 0

    tx = 0
    ty = 0
    tangle = 0

    def __init__(self,vertices):
        self.x,self.y = 0, 0 ## considera que o objeto foi instanciado no 0,0
        self.mat_transform = np.eye(4) ## considera que o objeto está no 0,0, com 0 graus e escala 1
    
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
            
        