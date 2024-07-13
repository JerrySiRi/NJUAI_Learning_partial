# 旋转点和矢量


import glfw
from OpenGL.GL import *
import numpy as np

def render(M):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # 绘制x、y坐标轴
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)                   #颜色
    #绘制point点p
    glBegin(GL_POINTS)
    # 点阵列的第三个元素，最后一个排列要素是1
    glVertex2fv((M @ np.array([.5, 0.,1.]))[:-1] )
    glEnd()
    # 绘制矢量 v / 绘制反向v
    glBegin(GL_LINES)
    # 实现的向量数组的第三个元素是0 ，最后一个排列要素是0
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv((M @ np.array([.5, 0.,0.]))[:-1] )
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480, 'rotating point&vector', None,None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        t = glfw.get_time()
        #逆时针旋转t / 像时间指针一样，逆时针旋转
        R = np.array([[np.cos(t), -np.sin(t), 0.],
                      [np.sin(t), np.cos(t), 0.],
                      [0., 0., 1.]])
        #在x轴上平移0.5
        T = np.array([[1.,0.,.5],
                     [0.,1.,0.],
                     [0.,0.,1.]])
        #第一次旋转和第二次旋转/
        render(R@T)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()