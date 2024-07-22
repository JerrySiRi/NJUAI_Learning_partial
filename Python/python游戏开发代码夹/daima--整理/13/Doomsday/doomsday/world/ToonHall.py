from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from panda3d.core import Vec3, Vec4
from doomsday.base import SoundBank

class ToonHall(DirectObject):
    
    nearbyCogs = []
    alarmPlaying = False
    firstPositions = {}
    
    def __init__(self, toonhall, door):
        self.toonhall = toonhall
        self.door = door
        self.rightDoorHole = self.door.find('**/doorFrameHoleRight')
        self.rightDoor = self.toonhall.find('**/rightDoor')
        self.sfx = SoundBank.getSound('toonhall_warning')
        base.taskMgr.doMethodLater(0.8, self.detectNearbyCogs, 'Detect Nearby Cogs')
        
    def detectNearbyCogs(self, task):
        nearbyCogs = []
        for cog in render.find('**/Cogs').getChildren():
            if(self.rightDoor.getDistance(cog) <= 60):
                nearbyCogs.append(cog)
        if not self.alarmPlaying and len(nearbyCogs) > 0:
            self.sfx.setLoop(True)
            self.sfx.play()
            self.alarmPlaying = True
        elif self.alarmPlaying and len(nearbyCogs) == 0:
            self.sfx.stop()
            self.alarmPlaying = False
        return Task.cont
        
    def startCogEnter(self, avatar):
        pos = avatar.getCog().getPos(render)
        self.firstPositions.update({avatar.getName():Vec3(pos.getX(), pos.getY(), pos.getZ())})
        base.taskMgr.add(self.moveAvatarToDoor, 'Move Avatar To Door', extraArgs = [avatar.getCog()], appendTask = True)
        
    def moveAvatarToDoor(self, avatar, task):
        pos = self.firstPositions.get(avatar.getPythonTag("Cog").getName())
        avatar.posInterval(1, Vec3(pos.getX() - 0.95, pos.getY(), pos.getZ()), startPos = (pos.getX(), pos.getY() - 1, pos.getZ()), blendType = 'easeInOut')
        base.taskMgr.doMethodLater(0.8, self.changeAnimLoop, 'Change Animation', extraArgs = [avatar, 'neutral'], appendTask = True)
        base.taskMgr.doMethodLater(0.9, self.openDoors, 'Open Doors', extraArgs = [avatar], appendTask = True)
        return Task.done
    
    def openDoors(self, avatar, task):
        if not avatar.getPythonTag('Cog').isDefeated:
            self.rightDoorHole.show()
            self.rightDoor.show()
            SoundBank.getSound('door_open').play()
            self.rightDoor.hprInterval(1, Vec3(95, 0, 0), startHpr=(0, 0, 0), blendType='easeInOut')
            base.taskMgr.doMethodLater(0.2, self.moveAvatarThroughDoor, 'Move Avatar Through Door', extraArgs = [avatar], appendTask = True)
        else:
            self.firstPositions.pop(avatar.getPythonTag("Cog").getName())
        return Task.done
    
    def closeDoors(self, avatar, task):
        self.firstPositions.pop(avatar.getPythonTag("Cog").getName())
        SoundBank.getSound('door_close').play()
        self.rightDoor.hprInterval(0.5, Vec3(0, 0, 0), startHpr = (95, 0, 0), blendType = 'easeInOut')
        self.rightDoor.hide()
        self.rightDoorHole.hide()
        self.toonhall.colorScaleInterval(2, Vec4(0.2509803921568627, 0.2509803921568627, 0.2509803921568627, 1), startColorScale=Vec4(1, 1, 1, 1), blendType='easeInOut')
        return Task.done
    
    def moveAvatarThroughDoor(self, avatar, task):
        if not avatar.getPythonTag('Cog').isDefeated:
            pos = self.firstPositions.get(avatar.getPythonTag("Cog").getName())
            base.taskMgr.add(self.changeAnimLoop, 'Change Animation', extraArgs = [avatar, 'walk'], appendTask = True)
            avatar.posInterval(1, Vec3(pos.getX() + 2, pos.getY(), pos.getZ()), startPos=(pos.getX(), pos.getY(), pos.getZ()))
            if not avatar.getPythonTag('Cog').isDefeated:
                avatar.getPythonTag('Cog').cleanup()
                base.taskMgr.doMethodLater(0.5, self.closeDoor, 'CLose Doors', extraArgs = [avatar], appendTask = True)
        self.firstPositions.pop(avatar.getPythonTag("Cog").getName())
        return Task.done
    
    def changeAnimLoop(self, avatar, anim, task):
        if not avatar.getPythonTag('Cog').isDefeated:
            avatar.loop(anim)
        self.firstPositions.pop(avatar.getPythonTag("Cog").getName())
        return Task.done
        
    def getToonHall(self):
        return self.toonhall