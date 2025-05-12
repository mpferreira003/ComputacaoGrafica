import glfw
from OpenGL.GL import *
import numpy as np
import glm
import math
import random
from numpy import random
from PIL import Image

from shaders.shader import Shader
import loader
import camera
from model import Model

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
verticeInicial_estabulo, quantosVertices_estabulo = loader.load_obj_and_texture('objects/estabulo/estabulo.obj', 
                                                                            ['objects/estabulo/textures/002_diffuse.png'],
                                                                            vertices_list,
                                                                            textures_coord_list,
                                                                            find_textures=True)




verticeInicial_pig, qtd_vertices_pig = loader.load_obj_and_texture('objects/pig/pig.obj', 
                                                                            None,
                                                                            vertices_list,
                                                                            textures_coord_list,
                                                                            find_textures=True)

verticeInicial_feno, qtd_vertices_feno = loader.load_obj_and_texture('objects/feno/feno.obj', 
                                                                            None,
                                                                            vertices_list,
                                                                            textures_coord_list,
                                                                            find_textures=True)


                                                                        
# verticeInicial_horse, qtd_vertices_horse = loader.load_obj_and_texture('objects/horse/horse.obj', 
#                                                                             None,
#                                                                             vertices_list,
#                                                                             textures_coord_list,
#                                                                             find_textures=True)

verticeInicial_caixa, qtd_vertices_caixa = loader.load_obj_and_texture('objects/caixa/caixa.obj', 
                                                                            [
                                                                                'objects/caixa/textures/grama.jpg',
                                                                                'objects/caixa/textures/interno.jpg',
                                                                                'objects/caixa/textures/ceu.jpg'
                                                                            ],
                                                                            vertices_list,
                                                                            textures_coord_list,
                                                                            find_textures=False)


verticeInicial_ovelha, qtd_vertices_ovelha = loader.load_obj_and_texture('objects/ovelha/ovelha.obj', 
                                                                            None,
                                                                            vertices_list,
                                                                            textures_coord_list,
                                                                            find_textures=True)

verticeInicial_moinho, qtd_vertices_moinho = loader.load_obj_and_texture('objects/moinho/moinho.obj', 
                                                                            [],
                                                                            vertices_list,
                                                                            textures_coord_list,
                                                                            find_textures=False)

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

cam = camera.Camera(window,altura,largura,
                    cameraPos= glm.vec3(0.68,     0.30,    -1.10 ),
                    cameraFront= glm.vec3(0.97,    0.096,    -0.19 ),
                    cameraUp= glm.vec3(0,            1,            0 ),
                    yaw=-15.65,pitch=3.75,fov=45.0,main_speed=20)


## ------------ exibindo janela
glfw.show_window(window)



## Loop principal
glEnable(GL_DEPTH_TEST) ### importante para 3D
polygonal_mode = False 


estabulo = Model(verticeInicial_estabulo, 
                    quantosVertices_estabulo,
                    0,
                    pos=np.array([0,0,0]),
                    scale=np.ones(3)/5,
                    rotation=[(np.array([1,0,0]),0)],
                    )
    

porco = Model(verticeInicial_pig,qtd_vertices_pig,1,
              pos=np.array([-3.8,4,0]),
              scale=np.ones(3)/2,
              rotation=[(np.array([1,0,0]),90),
                        (np.array([0,0,1]),90)]
            )


fenos = []

altura_do_chao = 0.02
for x_add in range(3):
    x = 0.2+x_add*0.125*1.2
    feno = Model(verticeInicial_feno,qtd_vertices_feno,2,
                pos=np.array([1.8,x,altura_do_chao]),
                scale=np.ones(3),
                normal_scale=1/400,
                rotation=[(np.array([1,0,0]),90)]
                
                )
    fenos.append(feno)
for x_add in range(2):
    x = 0.2+0.125*1.2*(x_add+1) - 0.125*1.2/2
    feno = Model(verticeInicial_feno,qtd_vertices_feno,2,
                pos=np.array([1.8,x,altura_do_chao+0.125*1.2]),
                scale=np.ones(3),
                normal_scale=1/400,
                rotation=[(np.array([1,0,0]),90)]
                
                )
    fenos.append(feno)


# cavalo = Model(verticeInicial_horse,qtd_vertices_horse,3,
#               pos=np.array([0,0,0]),
#               scale=np.ones(3),
#             #   rotation=[(np.array([1,0,0]),90),
#             #             (np.array([0,0,1]),90)]
#             )


choes = []
for i in range(-10,10):
    for j in range(-10,10):
        x = i*2.0
        y = j*2.0
        chao = Model(verticeInicial_caixa,qtd_vertices_caixa,3,
                pos=np.array([x,0,y]),
                scale=np.array([1,0.0001,1]),
                normal_scale=1
                #   rotation=[(np.array([1,0,0]),90),
                #             (np.array([0,0,1]),90)]
                )
        choes.append(chao)

chao_interno = Model(verticeInicial_caixa,qtd_vertices_caixa,4,
                pos=np.array([1,1,-1]),
                scale=np.array([1,0.001,2]),
                normal_scale=1
                )

ceu = Model(verticeInicial_caixa,qtd_vertices_caixa,5,
                pos=np.array([0,0,0]),
                scale=np.array([1,-1,1]),
                normal_scale=120
                )

ovelhas = []
for i in range(10):
    x = random.uniform()
    y = random.uniform()
    
    x = (x-0.5)*30
    y = (y-0.5)*30
    
    x = min(abs(x),10) * x/abs(x)
    y = min(abs(y),10) * y/abs(y)
    
    
    angle = (random.uniform())*360
    ovelha = Model(verticeInicial_ovelha,qtd_vertices_ovelha,6,
                pos=np.array([x,0,y]),
                scale=np.ones(3)/2,
                rotation = [(np.array([0,1,0]),angle)]
                )
    ovelhas.append(ovelha)
    
moinho = Model(verticeInicial_moinho,qtd_vertices_moinho,0,
                pos=np.array([15,0,15]),
                scale=np.ones(3),
                normal_scale=1/20
                )


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
    
    
    
    
    ## Draw dos modelos:
    estabulo.draw(program)
    porco.draw(program)
    for feno in fenos:
        feno.draw(program)
    # cavalo.draw(program)
    for chao in choes:
        chao.draw(program)
    ceu.draw(program)
    for ovelha in ovelhas:
        ovelha.draw(program)
    moinho.draw(program)
    chao_interno.draw(program)
    
    
    mat_view = cam.view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)
    
    mat_projection = cam.projection()
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    
    
    glfw.swap_buffers(window)

glfw.terminate()