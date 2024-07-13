from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShadowPlacer import ShadowPlacer
from direct.directnotify import DirectNotifyGlobal
import doomsday.base.Globals

globalDropShadowFlag = 1
def setGlobalDropShadowFlag(flag):
    global globalDropShadowFlag
    if flag != globalDropShadowFlag:
        globalDropShadowFlag = flag
        messenger.send('globalDropShadowFlagChanged')


globalDropShadowGrayLevel = 0.5

def setGlobalDropShadowGrayLevel(grayLevel):
    global globalDropShadowGrayLevel
    if grayLevel != globalDropShadowGrayLevel:
        globalDropShadowGrayLevel = grayLevel
        messenger.send('globalDropShadowGrayLevelChanged')


class ShadowCaster():
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('ShadowCaster')

    def __init__(self, avatar, squareShadow = False):
        if squareShadow:
            self.shadowFileName = 'phase_3/models/props/square_drop_shadow.bam'
        else:
            self.shadowFileName = 'phase_3/models/props/drop_shadow.bam'
        self.dropShadow = None
        self.shadowPlacer = None
        self.activeShadow = 0
        self.wantsActive = 1
        self.storedActiveState = 0
        self.shadowJoint = avatar.find('**/joint_shadow')
        if hasattr(base, 'wantDynamicShadows') and base.wantDynamicShadows:
            messenger.accept('globalDropShadowFlagChanged', self, self.__globalDropShadowFlagChanged)
            messenger.accept('globalDropShadowGrayLevelChanged', self, self.__globalDropShadowGrayLevelChanged)
        return

    def delete(self):
        if hasattr(base, 'wantDynamicShadows') and base.wantDynamicShadows:
            messenger.ignore('globalDropShadowFlagChanged', self)
            messenger.ignore('globalDropShadowGrayLevelChanged', self)
        self.deleteDropShadow()
        self.shadowJoint = None
        return

    def initializeDropShadow(self, hasGeomNode = True):
        pass
    """
        self.deleteDropShadow()
        dropShadow = loader.loadModel(self.shadowFileName)
        dropShadow.setScale(0.4)
        dropShadow.flattenMedium()
        dropShadow.setBillboardAxis(2)
        dropShadow.setColor(0.0, 0.0, 0.0, globalDropShadowGrayLevel, 1)
        self.shadowPlacer = ShadowPlacer(base.shadowTrav, dropShadow, BitMask32.bit(2), BitMask32.bit(1))
        self.dropShadow = dropShadow
        if not globalDropShadowFlag:
            self.dropShadow.hide()
        if self.getShadowJoint():
            dropShadow.reparentTo(self.getShadowJoint())
        else:
            self.dropShadow.hide()
        #self.setActiveShadow(self.wantsActive)
        self.shadowPlacer.on()
        self.__globalDropShadowFlagChanged()
        self.__globalDropShadowGrayLevelChanged()
    """

    def update(self):
        pass

    def deleteDropShadow(self):
        if self.shadowPlacer:
            self.shadowPlacer.delete()
            self.shadowPlacer = None
        if self.dropShadow:
            self.dropShadow.removeNode()
            self.dropShadow = None
        return

    def setActiveShadow(self, isActive = 1):
        if isActive:
            isActive = self.wantsActive
            if not globalDropShadowFlag:
                self.storedActiveState = isActive
            if self.shadowPlacer != None:
                if isActive:
                    isActive = globalDropShadowFlag
                    self.activeShadow = self.activeShadow != isActive and isActive
                    isActive and self.shadowPlacer.on()
                else:
                    self.shadowPlacer.off()
        return

    def setShadowHeight(self, shadowHeight):
        if self.dropShadow:
            self.dropShadow.setZ(-shadowHeight)

    def getShadowJoint(self):
        return self.shadowJoint

    def hideShadow(self):
        self.dropShadow.hide()

    def showShadow(self):
        if not globalDropShadowFlag:
            self.dropShadow.hide()
        else:
            self.dropShadow.show()

    def __globalDropShadowFlagChanged(self):
        if self.dropShadow != None:
            if globalDropShadowFlag == 0:
                if self.activeShadow == 1:
                    self.storedActiveState = 1
                    self.setActiveShadow(0)
            elif self.activeShadow == 0:
                self.setActiveShadow(1)
            self.showShadow()
        return

    def __globalDropShadowGrayLevelChanged(self):
        if self.dropShadow != None:
            self.dropShadow.setColor(0.0, 0.0, 0.0, globalDropShadowGrayLevel, 1)
        return
        
        