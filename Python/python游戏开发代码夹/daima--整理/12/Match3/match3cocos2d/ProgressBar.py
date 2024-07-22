import cocos
from pyglet import gl


class ProgressBar(cocos.cocosnode.CocosNode):

    def __init__(self, width, height):
        super(ProgressBar, self).__init__()
        self.width, self.height = width, height
        self.vertexes_in = [(0, 0, 0), (width, 0, 0), (width, height, 0), (0, height, 0)]
        self.vertexes_out = [(-2, -2, 0),
            (width + 2, -2, 0), (width + 2, height + 2, 0), (-2, height + 2, 0)]

    def set_progress(self, percent):
        width = int(self.width * percent)
        height = self.height
        self.vertexes_in = [(0, 0, 0), (width, 0, 0), (width, height, 0), (0, height, 0)]

    def draw(self):
        gl.glPushMatrix()
        self.transform()
        gl.glBegin(gl.GL_QUADS)
        gl.glColor4ub(*(255, 255, 255, 255))
        for v in self.vertexes_out:
            gl.glVertex3i(*v)
        gl.glColor4ub(*(0, 150, 0, 255))
        for v in self.vertexes_in:
            gl.glVertex3i(*v)
        gl.glEnd()
        gl.glPopMatrix()
