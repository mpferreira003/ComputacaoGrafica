import glfw
from OpenGL.GL import *
import numpy as np
import glm
import math
from numpy import random
from PIL import Image

from shaders.shader import Shader
import loader
import camera

## Iniciando ----------------------------
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

altura = 700
largura = 700

window = glfw.create_window(largura, altura, "Programa", None, None)

if (window == None):
    print("Failed to create GLFW window")
    glfwTerminate()
    
glfw.make_context_current(window)


## Construindo os shaders --------------
ourShader = Shader("shaders/vertex_shader.vs", "shaders/fragment_shader.fs")
ourShader.use()

program = ourShader.getProgram()



## Carregando os modelos
glEnable(GL_TEXTURE_2D)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable( GL_BLEND )
glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
glEnable(GL_LINE_SMOOTH)

vertices_list = []    
textures_coord_list = []

## Desenhando ----------
# carrega caixa (modelo e texturas)
verticeInicial_caixa, quantosVertices_caixa = loader.load_obj_and_texture('objects/caixa/caixa.obj', 
                                                                          ['objects/caixa/caixa.jpg', 
                                                                           'objects/caixa/tijolos.jpg', 
                                                                           'objects/caixa/matrix.jpg'],
                                                                           vertices_list,
                                                                           textures_coord_list)



## ----------------------------------------------------------------------------------------------------------------

## Requisitando buffers
buffer_VBO = glGenBuffers(2)

## Enviando dados para a GPU
vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
vertices['position'] = vertices_list

# Upload data
glBindBuffer(GL_ARRAY_BUFFER, buffer_VBO[0])
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
stride = vertices.strides[0]
offset = ctypes.c_void_p(0)
loc_vertices = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc_vertices)
glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)




## Enviando textura para a GPU
textures = np.zeros(len(textures_coord_list), [("position", np.float32, 2)]) # duas coordenadas
textures['position'] = textures_coord_list

# Upload data
glBindBuffer(GL_ARRAY_BUFFER, buffer_VBO[1])
glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
stride = textures.strides[0]
offset = ctypes.c_void_p(0)
loc_texture_coord = glGetAttribLocation(program, "texture_coord")

glEnableVertexAttribArray(loc_texture_coord)
glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)

## ----------------------------------------------------------------------------------------------------------------

cam = camera.Camera(window,altura,largura)


## ------------ exibindo janela
glfw.show_window(window)



## Loop principal
glEnable(GL_DEPTH_TEST) ### importante para 3D
polygonal_mode = False 

range_caixas = (-5,5)
textures = np.random.randint(0,3,len(range(*range_caixas)))

from model import Model
import matriz

caixas = []
for i in range(5):
    caixas.append(Model(verticeInicial_caixa, quantosVertices_caixa,i%3))


lastFrame = glfw.get_time()
while not glfw.window_should_close(window):
    
    currentFrame = glfw.get_time()
    deltaTime = currentFrame - lastFrame
    lastFrame = currentFrame
    cam.atualize_speed(deltaTime)

    glfw.poll_events() 
       
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    if polygonal_mode:
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    for caixa in caixas:
        caixa.draw(program)
    
    mat_view = cam.view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)
    
    mat_projection = cam.projection()
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    
    
    glfw.swap_buffers(window)

glfw.terminate()