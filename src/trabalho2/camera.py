import glm
import glfw
from OpenGL.GL import *
import matriz

class Camera():
    
    
    polygonal_mode = False
    
    firstMouse = True
    
    # timing
    deltaTime = 0.0	# time between current frame and last frame
    lastFrame = 0.0
    
    def __init__(self,window,altura,largura,
                 cameraPos   = glm.vec3(0.0,  0.0,  1.0),
                 cameraFront = glm.vec3(0.0,  0.0, -1.0),
                 cameraUp    = glm.vec3(0.0,  1.0,  0.0),
                 yaw   = -90.0,
                 pitch =  0.0,
                 fov   =  45.0,
                 near = 0.1,
                 far = 200,
                 chao_limit=0,
                 sensitivity:float=0.1,
                 main_speed=50):
        self.yaw=yaw
        self.pitch=pitch
        self.fov=fov
        self.near=near
        self.far=far
        
        self.sensitivity=sensitivity
        self.main_speed=main_speed
        self.cameraSpeed = 0
        self.chao_limit=chao_limit
        
        self.cameraPos=cameraPos
        self.cameraFront=cameraFront
        self.cameraUp=cameraUp
        
        self.altura = altura
        self.largura = largura
        
        
        self.lastX =  largura / 2.0
        self.lastY =  altura / 2.0
        
        
        ## Colocar nas cameras    
        glfw.set_key_callback(window,self.key_event)
        glfw.set_framebuffer_size_callback(window, self.framebuffer_size_callback)
        glfw.set_cursor_pos_callback(window, self.mouse_callback)
        glfw.set_scroll_callback(window, self.scroll_callback)
        
        # tell GLFW to capture our mouse
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    
    def atualize_speed(self,deltaTime):
        self.cameraSpeed = self.main_speed*deltaTime
    def key_event(self,window,key,scancode,action,mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        
        if key == glfw.KEY_Q and action == glfw.PRESS:
            self.get_status()
        
        if key == glfw.KEY_W and (action == glfw.PRESS or action == glfw.REPEAT):
            new_pos = self.cameraPos + self.cameraSpeed * self.cameraFront
            if new_pos[1]>self.chao_limit:
                self.cameraPos = new_pos
        
        if key == glfw.KEY_S and (action == glfw.PRESS or action == glfw.REPEAT):
            new_pos = self.cameraPos - self.cameraSpeed * self.cameraFront
            if new_pos[1]>self.chao_limit:
                self.cameraPos = new_pos
        
        if key == glfw.KEY_A and (action == glfw.PRESS or action == glfw.REPEAT):
            new_pos = self.cameraPos - glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * self.cameraSpeed
            if new_pos[1]>self.chao_limit:
                self.cameraPos = new_pos
            
        if key == glfw.KEY_D and (action == glfw.PRESS or action == glfw.REPEAT):
            new_pos = self.cameraPos + glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * self.cameraSpeed
            if new_pos[1]>self.chao_limit:
                self.cameraPos = new_pos

        if key == glfw.KEY_SPACE and (action == glfw.PRESS or action == glfw.REPEAT):
            new_pos = self.cameraPos + self.cameraUp * self.cameraSpeed
            if new_pos[1]>self.chao_limit:
                self.cameraPos = new_pos
        
        if key == glfw.KEY_LEFT_SHIFT and (action == glfw.PRESS or action == glfw.REPEAT):
            new_pos = self.cameraPos - self.cameraUp * self.cameraSpeed
            if new_pos[1]>self.chao_limit:
                self.cameraPos = new_pos
            
        if key == glfw.KEY_P and action == glfw.PRESS:
            polygonal_mode = not polygonal_mode
        
    def get_status(self):
        print("Camera status --- ")
        print(f"cameraPos: {self.cameraPos}")
        print(f"cameraFront: {self.cameraFront}")
        print(f"cameraUp: {self.cameraUp}")
        print(f'yaw: {self.yaw}')
        print(f'pitch: {self.pitch}')
        print(f'fov: {self.fov}\n')
    
    
    def framebuffer_size_callback(window, largura, altura):
        
        # make sure the viewport matches the new window dimensions note that width and 
        # height will be significantly larger than specified on retina displays.
        glViewport(0, 0, largura, altura)

    # glfw: whenever the mouse moves, this callback is called
    # -------------------------------------------------------
    def mouse_callback(self,window, xpos, ypos):
    
        if (self.firstMouse):
            
            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False
        
        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos # reversed since y-coordinates go from bottom to top
        self.lastX = xpos
        self.lastY = ypos

        
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        self.yaw += xoffset
        self.pitch += yoffset
        
        # make sure that when pitch is out of bounds, screen doesn't get flipped
        if (self.pitch > 89.0):
            self.pitch = 89.0
        if (self.pitch < -89.0):
            self.pitch = -89.0

        front = glm.vec3()
        front.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        front.y = glm.sin(glm.radians(self.pitch))
        front.z = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.cameraFront = glm.normalize(front)

    # glfw: whenever the mouse scroll wheel scrolls, this callback is called
    # ----------------------------------------------------------------------
    def scroll_callback(self,window, xoffset, yoffset):
        
        self.fov -= yoffset
        if (self.fov < 1.0):
            self.fov = 1.0
        if (self.fov > 45.0):
            self.fov = 45.0
    
    def view(self):
        return matriz.view(self.cameraPos, self.cameraFront, self.cameraUp)
    def projection(self):
        return matriz.projection(self.fov,self.altura,self.largura,near=self.near,far=self.far)