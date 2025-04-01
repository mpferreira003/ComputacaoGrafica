import glfw
from OpenGL.GL import *
import numpy as np
import utils.shaders as shaders
import utils.builder as builder
import area
import actor
import random

## Iniciando o programa
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
## Parâmetros

TRIANGLE_SHOW_KEY = 'p'
QUIT_PROGRAM_KEY = 'q'

N_METEOROS = 20
METEORO_MIN_VERTICES = 5
METEORO_MAX_VERTICES = 20
METEORO_ANIMATE_KEY = 'm'

N_ESTRELAS = 40
ESTRELAS_MIN_STEPS = 20
ESTRELA_ANIMATE_KEY = 'n'

SHOT_ANIMATE_KEY = 32 ## espaço

SHIELD_ANIMATE_KEY = 'e'
SHIP_RIGHT_KEY = 'd'
SHIP_LEFT_KEY = 'a'



## Atores da cena
can_animate_meteoros = False
meteoros = []
for i in range(N_METEOROS):
    r1 = random.random()
    r2 = random.random()
    meteoros.append(actor.Meteoro(n_vertices = random.randint(METEORO_MIN_VERTICES,METEORO_MAX_VERTICES),
                                  radius_base=0.1*r1,
                                  radius_diff=0.025*r1,
                                  animate_angle_step=0.01*r2,
                                  animate_move_step=0.001*r2))
    
can_animate_estrelas = False
estrelas = []
for i in range(N_ESTRELAS):
    r1 = random.random()
    r2 = random.random()
    estrelas.append(actor.Star(n_vertices=random.randint(5,7),
                               intern_radius=0.01*r1,
                               extern_radius=0.04*r1,
                               animation_max_steps= amx if (amx:=100*r2) > ESTRELAS_MIN_STEPS else ESTRELAS_MIN_STEPS))


can_animate_shoots = False
shots = []
for i in range(1):
    shots.append(actor.Shot())

can_animate_shield = False
shield = actor.Shield()


ship_direction = 0
ship = actor.Ship()

## Objetos principais de atores e vértices
actors = estrelas + meteoros + shots + [ship] + [shield]
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

## Vertex
loc = glGetAttribLocation(program, shaders.SN_POSITION_NAME)
glEnableVertexAttribArray(loc)
glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)
loc_color = glGetUniformLocation(program, shaders.SN_COLOR)

glEnable(GL_BLEND);
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
loc_matriz = glGetUniformLocation(program, shaders.SN_MAT_TRANSFORMATION)

## Eventos de teclado
was_pressed = lambda char,key: ord(char)==((97-65)+key) ## verificador pra quando a tecla é pressionada
aux_pressed_inverter = False ## auxilia o processo de detectar quando vc fica pressionando por mais tempo (sistema de action usado na key_event)
show_triangles = False
def key_event(window,key,scancode,action,mods,scale=-1):
    global can_animate_meteoros,can_animate_estrelas,can_animate_shoots,can_animate_shield
    global aux_pressed_inverter, program_running, show_triangles
    global ship_direction
    
    ## Controle dos meteoros
    if was_pressed(METEORO_ANIMATE_KEY,key):
        if action == 0: ## Se ele pressionou por um tempo médio
            aux_pressed_inverter = True
        elif action == 1:
            can_animate_meteoros = not can_animate_meteoros
            aux_pressed_inverter = False
    
    ## Controle das estrelas
    if was_pressed(ESTRELA_ANIMATE_KEY,key):
        if action == 0: ## Se ele pressionou por um tempo médio
            aux_pressed_inverter = True
        elif action == 1:
            can_animate_estrelas = not can_animate_estrelas
            aux_pressed_inverter = False
    
    ## Controle dos tiros
    if key == SHOT_ANIMATE_KEY:
        if action == 0: ## Se ele pressionou por um tempo médio
            aux_pressed_inverter = True
        elif action == 1:
            can_animate_shoots = not can_animate_shoots
            aux_pressed_inverter = False
    
    ## Controle do escudo
    if was_pressed(SHIELD_ANIMATE_KEY,key):
        if action == 0: ## Se ele pressionou por um tempo médio
            aux_pressed_inverter = True
        elif action == 1:
            can_animate_shield = not can_animate_shield
            aux_pressed_inverter = False
    
    
    # Controle da nave
    if was_pressed(SHIP_RIGHT_KEY,key):
        if action == 0: ## Se ele pressionou por um tempo médio
            ship_direction = 0 
        elif action == 1:
            ship_direction = 1
    if was_pressed(SHIP_LEFT_KEY,key):
        if action == 0: ## Se ele pressionou por um tempo médio
            ship_direction = 0
        elif action == 1:
            ship_direction = -1
    
    ## Controle do programa
    if was_pressed(QUIT_PROGRAM_KEY,key):
        program_running = False
    
    ## Controle dos triângulos
    if was_pressed(TRIANGLE_SHOW_KEY,key):
        if action == 0: ## Se ele pressionou por um tempo médio
            aux_pressed_inverter = True
        elif action == 1:
            show_triangles = not show_triangles
            aux_pressed_inverter = False
glfw.set_key_callback(window,key_event)
glfw.show_window(window)



## Loop principal
first_animation = True
program_running = True
while (not glfw.window_should_close(window)) and program_running:
    ## Reseta a tela
    glClear(GL_COLOR_BUFFER_BIT) 
    glClearColor(0.0, 0.0, 0.0, 1.0)
    
    ## Animação dos meteoros
    if can_animate_meteoros or first_animation:
        for meteoro in meteoros:
            meteoro.animate()
    
    ## Animação das estrelas
    if can_animate_estrelas or first_animation:
        for estrela in estrelas:
            estrela.animate()
    
    ## Animação dos tiros
    if can_animate_shoots:
        for shot in shots:
            shot.visible=True
            shot.animate(ship.current_pos())
    else:
        for shot in shots:
            shot.visible=False
    
    ## Animação do escudo
    if can_animate_shield:
        shield.visible=True
        shield.animate(ship.current_pos())
    else:
        shield.visible=False
    
    ## Animação da nave
    ship.animate(ship_direction)
    
    
    ## Chama o método draw_objects que desenha de fato todos os objetos
    area.Area.draw_objects(actors,loc_color,loc_matriz,just_triangles=show_triangles)
    
    first_animation = False
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()