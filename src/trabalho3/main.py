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
import time
from model import Model

# Variáveis de controle de iluminação
class Light:
    def __init__(self,ambient=None,diffuse=None,specular=None,shininess=None,position=None,color=None,enabled=None):
        self.ambient = ambient or 1.0
        self.diffuse = diffuse or 0.8
        self.specular = specular or 0.5
        self.shininess = shininess or 32.0
        self.position = position or glm.vec3(0.0, 0.0, 0.0)
        self.color = color or glm.vec3(1.0, 1.0, 1.0)
        self.enabled = enabled or True

moinho_light = Light()
moinho_light.color = glm.vec3(50.0, 40.0, 10.0)  
moinho_light.position = glm.vec3(0, 0, 0)  
moinho_light.ambient = 0.5  
moinho_light.diffuse = 0.2
moinho_light.specular = 0.2
moinho_light.enabled = True

# Configuração da iluminação
ambientLight = glm.vec3(0.3, 0.3, 0.3)  # Luz ambiente global 
ambientIntensity = 0.3  # Intensidade da luz ambiente 

# Funções de callback para teclado
def key_callback(window, key, scancode, action, mods):
    # Deixando a câmera lidar com os eventos de teclado
    cam.key_event(window, key, scancode, action, mods)

## Iniciando ----------------------------
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

altura = 700
largura = 700

window = glfw.create_window(largura, altura, "Programa", None, None)

if (window == None):
    print("Failed to create GLFW window")
    glfw.terminate()
    
glfw.make_context_current(window)

# Inicializando a câmera
cam = camera.Camera(window, altura, largura)

## Construindo os shaders --------------
ourShader = Shader("shaders/vertex_shader.vs", "shaders/fragment_shader.fs")
ourShader.use()

program = ourShader.getProgram()

# Mapeando eventos para os modelos
models_by_keyoutput = {
    "moinho_light": [moinho_light]
}

events_by_keyoutput = {
    "ambient_down": lambda model: setattr(model, "ambient", max(0.0, model.ambient - 0.1)),
    "ambient_up": lambda model: setattr(model, "ambient", min(1.0, model.ambient + 0.1)),
    "diffuse_down": lambda model: setattr(model, "diffuse", max(0.0, model.diffuse - 0.1)),
    "diffuse_up": lambda model: setattr(model, "diffuse", min(1.0, model.diffuse + 0.1)),
    "specular_down": lambda model: setattr(model, "specular", max(0.0, model.specular - 0.1)),
    "specular_up": lambda model: setattr(model, "specular", min(1.0, model.specular + 0.1)),
    "shininess_down": lambda model: setattr(model, "shininess", max(1.0, model.shininess - 1.0)),
    "shininess_up": lambda model: setattr(model, "shininess", min(128.0, model.shininess + 1.0))
}


# Configuração inicial dos shaders
ourShader.use()
ourShader.setFloat("ka", 0.5)  # Coeficiente ambiente do material
ourShader.setFloat("kd", 0.8)  # Coeficiente difuso do material
ourShader.setFloat("ks", 0.5)  # Coeficiente especular do material
ourShader.setFloat("ns", 32.0)  # Expoente especular

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


verticeInicial_lampada, qtd_vertices_lampada = loader.load_obj_and_texture('objects/lampada/lampada.obj', 
                                                                            None,
                                                                            vertices_list,
                                                                            textures_coord_list,
                                                                            find_textures=True)
centroid_lampada = centroid(verticeInicial_lampada, qtd_vertices_lampada)


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

# Converter listas para arrays numpy
vertices = np.array(vertices_list, dtype=np.float32)
textures = np.array(textures_coord_list, dtype=np.float32)

# Calcular normais para cada face
normals = np.zeros((len(vertices_list), 3), dtype=np.float32)
for i in range(0, len(vertices_list), 3):
    v1 = vertices[i]
    v2 = vertices[i+1]
    v3 = vertices[i+2]
    
    # Calcular vetores da face
    edge1 = v2 - v1
    edge2 = v3 - v1
    
    # Calcular normal da face
    normal = np.cross(edge1, edge2)
    normal = normal / np.linalg.norm(normal)  # Normalizar
    
    # Atribuir a normal a cada vértice da face
    normals[i] = normal
    normals[i+1] = normal
    normals[i+2] = normal

# Configurar VAO e VBOs
VAO = glGenVertexArrays(1)
VBO_vertices = glGenBuffers(1)
VBO_textures = glGenBuffers(1)
VBO_normals = glGenBuffers(1)

