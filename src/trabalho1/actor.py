import numpy as np
from shaders import SN_POSITION_NAME
import glfw
from OpenGL.GL import *

def create_vertice_array(n_points,dim=2):
    return np.zeros(n_points, [(SN_POSITION_NAME, np.float32, dim)])


class Actor():
    def __init__(self):
        pass
    def upload_data():
        ## tentar passar o buffer_VBO como parâmetro e, caso não passar, criar automaticamente
        buffer_VBO = builder.request_buffer_slot() 
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW) ## lembre que é global
        glBindBuffer(GL_ARRAY_BUFFER, buffer_VBO) ## vincula a gpu
    
    def enable_attrib():
        glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(loc)