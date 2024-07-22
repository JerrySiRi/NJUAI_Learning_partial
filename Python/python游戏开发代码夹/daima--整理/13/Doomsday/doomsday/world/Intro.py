from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText

# The name of the media file.
MEDIAFILE="../../assets/cutscenes/intro.mpg"

class Intro(DirectObject):
    
    def __init__(self):
        self.tex = MovieTexture("Intro")
        assert self.tex.read(MEDIAFILE), "Failed to load video!"
        cm = CardMaker("Card maker");
        cm.setFrameFullscreenQuad()
        cm.setUvRange(self.tex)
        card = NodePath(cm.generate())
        card.reparentTo(render2d)
        card.setTexture(self.tex)
        card.setScale(card, 1)
        self.sound=loader.loadSfx(MEDIAFILE)
        self.tex.synchronizeTo(self.sound)
        self.card = card
        self.play()
        
    def play(self):
        self.sound.play()
        
    def destroy(self):
        self.sound.stop()
        self.card.removeNode()
