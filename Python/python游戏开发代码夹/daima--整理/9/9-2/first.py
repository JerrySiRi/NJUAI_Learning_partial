from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def Draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glRotatef(0.5, 0, 1, 0)
    glutWireTeapot(0.5)
    glFlush()

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
glutInitWindowSize(400, 400)
glutCreateWindow("test".encode('utf-8'))
glutDisplayFunc(Draw)
glutIdleFunc(Draw)
glutMainLoop()

if __name__ == '__main__':
    Draw()