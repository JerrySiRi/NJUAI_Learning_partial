import sys

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print(
    '''
ERROR: PyOpenGL not installed properly.  
        ''')
    sys.exit()

spin = 0.0


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glPushMatrix()
    glRotatef(spin, 0.0, 0.0, 1.0)
    glColor3f(1.0, 1.0, 1.0)
    glRectf(-25.0, -25.0, 25.0, 25.0)
    glPopMatrix()
    glutSwapBuffers()


def spinDisplay():
    global spin
    spin = spin + 2.0
    if (spin > 360.0):
        spin = spin - 360.0
    glutPostRedisplay()


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_FLAT)


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-50.0, 50.0, -50.0, 50.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):
            glutIdleFunc(spinDisplay)
    elif button == GLUT_MIDDLE_BUTTON or button == GLUT_RIGHT_BUTTON:
        if (state == GLUT_DOWN):
            glutIdleFunc(None)


#  请求双缓冲显示模式。
# 注册鼠标输入回调函数
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(250, 250)
glutInitWindowPosition(100, 100)
glutCreateWindow('Double'.encode('utf-8'))
init()
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutMouseFunc(mouse)
glutMainLoop()