# 旋转2d三角形

import glfw
from OpenGL.GL import *
import numpy as np

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # x轴和y轴
    glBegin(GL_LINES)   #绘制线条线条选项
    glColor3ub(255, 0, 0)   #颜色:红色的y轴
    glVertex2fv(np.array([0.,0.]))  #二维（2fv）
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)   #颜色：绿色的x轴
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # 画三角形
    glBegin(GL_TRIANGLES)   #使用GL_TRIANGLES方式绘制三角形
    glColor3ub(255, 255, 255) #颜色：白色的三角形
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )  # 二维
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )  # 用三角形用矩阵乘(0,0),(0,0.5),(0.5,0)乘以transform
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )  # 各点（因为是point，所以最后的点乘1）后除去最后的点。（[:-1]）
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"rotating_triangle", None,None) #窗口尺寸的大小480*480
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    # glfw.swap_interval : 在调用glfw.swap_buffer()前，调整刷新参数screen、反复设置时间间隔。
    # 如果refresh的值是60Hz，那么每1/60秒重复一次while循环.
    glfw.swap_interval(1)
    while not glfw.window_should_close(window): #直到窗口关闭
        glfw.poll_events()
        t = glfw.get_time() # 小时
        # 以rotate t rad/t rad角度旋转
        th = t
        R = np.array([[np.cos(th), -np.sin(th), 0.],
                      [np.sin(th), np.cos(th), 0.],
                      [0., 0., 1.]])
        # 依据 (.5, 0.) / (0.5, 0)移动
        T = np.array([[1., 0., .5],
                      [0., 1., 0.],
                      [0., 0., 1.]])
        #第一次平移和第二次旋转
        render(R @ T)
        glfw.swap_buffers(window)   # 交换缓冲区
    glfw.terminate()

if __name__ == "__main__":
    main()