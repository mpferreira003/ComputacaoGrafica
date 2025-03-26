import numpy as np
import math
def get_rot_matrix(angle,pivot='z'):
    c = math.cos(angle)
    s = math.sin(angle)
    
    if pivot=='z':
        return  np.array([      [c,   -s,  0.0, 0.0], 
                                [s,    c,  0.0, 0.0], 
                                [0.0, 0.0, 1.0, 0.0], 
                                [0.0, 0.0, 0.0, 1.0]], np.float32)
    else:
        raise ValueError("Not implemented yet! :(")

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