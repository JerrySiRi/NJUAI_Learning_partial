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

teapotList = None

# 初始化深度缓冲器、投影矩阵、光源和照明模型。这里不指定材质属性。

def init():
   ambient = [0.0, 0.0, 0.0, 1.0]
   diffuse = [1.0, 1.0, 1.0, 1.0]
   specular = [1.0, 1.0, 1.0, 1.0]
   position = [0.0, 3.0, 3.0, 0.0]

   lmodel_ambient = [0.2, 0.2, 0.2, 1.0]
   local_view = [0.0]

   glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
   glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
   glLightfv(GL_LIGHT0, GL_POSITION, position)
   glLightModelfv(GL_LIGHT_MODEL_AMBIENT, lmodel_ambient)
   glLightModelfv(GL_LIGHT_MODEL_LOCAL_VIEWER, local_view)

   glFrontFace(GL_CW)
   glEnable(GL_LIGHTING)
   glEnable(GL_LIGHT0)
   glEnable(GL_AUTO_NORMAL)
   glEnable(GL_NORMALIZE)
   glEnable(GL_DEPTH_TEST)

   #  高效——制作茶壶陈列
   global teapotList
   teapotList = glGenLists(1)
   glNewList (teapotList, GL_COMPILE)
   glutSolidTeapot(1.0)
   glEndList ()

# 将物体移动到位置。使用第3到第12个参数来指定材料属性。画一个茶壶。
def renderTeapot(x, y, ambr, ambg, ambb, difr, difg,
                      difb, specr, specg, specb, shine):
   mat = [0, 0, 0, 0]

   glPushMatrix()
   glTranslatef(x, y, 0.0)
   mat[0] = ambr; mat[1] = ambg; mat[2] = ambb; mat[3] = 1.0
   glMaterialfv(GL_FRONT, GL_AMBIENT, mat)
   mat[0] = difr; mat[1] = difg; mat[2] = difb
   glMaterialfv(GL_FRONT, GL_DIFFUSE, mat)
   mat[0] = specr; mat[1] = specg; mat[2] = specb
   glMaterialfv(GL_FRONT, GL_SPECULAR, mat)
   glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0)
   glutSolidTeapot(1.0)
   glPopMatrix()


#  第一列：翡翠、玉石、黑曜石、珍珠、红宝石、绿松石
#  第二列：黄铜、青铜、铬、铜、金、银
#  第三列：黑色、青色、绿色、红色、白色、黄色塑料
#  第四列：黑、青、绿、红、白、黄橡胶
def display():
    global teapotList
    if not teapotList:
        init();
    glClearColor( 1.0,1.0,1.0, 1.0 )
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    renderTeapot(2.0, 17.0, 0.0215, 0.1745, 0.0215,
      0.07568, 0.61424, 0.07568, 0.633, 0.727811, 0.633, 0.6)
    renderTeapot(2.0, 14.0, 0.135, 0.2225, 0.1575,
      0.54, 0.89, 0.63, 0.316228, 0.316228, 0.316228, 0.1)
    renderTeapot(2.0, 11.0, 0.05375, 0.05, 0.06625,
      0.18275, 0.17, 0.22525, 0.332741, 0.328634, 0.346435, 0.3)
    renderTeapot(2.0, 8.0, 0.25, 0.20725, 0.20725,
      1, 0.829, 0.829, 0.296648, 0.296648, 0.296648, 0.088)
    renderTeapot(2.0, 5.0, 0.1745, 0.01175, 0.01175,
      0.61424, 0.04136, 0.04136, 0.727811, 0.626959, 0.626959, 0.6)
    renderTeapot(2.0, 2.0, 0.1, 0.18725, 0.1745,
      0.396, 0.74151, 0.69102, 0.297254, 0.30829, 0.306678, 0.1)
    renderTeapot(6.0, 17.0, 0.329412, 0.223529, 0.027451,
      0.780392, 0.568627, 0.113725, 0.992157, 0.941176, 0.807843,
      0.21794872);
    renderTeapot(6.0, 14.0, 0.2125, 0.1275, 0.054,
      0.714, 0.4284, 0.18144, 0.393548, 0.271906, 0.166721, 0.2)
    renderTeapot(6.0, 11.0, 0.25, 0.25, 0.25,
      0.4, 0.4, 0.4, 0.774597, 0.774597, 0.774597, 0.6)
    renderTeapot(6.0, 8.0, 0.19125, 0.0735, 0.0225,
      0.7038, 0.27048, 0.0828, 0.256777, 0.137622, 0.086014, 0.1)
    renderTeapot(6.0, 5.0, 0.24725, 0.1995, 0.0745,
      0.75164, 0.60648, 0.22648, 0.628281, 0.555802, 0.366065, 0.4)
    renderTeapot(6.0, 2.0, 0.19225, 0.19225, 0.19225,
      0.50754, 0.50754, 0.50754, 0.508273, 0.508273, 0.508273, 0.4)
    renderTeapot(10.0, 17.0, 0.0, 0.0, 0.0, 0.01, 0.01, 0.01,
      0.50, 0.50, 0.50, .25)
    renderTeapot(10.0, 14.0, 0.0, 0.1, 0.06, 0.0, 0.50980392, 0.50980392,
      0.50196078, 0.50196078, 0.50196078, .25)
    renderTeapot(10.0, 11.0, 0.0, 0.0, 0.0,
      0.1, 0.35, 0.1, 0.45, 0.55, 0.45, .25);
    renderTeapot(10.0, 8.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0,
      0.7, 0.6, 0.6, .25)
    renderTeapot(10.0, 5.0, 0.0, 0.0, 0.0, 0.55, 0.55, 0.55,
      0.70, 0.70, 0.70, .25)
    renderTeapot(10.0, 2.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0,
      0.60, 0.60, 0.50, .25)
    renderTeapot(14.0, 17.0, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01,
      0.4, 0.4, 0.4, .078125)
    renderTeapot(14.0, 14.0, 0.0, 0.05, 0.05, 0.4, 0.5, 0.5,
      0.04, 0.7, 0.7, .078125)
    renderTeapot(14.0, 11.0, 0.0, 0.05, 0.0, 0.4, 0.5, 0.4,
      0.04, 0.7, 0.04, .078125)
    renderTeapot(14.0, 8.0, 0.05, 0.0, 0.0, 0.5, 0.4, 0.4,
      0.7, 0.04, 0.04, .078125)
    renderTeapot(14.0, 5.0, 0.05, 0.05, 0.05, 0.5, 0.5, 0.5,
      0.7, 0.7, 0.7, .078125)
    renderTeapot(14.0, 2.0, 0.05, 0.05, 0.0, 0.5, 0.5, 0.4,
      0.7, 0.7, 0.04, .078125)
    glutSwapBuffers()

def reshape(w, h):
   glViewport(0, 0, w, h)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   if (w <= h):
      glOrtho(0.0, 16.0, 0.0, 16.0*h/w, -10.0, 10.0)
   else:
      glOrtho(0.0, 16.0*w/h, 0.0, 16.0, -10.0, 10.0)
   glMatrixMode(GL_MODELVIEW)


def keyboard(key, x, y):
   if key == chr(27):
      sys.exit(0)

# Main Loop
if __name__ == "__main__":
	glutInit(sys.argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
	glutInitWindowSize(500, 600);
	glutInitWindowPosition(50,50);
	glutCreateWindow(sys.argv[0].encode('utf-8'));
	glutReshapeFunc(reshape)
	glutDisplayFunc(display)
	glutKeyboardFunc(keyboard)
	glutMainLoop()