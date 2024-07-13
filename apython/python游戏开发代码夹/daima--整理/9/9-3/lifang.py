# 导入OpenGL的库
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
# from numpy import *
import sys


def init():
    # 初始化背景
    glClearColor(1.0, 0.0, 1.0, 1.0)
    gluOrtho2D(-5.0, 5.0, -5.0, 5.0)


def plotfunc():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(5.0)

    # 绘制坐标系
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_LINES)  # 画线
    glVertex2f(-5.0, 0.0)
    glVertex2f(5.0, 0.0)
    glVertex2f(0.0, 5.0)
    glVertex2f(0.0, -5.0)
    glEnd()

    # 绘制y = x*x*x (-5.0 < x < 5.0) 的图像
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)  # 画线
    # for x in arange(-5.0, 5.0, 0.1):
    for x in (i * 0.1 for i in range(-50, 50)):
        y = x * x * x
        glVertex2f(x, y)  # 绘制每个0.1个步长的点
    glEnd()

    glFlush()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowPosition(50, 50)
    glutInitWindowSize(400, 400)
    glutCreateWindow("Function Plotter".encode('utf-8'))
    glutDisplayFunc(plotfunc)
    init()
    glutMainLoop()


main()