glBindVertexArray(VAO)

# Configurar buffer de vértices
glBindBuffer(GL_ARRAY_BUFFER, VBO_vertices)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(0)

# Configurar buffer de texturas
glBindBuffer(GL_ARRAY_BUFFER, VBO_textures)
glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(1)

# Configurar buffer de normais
glBindBuffer(GL_ARRAY_BUFFER, VBO_normals)
glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(2)

# Desvincular buffers
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

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
                    is_outdoor=True,
                    ka=0.3, kd=0.8, ks=0.3, ns=32.0  # Material para o estábulo
                    )

porco = Model(verticeInicial_pig, qtd_vertices_pig, 1,
              pos=np.array([1.2,0,-2]),
              scale=np.ones(3)/2,
              centroid=centroid_pig,
              rotation=[(np.array([1,0,0]),90),
                       (np.array([0,0,1]),90)],
              is_outdoor=False,
              ka=0.4, kd=0.9, ks=0.6, ns=64.0  # Material para o porco
              )

fenos = []

altura_do_chao = 0.02
for x_add in range(3):
    x = x_add*0.15
    feno = Model(verticeInicial_feno, qtd_vertices_feno, 2,
                pos=np.array([3.7,0.2,-27.78-x])/400,
                scale=np.ones(3),
                centroid=centroid_feno,
                normal_scale=1/400,
                rotation=[(np.array([1,0,0]),90)],
                is_outdoor=False,
                ka=0.5, kd=0.7, ks=0.2, ns=16.0  # Material para o feno
                )
    fenos.append(feno)
for x_add in range(2):
    x = x_add*0.15+0.15/2
    feno = Model(verticeInicial_feno, qtd_vertices_feno, 2,
                pos=np.array([3.7,0.2+0.15,-27.78-x])/400,
                centroid=centroid_feno,
                scale=np.ones(3),
                normal_scale=1/400,
                rotation=[(np.array([1,0,0]),90)],
                is_outdoor=False,
                ka=0.5, kd=0.7, ks=0.2, ns=16.0  # Material para o feno (segunda camada)
                )
    fenos.append(feno)


choes = []
for i in range(-10,10):
    for j in range(-10,10):
        x = i*2.0
        y = j*2.0
        chao = Model(verticeInicial_caixa, qtd_vertices_caixa, 3,
                pos=np.array([x,0,y]),
                scale=np.array([1,0.0001,1]),
                normal_scale=1,
                is_outdoor=True,
                ka=0.3, kd=0.6, ks=0.1, ns=8.0  # Material para o chão
                )
        choes.append(chao)

chao_interno = Model(verticeInicial_caixa, qtd_vertices_caixa, 4,
                pos=np.array([1,0.0,-2]),
                scale=np.array([1,0.001,2]),
                normal_scale=1,
                is_outdoor=False,
                ka=0.4, kd=0.7, ks=0.3, ns=16.0  # Material para o chão interno
                )

