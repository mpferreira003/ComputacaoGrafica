import math
import glm
import numpy as np
def model_matrix(angle, translation, rotation, scale, centroid=(0.0, 0.0, 0.0)):
    t_x, t_y, t_z = translation
    r_x, r_y, r_z = rotation
    s_x, s_y, s_z = scale
    c_x, c_y, c_z = centroid  # centro no espaço do mundo
    
    matrix = glm.mat4(1.0)

    # 1. Translada para o mundo (posição final do objeto)
    matrix = glm.translate(matrix, glm.vec3(t_x, t_y, t_z))

    # 2. Translada para o centro do objeto
    matrix = glm.translate(matrix, glm.vec3(c_x, c_y, c_z))
    
    # 3. Aplica escala
    matrix = glm.scale(matrix, glm.vec3(s_x, s_y, s_z))
    
    # 4. Volta do centro
    matrix = glm.translate(matrix, glm.vec3(-c_x, -c_y, -c_z))
    
    # 5. Aplica rotação se quiser (em torno do centro)
    rotation_axis = glm.vec3(r_x, r_y, r_z)
    if angle != 0.0 and glm.length(rotation_axis) > 0.0:
        rotation_axis = glm.normalize(rotation_axis)
        matrix = glm.rotate(matrix, angle, rotation_axis)

    return np.array(matrix)

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