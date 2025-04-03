import numpy as np
import math
import numpy as np
import math

def get_rot_matrix(angle, pivot='z'):
    """
    Retorna uma matriz de rotação 4x4 em torno de um eixo específico.
    
    Parâmetros:
        angle: Ângulo de rotação em radianos.
        pivot: Eixo de rotação ('x', 'y' ou 'z').
    
    Retorno:
        Matriz de rotação 4x4.
    """
    c = math.cos(angle)
    s = math.sin(angle)
    
    if pivot.lower() == 'z':
        # Rotação em torno do eixo Z (padrão)
        return np.array([
            [c, -s, 0.0, 0.0],
            [s,  c, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)
    
    elif pivot.lower() == 'x':
        # Rotação em torno do eixo X
        return np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0,  c, -s, 0.0],
            [0.0,  s,  c, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)
    
    elif pivot.lower() == 'y':
        # Rotação em torno do eixo Y
        return np.array([
            [ c, 0.0,  s, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-s, 0.0,  c, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)
    
    else:
        raise ValueError("Eixo inválido")

def get_transl_matrix(x,y,z=0):
    return  np.array([      [1.0, 0.0, 0.0, x], 
                            [0.0, 1.0, 0.0, y], 
                            [0.0, 0.0, 1.0, z], 
                            [0.0, 0.0, 0.0, 1.0]], np.float32)

def get_scale_matrix(sx,sy,sz):
    return  np.array([      [sx, 0.0, 0.0, 0.0], 
                            [0.0, sy, 0.0, 0.0], 
                            [0.0, 0.0, sz, 0.0], 
                            [0.0, 0.0, 0.0, 1.0]], np.float32)

