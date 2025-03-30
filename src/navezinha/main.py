import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm
import shaders
import builder
import src.trabalho1.vertice as vertice
import posmath
import time

glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE);

# Cria a janela
window = builder.create_window(600,600)
glfw.make_context_current(window)


# Request a program and shader slots from GPU
program  = glCreateProgram()
shaders.compile_shaders(program)
builder.build_program(program)


buffer_VBO = builder.request_buffer_slot()



# Upload data
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW) ## lembre que é global
glBindBuffer(GL_ARRAY_BUFFER, buffer_VBO) ## vincula a gpu


# Bind the position attribute
# --------------------------------------
stride = vertices.strides[0]
offset = ctypes.c_void_p(0)


loc = glGetAttribLocation(program, shaders.SN_POSITION_NAME)
glEnableVertexAttribArray(loc)

glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

loc_color = glGetUniformLocation(program, shaders.SN_COLOR)
R = 0.7
G = 0.0
B = 0.2

#### O código dessa célula não está sendo usado.

def key_event(window,key,scancode,action,mods,scale=-1):
    global t_x, t_y
    print("key: ",key)
    if key == 87: t_y += 0.01*scale #cima
    if key == 68: t_x += 0.01*scale #direita
    if key == 83: t_y -= 0.01*scale #baixo
    if key == 65: t_x -= 0.01*scale #esquerda


    
glfw.set_key_callback(window,key_event)

glfw.show_window(window)

import math

angulo = 0
t_x = 0
t_y = 0


def multiplica_matriz(a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c

glEnable(GL_BLEND);
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);


def pipeline(angle, t_x, t_y):
    """
    Retorna a matriz de transformação combinada.
    
    Parâmetros:
        angle: Ângulo de rotação (em radianos).
        t_x: Translação no eixo X.
        t_y: Translação no eixo Y.
    
    Retorno:
        Matriz de transformação 4x4.
    """
    # 1. Translação para a origem
    pos = posmath.get_transl_matrix(-t_x, -t_y)
    
    # 2. Rotação em torno da origem
    rotation = posmath.get_rot_matrix(angle)
    
    # 3. Translação de volta para a posição original
    # pos_anti = posmath.get_transl_matrix(t_x, t_y)
    
    # Combina as matrizes: pos_anti @ rotation @ pos
    # return pos_anti @ rotation @ pos
    return pos @ rotation
while not glfw.window_should_close(window):
    
    glClear(GL_COLOR_BUFFER_BIT) 
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    angulo -= 0.01
    matriz_transformacao = pipeline(angulo,t_x,t_y) ## matriz que aplica a transformação nos vértices    
    
    # pede a localizacao da variavel mat_transformation no shader
    loc = glGetUniformLocation(program, shaders.SN_MAT_TRANSFORMATION)
    
    # set mat_transformation com a mat_rotation
    glUniformMatrix4fv(loc, 1, GL_TRUE, matriz_transformacao)
    
    #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE) ## ative esse comando para enxergar os triângulos
    
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4) ## escreve os pontos
    glUniform4f(loc_color, R, G, B, 1.0) ### modificando a cor do objeto!
    
    glfw.swap_buffers(window)
    glfw.poll_events() 
    # time.sleep(0.1)
glfw.terminate()