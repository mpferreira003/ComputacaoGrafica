from OpenGL.GL import *

SN_POSITION_NAME = 'position'
SN_COLOR = 'color'
SN_MAT_TRANSFORMATION = 'transformation'

vertex_code = """
        attribute vec2 {pos};
        uniform mat4 {transformation};
        void main(){{
            gl_Position = {transformation} * vec4({pos},0.0,1.0);
        }}
        """.format(pos=SN_POSITION_NAME,transformation=SN_MAT_TRANSFORMATION)
vertex_code = vertex_code.replace("{{", "{").replace("}}", "}")

fragment_code = """
        uniform vec4 {color};
        void main(){{
            gl_FragColor = {color};
        }}
        """.format(color=SN_COLOR)
fragment_code = fragment_code.replace("{{", "{").replace("}}", "}")


def compile_shaders(program):
    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)
    
    # Set shaders source
    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, fragment_code)


    # Compile shaders
    glCompileShader(vertex)
    if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(vertex).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Vertex Shader")


    glCompileShader(fragment)
    if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(fragment).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Fragment Shader")

    # Attach shader objects to the program
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