ceu = Model(verticeInicial_caixa, qtd_vertices_caixa, 5,
                pos=np.array([0,0,0]),
                scale=np.array([1,-1,1]),
                normal_scale=120,
                is_outdoor=True,
                ka=0.8, kd=0.2, ks=0.1, ns=4.0  # Material para o céu
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
    ovelha = Model(verticeInicial_ovelha, qtd_vertices_ovelha, 6,
                pos=np.array([x,-0.25,y]),
                centroid=centroid_ovelha,
                scale=np.ones(3)/2,
                rotation = [(np.array([0,1,0]),angle)],
                is_outdoor=True,
                ka=0.5, kd=0.9, ks=0.7, ns=128.0  # Material para a ovelha (mais brilhante)
                )
    ovelhas.append(ovelha)

moinho = Model(verticeInicial_moinho, qtd_vertices_moinho, 0,
                pos=np.array([-2,-3.65,-1]),
                scale=np.ones(3),
                centroid=centroid_moinho,
                normal_scale=1/10,
                is_outdoor=True,
                ka=0.4, kd=0.7, ks=0.5, ns=64.0  # Material para o moinho
                )

galinha = Model(verticeInicial_galinha, qtd_vertices_galinha, 7,
                pos=np.array([1,-0.1,-3]),
                centroid=centroid_galinha,
                scale=np.ones(3)/2,
                normal_scale=1,
                is_outdoor=False,
                ka=0.6, kd=0.8, ks=0.9, ns=96.0  # Material para a galinha
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
    grama = Model(vi, qtd, textura_id,
            pos=np.array([x,0,y]),
            scale=np.ones(3),
            centroid=centroid,
            normal_scale=1,
            is_outdoor=True,
            ka=0.4, kd=0.6, ks=0.1, ns=8.0  # Material para as gramas
            )
    gramas.append(grama)


lampadas = [
    (
        Model(verticeInicial_lampada, qtd_vertices_lampada, 9,
                pos=np.array([3.7,1.0,-27.78-7.525])/500,
                scale=np.ones(3),
                centroid=centroid_feno,
                normal_scale=1/400,
                is_outdoor=False,
                ka=0.8, kd=0.9, ks=1.0, ns=128.0  # Material para a lâmpada 1 (mais brilhante)
                ),
        Light(color=glm.vec3(70.0, 0.0, 70.0), position=glm.vec3(0, 0, 0),
              ambient=0.1, diffuse=0.4, specular=0.3, enabled=True)
    ),
    (
        Model(verticeInicial_lampada, qtd_vertices_lampada, 9,
                    pos=np.array([3.7,1.0,-27.78-7.525-2.5])/500,
                    scale=np.ones(3),
                    centroid=centroid_feno,
                    normal_scale=1/400,
                    is_outdoor=False,
                    ka=0.5, kd=0.7, ks=0.8, ns=64.0  # Material para a lâmpada 2
                    ),
        Light(color=glm.vec3(0.0, 70.0, 70.0),  # Ciano mais suave
              position=glm.vec3(0, 0, 0),
              ambient=0.1,   # Reduzindo ambiente
              diffuse=0.4,   # Reduzindo difuso
              specular=0.3,  # Reduzindo especular
              enabled=True)
    )
]

#endregion

## main loop ------------------------------------------------------------------------------------------------


## Configuração do seletor 
cam.add_event_handler(glfw.KEY_1,1)
cam.add_event_handler(glfw.KEY_2,2)
cam.add_event_handler(glfw.KEY_3,3)
cam.add_event_handler(glfw.KEY_4,4)
cam.add_event_handler(glfw.KEY_5,5)
cam.add_event_handler(glfw.KEY_6,6)
cam.add_event_handler(glfw.KEY_7,7)
cam.add_event_handler(glfw.KEY_8,8)
cam.add_event_handler(glfw.KEY_9,9)
cam.add_event_handler(glfw.KEY_Q,10)
cam.add_event_handler(glfw.KEY_E,11)
cam.add_event_handler(glfw.KEY_I,30)
cam.add_event_handler(glfw.KEY_O,40)



def setambient(p):
    global ambientLight
    ambientLight = glm.vec3([ambientLight.x + p, ambientLight.y + p, ambientLight.z + p])

def set_light(p,model,attr):
    if isinstance(model,list):
        for m in model:
            if(getattr(m,attr)+p>1 or getattr(m,attr)+p<0):
                continue
            setattr(m,attr,getattr(m,attr)+p)
    else:
        setattr(model,attr,getattr(model,attr)+p)

events_by_keyoutput = {
    1: lambda: setattr(moinho_light, 'enabled', not moinho_light.enabled),
    2: lambda: setattr(lampadas[0][1], 'enabled', not lampadas[0][1].enabled),
    3: lambda: setattr(lampadas[1][1], 'enabled', not lampadas[1][1].enabled),
    4: lambda: setambient(0.1),
    5: lambda: setambient(-0.1),
    6: lambda: set_light(0.1,[moinho_light]+[light for lamp,light in lampadas],'diffuse'),
    7: lambda: set_light(-0.1,[moinho_light]+[light for lamp,light in lampadas],'diffuse'),
    8: lambda: set_light(0.1,[moinho_light]+[light for lamp,light in lampadas],'specular'),
    9: lambda: set_light(-0.1,[moinho_light]+[light for lamp,light in lampadas],'specular'),
    
    30:lambda: moinho.modify(add_pos=np.array([0.0,0.0,0.01])),
    40:lambda: moinho.modify(add_pos=-np.array([0.0,0.0,0.01])),
}



last_frame = glfw.get_time()

while not glfw.window_should_close(window):
    # Cálculo do deltaTime
    current_frame = glfw.get_time()
    delta_time = current_frame - last_frame
    last_frame = current_frame
    
    # Atualiza os uniformes de iluminação
    ourShader.use()
    ourShader.setVec3("viewPos", cam.cameraPos)
    ourShader.setVec3("ambientLight", ambientLight)
    ourShader.setFloat("ambientIntensity", ambientIntensity)
    
    # Prepara o array de luzes (incluindo a luz do moinho e as lâmpadas)
    all_lights = [
        {
            'position': moinho_light.position,
            'color': moinho_light.color,
            'ambient': moinho_light.ambient,
            'diffuse': moinho_light.diffuse,
            'specular': moinho_light.specular,
            'enabled': moinho_light.enabled,
            'isOutdoor': True  # Luz do moinho é outdoor
        }
    ]
    
    # Adiciona as lâmpadas (luzes internas)
    for lamp, light in lampadas:
        all_lights.append({
            'position': light.position,
            'color': light.color,
            'ambient': light.ambient,
            'diffuse': light.diffuse,
            'specular': light.specular,
            'enabled': light.enabled,
            'isOutdoor': False  # Lâmpadas são luzes internas
        })
    
    # Envia as luzes para o shader
    ourShader.setInt("numLights", len(all_lights))
    for i, light in enumerate(all_lights):
        if i >= 10:  # Limite definido no shader
            break
            
        ourShader.setVec3(f"lights[{i}].position", light['position'])
        ourShader.setVec3(f"lights[{i}].color", light['color'])
        ourShader.setFloat(f"lights[{i}].ambient", light['ambient'])
        ourShader.setFloat(f"lights[{i}].diffuse", light['diffuse'])
        ourShader.setFloat(f"lights[{i}].specular", light['specular'])
        ourShader.setBool(f"lights[{i}].enabled", light['enabled'])
        ourShader.setBool(f"lights[{i}].isOutdoor", light['isOutdoor'])
    
    # Limpa o buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    
    # Atualiza a câmera
    cam.atualize_speed(delta_time)

    ## Aplica modificações do teclado:
    if cam.output_value in events_by_keyoutput.keys():
        events_by_keyoutput[cam.output_value]()
        time.sleep(0.1)
    
    # Atualiza a posição da luz do moinho  
    moinho_light.position = glm.vec3(moinho.pos[0]+5, moinho.pos[1]+44.5, moinho.pos[2]+2)
    
    # Atualiza os uniformes de iluminação
    ourShader.use()
    ourShader.setVec3("viewPos", cam.cameraPos)
    
    # Aumenta a intensidade da luz ambiente para melhor visualização
    ourShader.setVec3("ambientLight", ambientLight)
    ourShader.setFloat("ambientIntensity", ambientIntensity)  # Ajusta a intensidade da luz ambiente

    glPushMatrix()
    glTranslatef(moinho_light.position.x, moinho_light.position.y, moinho_light.position.z)
    glPopMatrix()

    # Coeficientes do material agora são definidos individualmente para cada objeto
    
    # Matrizes de transformação
    mat_view = cam.view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)
    
    mat_projection = cam.projection()
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)

    # Draw dos modelos:
    ourShader.use()
    ourShader.setBool("isOutdoor", estabulo.is_outdoor)
    ourShader.setFloat("ka", estabulo.ka)
    ourShader.setFloat("kd", estabulo.kd)
    ourShader.setFloat("ks", estabulo.ks)
    ourShader.setFloat("ns", estabulo.ns)
    glBindVertexArray(VAO)
    estabulo.draw(program) 
    glDrawArrays(GL_TRIANGLES, estabulo.verticeInicial, estabulo.quantosVertices)
    glBindVertexArray(0)
    
    # Desenha o porco
    ourShader.use()
    ourShader.setBool("isOutdoor", porco.is_outdoor)
    ourShader.setFloat("ka", porco.ka)
    ourShader.setFloat("kd", porco.kd)
    ourShader.setFloat("ks", porco.ks)
    ourShader.setFloat("ns", porco.ns)
    glBindVertexArray(VAO)
    porco.draw(program)
    glDrawArrays(GL_TRIANGLES, porco.verticeInicial, porco.quantosVertices)
    glBindVertexArray(0)
    
    # Desenha o moinho
    ourShader.use()
    ourShader.setBool("isOutdoor", moinho.is_outdoor)
    ourShader.setFloat("ka", moinho.ka)
    ourShader.setFloat("kd", moinho.kd)
    ourShader.setFloat("ks", moinho.ks)
    ourShader.setFloat("ns", moinho.ns)
    glBindVertexArray(VAO)
    moinho.draw(program)
    glDrawArrays(GL_TRIANGLES, moinho.verticeInicial, moinho.quantosVertices)
    glBindVertexArray(0)
    
    # Atualiza e desenha as lâmpadas
    for lampada, light in lampadas:
        ourShader.use()
        ourShader.setBool("isOutdoor", lampada.is_outdoor)
        ourShader.setFloat("ka", lampada.ka)
        ourShader.setFloat("kd", lampada.kd)
        ourShader.setFloat("ks", lampada.ks)
        ourShader.setFloat("ns", lampada.ns)
        glBindVertexArray(VAO)
        lampada.draw(program)
        glDrawArrays(GL_TRIANGLES, lampada.verticeInicial, lampada.quantosVertices)
        glBindVertexArray(0)
        light.position = glm.vec3(lampada.pos[0]/3, lampada.pos[1], 1 + lampada.pos[2]/30)
    # Desenha os fenos
    for feno in fenos:
        ourShader.use()
        ourShader.setBool("isOutdoor", feno.is_outdoor)
        ourShader.setFloat("ka", feno.ka)
        ourShader.setFloat("kd", feno.kd)
        ourShader.setFloat("ks", feno.ks)
        ourShader.setFloat("ns", feno.ns)
        glBindVertexArray(VAO)
        feno.draw(program)
        glDrawArrays(GL_TRIANGLES, feno.verticeInicial, feno.quantosVertices)
        glBindVertexArray(0)
     # Desenha o chão
    for chao in choes:
        ourShader.use()
        ourShader.setBool("isOutdoor", chao.is_outdoor)
        ourShader.setFloat("ka", chao.ka)
        ourShader.setFloat("kd", chao.kd)
        ourShader.setFloat("ks", chao.ks)
        ourShader.setFloat("ns", chao.ns)
        glBindVertexArray(VAO)
        chao.draw(program)
        glDrawArrays(GL_TRIANGLES, chao.verticeInicial, chao.quantosVertices)
        glBindVertexArray(0)
    # Desenha o céu
    ourShader.use()
    ourShader.setBool("isOutdoor", ceu.is_outdoor)
    ourShader.setFloat("ka", ceu.ka)
    ourShader.setFloat("kd", ceu.kd)
    ourShader.setFloat("ks", ceu.ks)
    ourShader.setFloat("ns", ceu.ns)
    glBindVertexArray(VAO)
    ceu.draw(program)
    glDrawArrays(GL_TRIANGLES, ceu.verticeInicial, ceu.quantosVertices)
    glBindVertexArray(0)
    # Desenha as ovelhas
    for ovelha in ovelhas:
        ourShader.use()
        ourShader.setBool("isOutdoor", ovelha.is_outdoor)
        ourShader.setFloat("ka", ovelha.ka)
        ourShader.setFloat("kd", ovelha.kd)
        ourShader.setFloat("ks", ovelha.ks)
        ourShader.setFloat("ns", ovelha.ns)
        glBindVertexArray(VAO)
        ovelha.draw(program)
        glDrawArrays(GL_TRIANGLES, ovelha.verticeInicial, ovelha.quantosVertices)
        glBindVertexArray(0)
    # Desenha o chão interno
    ourShader.use()
    ourShader.setBool("isOutdoor", chao_interno.is_outdoor)
    ourShader.setFloat("ka", chao_interno.ka)
    ourShader.setFloat("kd", chao_interno.kd)
    ourShader.setFloat("ks", chao_interno.ks)
    ourShader.setFloat("ns", chao_interno.ns)
    glBindVertexArray(VAO)
    chao_interno.draw(program)
    glDrawArrays(GL_TRIANGLES, chao_interno.verticeInicial, chao_interno.quantosVertices)
    glBindVertexArray(0)
    
    ourShader.use()
    ourShader.setBool("isOutdoor", galinha.is_outdoor)
    ourShader.setFloat("ka", galinha.ka)
    ourShader.setFloat("kd", galinha.kd)
    ourShader.setFloat("ks", galinha.ks)
    ourShader.setFloat("ns", galinha.ns)
    glBindVertexArray(VAO)
    galinha.draw(program)
    glDrawArrays(GL_TRIANGLES, galinha.verticeInicial, galinha.quantosVertices)
    glBindVertexArray(0)
    
    for grama in gramas:
        ourShader.use()
        ourShader.setBool("isOutdoor", grama.is_outdoor)
        ourShader.setFloat("ka", grama.ka)
        ourShader.setFloat("kd", grama.kd)
        ourShader.setFloat("ks", grama.ks)
        ourShader.setFloat("ns", grama.ns)
        glBindVertexArray(VAO)
        grama.draw(program)
        glDrawArrays(GL_TRIANGLES, grama.verticeInicial, grama.quantosVertices)
        glBindVertexArray(0)
    
    # Atualiza a janela
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
