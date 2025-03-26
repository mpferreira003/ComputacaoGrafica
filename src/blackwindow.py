import glfw

glfw.init()
window = glfw.create_window(500,500,"Bom dia",None,None)
glfw.make_context_current(window)
while not glfw.window_should_close(window):
    glfw.poll_events()
    # glfw.wait_events()
    glfw.swap_buffers(window)
glfw.terminate()