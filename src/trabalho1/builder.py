from OpenGL.GL import *
import glfw
def build_program(program):
    # Builda e linka o programa
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')
        
    glUseProgram(program) # Make program the default program

def create_window(width,weight,title='Programa'):
    window = glfw.create_window(width, weight, title, None, None)
    
    if (window == None):
        print("Failed to create GLFW window")
        glfwTerminate()
    return window

def request_buffer_slot():
    buffer_VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer_VBO)
    return buffer_VBO