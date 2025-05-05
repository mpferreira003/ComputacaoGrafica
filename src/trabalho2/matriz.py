import math
import glm
import numpy as np
def model_matrix(angle, translation, rotation, scale):
    t_x, t_y, t_z = translation
    r_x, r_y, r_z = rotation
    s_x, s_y, s_z = scale
    angle = math.radians(angle)
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade
    
    # aplicando translacao (terceira operação a ser executada)
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))    
    
    # aplicando rotacao (segunda operação a ser executada)
    if angle!=0:
        matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z))
    
    # aplicando escala (primeira operação a ser executada)
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))
    matrix_transform = np.array(matrix_transform)
    return matrix_transform

def view(cameraPos, cameraFront, cameraUp):
    mat_view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp);
    mat_view = np.array(mat_view)
    return mat_view

def projection(fov, altura, largura):
    # perspective parameters: fovy, aspect, near, far
    mat_projection = glm.perspective(glm.radians(fov), largura/altura, 0.1, 100.0)
    mat_projection = np.array(mat_projection)    
    return mat_projection