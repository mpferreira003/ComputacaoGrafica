import glfw
from OpenGL.GL import *
import numpy as np
import shaders
import builder
import vertice
import area
import math
import actor


glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE);

# Cria a janela
window = builder.create_window(600,600)
glfw.make_context_current(window)

# Request a program and shader slots from GPU
program  = glCreateProgram()
shaders.compile_shaders(program)
builder.build_program(program)


## ----------------------------------------------------------------------------------------
## Atores da cena

# Fazendo os objetos
# nave = [
#     (+0.00, +0.00),
#     (+0.20, +0.00),
#     (+0.00, +0.20),
#     (+0.00, -0.20),
# ]

meteoro = actor.Star(10)

draw_schema,vertices = area.Area.get_draw_schema([meteoro])

## ----------------------------------------------------------------------------------------


# Upload data
buffer_VBO = builder.request_buffer_slot()
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


def key_event(window,key,scancode,action,mods,scale=-1):
    global t_x, t_y
    print("key: ",key)
    if key == 87: t_y += 0.01*scale #cima
    if key == 68: t_x += 0.01*scale #direita
    if key == 83: t_y -= 0.01*scale #baixo
    if key == 65: t_x -= 0.01*scale #esquerda

glfw.set_key_callback(window,key_event)

glfw.show_window(window)

def multiplica_matriz(a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c

glEnable(GL_BLEND);
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);


while not glfw.window_should_close(window):
    
    glClear(GL_COLOR_BUFFER_BIT) 
    glClearColor(0.0, 0.0, 0.0, 1.0)
    
    meteoro.modify(0.0, 0.0, 0.001)
    
    # Chama o método draw da instância e obtém a matriz de transformação
    matriz_transformacao = meteoro.draw()

    loc = glGetUniformLocation(program, shaders.SN_MAT_TRANSFORMATION)
    glUniformMatrix4fv(loc, 1, GL_TRUE, matriz_transformacao)
    
    ## Chama o método draw_objects que desenha de fato todos os objetos baseado no esquema
    area.Area.draw_objects(draw_schema,loc_color)
    
    
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()