from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

def lineSegment():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0,0.4,0.2)     #线的颜色为绿色
    glBegin(GL_LINES)
    glVertex2i(180,15)
    glVertex2i(10,145)
    glEnd()
    glFlush()

def init():
    glClearColor(1.0,1.0,1.0,0.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0.0,200.0,0.0,150.0)

if __name__=="__main__":
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
    glutInitWindowPosition(50,100)
    glutInitWindowSize(400,300)
    glutCreateWindow('First Program'.encode('utf-8'))

    init()
    glutDisplayFunc(lineSegment)
    glutMainLoop()
