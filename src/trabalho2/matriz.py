import math
import glm
import numpy as np
def model_matrix(angle, translation, rotation, scale): ## angle deve ser em radianos
    t_x, t_y, t_z = translation
    r_x, r_y, r_z = rotation
    s_x, s_y, s_z = scale
    
    has_translation = not ((t_x)==0 and (t_y)==0 and (t_z)==0 )
    has_rotation = True
    has_scale = not ((s_x)==0 and (s_y)==0 and (s_z)==0 )
    
    # angle = math.radians(angle)
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade
    
    
    if (has_rotation and has_scale and has_translation):
        matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z)) ## aplica escala
        matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z)) ## aplica rotacao
        matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))     ## aplica translação
    elif (has_rotation or has_translation):
            ## escala, faz rotação e move (no mesmo eixo)
            # print("## escala, faz rotação e move (no mesmo eixo)")
            matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))     ## aplica translação
            matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z)) ## aplica rotacao
            matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z)) ## aplica escala
        
    elif (has_translation):
            ## apenas move
            # print("## apenas move")
            matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))     ## aplica translação    
    matrix_transform = np.array(matrix_transform)
    return matrix_transform

def view(cameraPos, cameraFront, cameraUp):
    mat_view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp);
    mat_view = np.array(mat_view)
    return mat_view

def projection(fov, altura, largura,near=0.1,far=1000.0):
    # perspective parameters: fovy, aspect, near, far
    mat_projection = glm.perspective(glm.radians(fov), largura/altura, near, far)
    mat_projection = np.array(mat_projection)    
    return mat_projection
    


def compose_rotacoes(rotacoes):
    """
    Recebe uma lista de tuplas no formato [(vetor3d, angulo), ...]
    Retorna o eixo de rotação e ângulo que representa a composição de todas as rotações.
    """
    rot_final = glm.mat4(1.0)
    
    for eixo, angulo in rotacoes:
        if angulo==0:
            break
        angulo_rad = math.radians(angulo)
        eixo_normalizado = glm.normalize(glm.vec3(*eixo))
        rot = glm.rotate(glm.mat4(1.0), angulo_rad, eixo_normalizado)
        rot_final = rot * rot_final
        
    
    rot3 = glm.mat3(rot_final)
    angulo_rad = np.arccos((np.trace(np.array(rot3)) - 1) / 2)
    
    if np.isclose(angulo_rad, 0):
        return np.array([1.0, 0.0, 0.0]), 0.0

    rx = rot3[2][1] - rot3[1][2]
    ry = rot3[0][2] - rot3[2][0]
    rz = rot3[1][0] - rot3[0][1]
    axis = np.array([rx, ry, rz])
    axis = axis / np.linalg.norm(axis)
    
    return axis, angulo_rad