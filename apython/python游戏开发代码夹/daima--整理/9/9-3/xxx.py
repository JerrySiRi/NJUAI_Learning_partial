import sys

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ('''
ERROR: PyOpenGL not installed properly.  
        ''')
  sys.exit()

def drawOneLine(x1, y1, x2, y2):
  glBegin(GL_LINES)
  glVertex2f(x1, y1)
  glVertex2f(x2, y2)
  glEnd()


def init():
  glClearColor(0.0, 0.0, 0.0, 0.0)
  glShadeModel(GL_FLAT)

def display():
  glClear(GL_COLOR_BUFFER_BIT)

  # 为所有行选择白色
  glColor3f(1.0, 1.0, 1.0)

  # 在第一行，第3行，每一个有不同的点画
  glEnable(GL_LINE_STIPPLE)

  glLineStipple (1, 0x0101)  #  点虚线
  drawOneLine (50.0, 125.0, 150.0, 125.0)
  glLineStipple (1, 0x00FF)  #  虚线
  drawOneLine (150.0, 125.0, 250.0, 125.0);
  glLineStipple (1, 0x1C47)  #  短线/点/ 短线
  drawOneLine (250.0, 125.0, 350.0, 125.0)

  # 第二行，各有不同的点画。
  glLineWidth(5.0)
  glLineStipple(1, 0x0101)  # 点虚线
  drawOneLine(50.0, 100.0, 150.0, 100.0)
  glLineStipple(1, 0x00FF)  #  虚线
  drawOneLine(150.0, 100.0, 250.0, 100.0)
  glLineStipple(1, 0x1C47)  #   短线/点/ 短线
  drawOneLine(250.0, 100.0, 350.0, 100.0)
  glLineWidth(1.0)

  # 在第三行中，6行，以点/点/短线点画作为单个连接线条的一部分。
  glLineStipple (1, 0x1C47)  # 短线/点/ 短线
  glBegin (GL_LINE_STRIP)
  for i in range(0, 7):
    glVertex2f(50.0 + (i * 50.0), 75.0)
  glEnd()

  # 在第四行中，6条独立的线具有相同的点状*/
  for i in range(0, 6):
    drawOneLine (50.0 + (i * 50.0), 50.0, 50.0 + ((i+1) * 50.0), 50.0)

  # 在第五行，1行，用DASH/DOT/DASH点画α和点画重复因子5
  glLineStipple (5, 0x1C47)  #  dash/dot/dash
  drawOneLine (50.0, 25.0, 350.0, 25.0)

  glDisable (GL_LINE_STIPPLE)
  glFlush ()

def reshape(w, h):
  glViewport(0, 0, w, h)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluOrtho2D(0.0, w, 0.0, h)

def keyboard(key, x, y):
  if key == chr(27):
    sys.exit(0)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(400, 150)
glutInitWindowPosition(100, 100)
glutCreateWindow('Lines'.encode('utf-8'))
init()
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMainLoop()
