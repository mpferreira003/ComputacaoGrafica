from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import os
os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"



def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glutSwapBuffers()

# Initialize GLUT
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
glutInitWindowSize(500, 500)  # Set window size
glutCreateWindow(b"OpenGL Test")

# Print OpenGL version
print("OpenGL version:", glGetString(GL_VERSION).decode("utf-8"))

# Set up GLUT display function
glutDisplayFunc(display)

# Enter GLUT main loop (prevents immediate exit)
glutMainLoop()
