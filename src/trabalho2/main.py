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

def centroid(init,qtd):
    global vertices_list
    vertices_filtered = []
    for i in range(init,init+qtd):
        vertices_filtered.append([float(a) for a in vertices_list[i]])
    return np.mean(vertices_filtered,axis=0)

## Carregando modelos

#region
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
centroid_pig = centroid(verticeInicial_pig, qtd_vertices_pig)


verticeInicial_feno, qtd_vertices_feno = loader.load_obj_and_texture('objects/feno/feno.obj', 
                                                                            None,
                                                                            vertices_list,
                                                                            textures_coord_list,
                                                                            find_textures=True)
centroid_feno = centroid(verticeInicial_feno, qtd_vertices_feno)

                                                                        

verticeInicial_caixa, qtd_vertices_caixa = loader.load_obj_and_texture('objects/caixa/caixa.obj', 
                                                                            [
                                                                                'objects/caixa/textures/grama.png',
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
centroid_ovelha = centroid(verticeInicial_ovelha, qtd_vertices_ovelha)


verticeInicial_moinho, qtd_vertices_moinho = loader.load_obj_and_texture('objects/moinho/moinho.obj', 
                                                                            [],
                                                                            vertices_list,
                                                                            textures_coord_list,
                                                                            find_textures=False)
centroid_moinho = centroid(verticeInicial_moinho, qtd_vertices_moinho)


verticeInicial_galinha, qtd_vertices_galinha = loader.load_obj_and_texture('objects/galinha/galinha.obj', 
                                                                            None,
                                                                            vertices_list,
                                                                            textures_coord_list,
                                                                            find_textures=True)
centroid_galinha = centroid(verticeInicial_galinha, qtd_vertices_galinha)


verticeInicial_grama_1, qtd_vertices_grama_1 = loader.load_obj_and_texture('objects/grama_1/grama.obj', 
                                                                            None,
                                                                            vertices_list,
                                                                            textures_coord_list,
                                                                            find_textures=True)
centroid_grama_1 = centroid(verticeInicial_grama_1, qtd_vertices_grama_1)

verticeInicial_grama_2, qtd_vertices_grama_2 = loader.load_obj_and_texture('objects/grama_2/grama.obj', 
                                                                            [],
                                                                            vertices_list,
                                                                            textures_coord_list,
                                                                            find_textures=False)
centroid_grama_2 = centroid(verticeInicial_grama_2, qtd_vertices_grama_2)
#endregion

## -------------------------------------------------

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



## Fazendo os objetos ------------------------------
#region
estabulo = Model(verticeInicial_estabulo, 
                    quantosVertices_estabulo,
                    0,
                    pos=np.array([0,0,0]),
                    scale=np.ones(3)/5,
                    rotation=[(np.array([1,0,0]),0)],
                    )
    

porco = Model(verticeInicial_pig,qtd_vertices_pig,1,
              pos=np.array([1.2,0,-2]),
              scale=np.ones(3)/2,
              centroid=centroid_pig,
              rotation=[(np.array([1,0,0]),90),
                        (np.array([0,0,1]),90)]
            )


fenos = []

altura_do_chao = 0.02
for x_add in range(3):
    x = x_add*0.15
    feno = Model(verticeInicial_feno,qtd_vertices_feno,2,
                pos=np.array([3.7,0.2,-27.78-x])/400,
                scale=np.ones(3),
                centroid=centroid_feno,
                normal_scale=1/400,
                rotation=[(np.array([1,0,0]),90)]
                
                )
    fenos.append(feno)
for x_add in range(2):
    x = x_add*0.15+0.15/2
    feno = Model(verticeInicial_feno,qtd_vertices_feno,2,
                pos=np.array([3.7,0.2+0.15,-27.78-x])/400,
                centroid=centroid_feno,
                scale=np.ones(3),
                normal_scale=1/400,
                rotation=[(np.array([1,0,0]),90)]
                
                )
    fenos.append(feno)


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
                pos=np.array([1,0.0,-2]),
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
                pos=np.array([x,-0.25,y]),
                centroid=centroid_ovelha,
                scale=np.ones(3)/2,
                rotation = [(np.array([0,1,0]),angle)]
                )
    ovelhas.append(ovelha)
    
moinho = Model(verticeInicial_moinho,qtd_vertices_moinho,0,
                pos=np.array([-2,-3.65,-1]),
                scale=np.ones(3),
                centroid=centroid_moinho,
                normal_scale=1/10
                )

galinha = Model(verticeInicial_galinha,qtd_vertices_galinha,7,
                pos=np.array([1,-0.1,-3]),
                centroid=centroid_galinha,
                scale=np.ones(3)/2,
                normal_scale=1
                )

gramas = []
n_gramas = 300
for i in range(n_gramas):
    tipo = 1 if random.uniform()>0.5 else 0
    textura_tipo = 1 if random.uniform()>0.8 else 0
    
    vi = verticeInicial_grama_1 if tipo==1 else verticeInicial_grama_2
    qtd = qtd_vertices_grama_2 if tipo==1 else qtd_vertices_grama_2
    textura_id = 7 if tipo==1 else 8
    centroid = centroid_grama_1 if tipo==1 else centroid_grama_2
    
    loop = True
    while loop:
        x = (random.rand()-0.5)*30
        y = (random.rand()-0.5)*30
        if (abs(x)>7 and abs(y)>7):
            loop=False
    grama = Model(vi,qtd,textura_id,
            pos=np.array([x,0,y]),
            scale=np.ones(3),
            centroid=centroid,
            normal_scale=1
            )
    gramas.append(grama)
#endregion










## main loop ------------------------------------------------------------------------------------------------

## Configuração do seletor 
cam.add_event_handler(glfw.KEY_1,1)
cam.add_event_handler(glfw.KEY_2,2)
cam.add_event_handler(glfw.KEY_3,3)
cam.add_event_handler(glfw.KEY_4,4)
cam.add_event_handler(glfw.KEY_5,5)
cam.add_event_handler(glfw.KEY_6,6)
models_by_keyoutput = {
    1:[porco],
    2:fenos,
    3:ovelhas,
    4:[moinho],
    5:[galinha],
    6:gramas
}

cam.add_event_handler(glfw.KEY_U,10)
cam.add_event_handler(glfw.KEY_O,20)
cam.add_event_handler(glfw.KEY_I,30)
cam.add_event_handler(glfw.KEY_K,40)
cam.add_event_handler(glfw.KEY_J,50)
cam.add_event_handler(glfw.KEY_L,60)
events_by_keyoutput = {
    10:lambda model: model.modify(add_scale=+np.array([0.01,0.01,0.01])),
    20:lambda model: model.modify(add_scale=-np.array([0.01,0.01,0.01])),
    30:lambda model: model.modify(add_pos=np.array([0.0,0.0,0.01])),
    40:lambda model: model.modify(add_pos=-np.array([0.0,0.0,0.01])),
    50:lambda model: model.modify(add_rot=np.array([0.0,0.0,0.1]),angle=math.radians(1)),
    60:lambda model: model.modify(add_rot=-np.array([0.0,0.0,0.1]),angle=math.radians(1)),
}


selected = []
lastFrame = glfw.get_time()
while not glfw.window_should_close(window):
    
    currentFrame = glfw.get_time()
    deltaTime = currentFrame - lastFrame
    lastFrame = currentFrame
    cam.atualize_speed(deltaTime)
    
        
    
    glfw.poll_events() 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    if cam.polygonal_mode:
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    
    
    
    ## Draw dos modelos:
    estabulo.draw(program)
    porco.draw(program)
    for feno in fenos:
        feno.draw(program)
        
    for chao in choes:
        chao.draw(program)
    ceu.draw(program)
    for i,ovelha in enumerate(ovelhas):
        ovelha.draw(program)
    moinho.draw(program)
    chao_interno.draw(program)
    galinha.draw(program)
    
    for grama in gramas:
        grama.draw(program)
        
    
    ## Aplica modificações do teclado:
    if cam.output_value in models_by_keyoutput.keys():
        selected = models_by_keyoutput[cam.output_value]
    
    if cam.output_value in events_by_keyoutput.keys():
        for model in selected:
            events_by_keyoutput[cam.output_value](model)
    
    
    mat_view = cam.view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)
    
    mat_projection = cam.projection()
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    
    
    glfw.swap_buffers(window)

glfw.terminate()