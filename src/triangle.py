import glfw
from OpenGL.GL import *
import numpy as np

# Código do Vertex Shader
vertex_shader_code = """
#version 330 core
layout(location = 0) in vec3 position;
void main()
{
    gl_Position = vec4(position, 1.0);
}
"""

# Código do Fragment Shader
fragment_shader_code = """
#version 330 core
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0, 0.5, 0.2, 1.0);
}
"""

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader

# Inicializar o GLFW
if not glfw.init():
    raise Exception("Não foi possível inicializar o GLFW")

# Configurar o GLFW
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

# Criar a janela
window = glfw.create_window(800, 600, "Controle de Shaders com GLFW", None, None)
if not window:
    glfw.terminate()
    raise Exception("Não foi possível criar a janela GLFW")

glfw.make_context_current(window)

# Compilar os shaders
vertex_shader = compile_shader(vertex_shader_code, GL_VERTEX_SHADER)
fragment_shader = compile_shader(fragment_shader_code, GL_FRAGMENT_SHADER)

# Criar o programa de shader e anexar os shaders compilados
shader_program = glCreateProgram()
glAttachShader(shader_program, vertex_shader)
glAttachShader(shader_program, fragment_shader)
glLinkProgram(shader_program)

# Verificar se houve erro ao linkar o programa
if glGetProgramiv(shader_program, GL_LINK_STATUS) != GL_TRUE:
    raise RuntimeError(glGetProgramInfoLog(shader_program))

# Deletar shaders após linkar
glDeleteShader(vertex_shader)
glDeleteShader(fragment_shader)

# Definir os dados dos vértices
vertices = np.array([
    -0.5, -0.5, 0.0,
     0.5, -0.5, 0.0,
     0.0,  0.5, 0.0
], dtype=np.float32)

# Criar o Vertex Array Object (VAO)
VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)

# Criar o Vertex Buffer Object (VBO)
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Definir os apontadores de atributo de vértice
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

# Desvincular o VBO e VAO
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

# Loop principal
while not glfw.window_should_close(window):
    # Processar eventos
    glfw.poll_events()

    # Limpar o buffer de cor
    glClear(GL_COLOR_BUFFER_BIT)

    # Usar o programa de shader
    glUseProgram(shader_program)

    # Vincular o VAO
    glBindVertexArray(VAO)

    # Desenhar o triângulo
    glDrawArrays(GL_TRIANGLES, 0, 3)

    # Desvincular o VAO
    glBindVertexArray(0)
    
    # Trocar os buffers
    glfw.swap_buffers(window)

# Deletar recursos
glDeleteVertexArrays(1, [VAO])
glDeleteBuffers(1, [VBO])
glDeleteProgram(shader_program)

# Encerrar o GLFW
glfw.terminate()
