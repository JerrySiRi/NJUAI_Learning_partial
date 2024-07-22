import sys
import math
from time import sleep

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print(''' Fehler: PyOpenGL nicht intalliert !!''')
  sys.exit( )

animationAngle = 0.0
frameRate = 25
animationTime = 0

def animationStep( ):
	"""更新动画参数"""
	global animationAngle
	global frameRate
	animationAngle += 0.3
	while animationAngle > 360:
		animationAngle -= 360
	sleep( 1 / float( frameRate ) )
	glutPostRedisplay( )

degree=3
s2=math.sqrt(2)/2.0

# 初始化圆控制点.
circlePoints = [\
	[0.0, 1.0, 0.0, 1.0],\
	[s2, s2, 0.0, s2],\
	[1.0, 0.0, 0.0, 1.0],\
	[s2, -s2, 0.0, s2],\
	[0.0, -1.0, 0.0, 1.0],\
	[-s2, -s2, 0.0, s2],\
	[-1.0, 0.0, 0.0, 1.0],\
	[-s2, s2, 0.0, s2],\
	]

# 确保圆正确关闭
circlePoints = circlePoints + [circlePoints[0], circlePoints[1]]

# 初始化circleknots
circleKnots =  [ 0.0 ] + \
	[ float(i/2) for i in range( len( circlePoints ) + degree -1 )]

def display(  ):
	glClear( GL_COLOR_BUFFER_BIT )
	glMatrixMode( GL_PROJECTION )
	glLoadIdentity( )
	xSize, ySize = glutGet( GLUT_WINDOW_WIDTH ), glutGet( GLUT_WINDOW_HEIGHT )
	gluPerspective(60, float(xSize) / float(ySize), 0.1, 50)
	glMatrixMode( GL_MODELVIEW )
	glLoadIdentity( )
	glTranslatef( 0, 0, -2 )
	glRotatef( animationAngle, 0, 0, 1 )
	global circlePoints, circleKnots
	glColor3f(0, 1, 0)
	glBegin(GL_LINE_STRIP)
	for coord in circlePoints:
		glVertex3f(coord[0], coord[1], coord[2]);
	glEnd()
	global nurb
	glColor3f(1, 1, 1)
	gluBeginCurve( nurb )
	gluNurbsCurve	(	nurb, circleKnots, circlePoints, GL_MAP1_VERTEX_4 )
	gluEndCurve( nurb )
	glutSwapBuffers( )

nurb=None
samplingTolerance=1.0
def init(  ):
	"""GLUT初始化函数."""
	glClearColor ( 0, 0, 0, 0 )
	global nurb
	nurb = gluNewNurbsRenderer()
	global samplingTolerance
	glLineWidth(2.0)
	gluNurbsProperty(nurb, GLU_SAMPLING_TOLERANCE, samplingTolerance)

glutInit( sys.argv )
glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB )
glutInitWindowSize( 250, 250 )
glutInitWindowPosition( 100, 100 )
glutCreateWindow( sys.argv[0].encode('utf-8'))
init()
glutDisplayFunc( display )
glutIdleFunc( animationStep )
glutMainLoop( )