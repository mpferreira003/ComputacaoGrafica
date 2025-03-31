import glfw
from OpenGL.GL import *
import numpy as np
import shaders
import builder
import area
import math
import random
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


N_METEOROS = 10
METEORO_MIN_VERTICES = 5
METEORO_MAX_VERTICES = 20

N_ESTRELAS = 20
ESTRELAS_MIN_STEPS = 20

meteoros = []
for i in range(N_METEOROS):
    r1 = random.random()
    r2 = random.random()
    meteoros.append(actor.Meteoro(n_vertices = random.randint(METEORO_MIN_VERTICES,METEORO_MAX_VERTICES),
                                  radius_base=0.1*r1,
                                  radius_diff=0.025*r1,
                                  animate_angle_step=0.01*r2,
                                  animate_move_step=0.001*r2))
    
estrelas = []
for i in range(N_ESTRELAS):
    r1 = random.random()
    r2 = random.random()
    estrelas.append(actor.Star(n_vertices=5 if random.random()>0.5 else 6,
                               intern_radius=0.01*r1,
                               extern_radius=0.04*r1,
                               animation_max_steps= amx if (amx:=100*r2) > ESTRELAS_MIN_STEPS else ESTRELAS_MIN_STEPS))


actors = estrelas + meteoros
vertices = area.Area.get_world_vertices(actors)

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

loc_matriz = glGetUniformLocation(program, shaders.SN_MAT_TRANSFORMATION)
while not glfw.window_should_close(window):
    
    glClear(GL_COLOR_BUFFER_BIT) 
    glClearColor(0.0, 0.0, 0.0, 1.0)
    for meteoro in meteoros:
        meteoro.animate()
    
    for estrela in estrelas:
        estrela.animate()
        
    
    
    ## Chama o método draw_objects que desenha de fato todos os objetos
    area.Area.draw_objects(actors,loc_color,loc_matriz,just_triangles=True)
    
    
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()