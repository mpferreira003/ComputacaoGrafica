import posmath
import numpy as np

class Area():
    def __init__(self,vertices):
        self.x,self.y = 0 ## considera que o objeto foi instanciado no 0,0
        self.mat_transform = np.eye(4) ## considera que o objeto está no 0,0, com 0 graus e escala 1
    def draw(self):
        pass
    def transform(self):
        """
        Aplica a transformação em todos os vértices
        """
        ## desloca para o 0,0
        
        ## volta para o x,y 
    
    def move(self,x,y,relative=True):
        pass
    def rotateOn(pivot,relative=True):
        # 1. Translação para a origem
        pos = get_transl_matrix(-tx, -ty)
        
        # 2. Rotação em torno da origem
        rotation = get_rot_matrix(angle)
        
        # 3. Translação de volta para a posição original
        pos_anti = get_transl_matrix(tx, tty)
        
        # Combina as matrizes: pos_anti @ rotation @ pos
        # return pos_anti @ rotation @ pos
        return  (pos_anti @ (rotation @ (pos)))
            
        