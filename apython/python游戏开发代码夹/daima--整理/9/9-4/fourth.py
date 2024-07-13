import glfw
from OpenGL.GL import *
import numpy as np

gkey=[]

def render():
    global gkey #修改全局变量
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
 # 绘制X、Y坐标系
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

    glColor3ub(255, 255, 255)   #重置为白色

    for i in range(len(gkey)):              # 顺序：r-to-l全局帧/
        if gkey[len(gkey)-i-1]==2:          #按下Q键，在 x轴平移-0.1
            glTranslatef(-0.1, 0, 0)
        elif gkey[len(gkey)-i-1]==3:        #按下E键，在x轴上平移0.1
            glTranslatef(0.1, 0, 0)
        elif gkey[len(gkey) - i - 1] == 4:  #按下A键，逆时针旋转10
            glRotatef(10, 0, 0, 1)
        elif gkey[len(gkey)-i-1]==5:        #按下D键，逆时针旋转-10
            glRotatef(-10,0,0,1)

    drawTriangle()  #三角函数

def drawTriangle(): #固定三角形坐标
    glBegin(GL_TRIANGLES)                   #使用GL_TRIANGLES方式绘制三角形
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global gkey                             #修改全局变量
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:                 #如果按键值为glfw.KEY_1
            gkey= []
        elif key==glfw.KEY_Q:
            gkey= gkey + [2]                #在列表中添加按键q的操作
        elif key==glfw.KEY_E:
            gkey= gkey + [3]                #在列表中添加按键e的操作
        elif key==glfw.KEY_A:
            gkey= gkey + [4]                #在列表中添加按键a的操作
        elif key==glfw.KEY_D:
            gkey= gkey + [5]                #在列表中添加按键d的操作
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480, 'triangle movement', None,None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()