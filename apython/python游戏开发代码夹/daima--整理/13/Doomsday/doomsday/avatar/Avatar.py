from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from doomsday.avatar.ShadowCaster import ShadowCaster
from doomsday.avatar.AvatarAttributes import AvatarAttributes

Anims = {
"neutral", "walk", "run", "jump", "jump-idle", "running-jump", 
"running-jump-idle", "pie-throw"
}

class Avatar(DirectObject):
    
    def __init__(self):
        self.data = {
        'Animal' : None,
        'Gender' : None,
        'Weight' : None,
        'Height' : None,
        'Color' : None,
        'HeadType' : None,
        'HeadLength' : None,
        'Shirt' : None,
        'Bottoms' : None
        }
        
    def setData(self, key, value):
        self.data[key] = value
        
    def getData(self):
        return self.data
        
    def generateAnims(self, torso = False, legs = False):
        anims = {}
        if(torso):
            for anim in Anims:
                anims[anim] = loader.loadModel('phase_3/models/char/%s-torso-%s-%s.bam' % (self.data['Weight'], self.data['Gender'], anim))
        if(legs):
            for anim in Anims:
                anims[anim] = loader.loadModel('phase_3/models/char/%s-legs-%s.bam' % (self.data['Height'], anim))
        return anims
    
    def removeOtherParts(self, nodepath, impotent):
        if(impotent == None):
            matches = nodepath
            for part in range(0, matches.getNumPaths()):
                name = matches.getPath(part).getName()
                if(name):
                    if(name == 'muzzle-short-neutral' and self.data['Animal'] == 'mouse'):
                        if(self.data['HeadType'] == 500 or self.data['HeadType'] == 1000):
                            return
                    matches.getPath(part).removeNode()
        else:
            matches = nodepath
            for part in range(0, matches.getNumPaths()):
                if(part != impotent):
                    if(matches.getPath(part).getName()):
                        matches.getPath(part).removeNode()
    
    def setColor(self):
        colorEarAnimals = {'dog', 'horse', 'monkey'}
        body = ['**/head-*', '**/neck', '**/arms', '**/legs', '**/feet', '**/head']
        if(self.data['Animal'] not in colorEarAnimals):
            body.append('**/*ears*')
        for part in range(len(body)):
            self.Avatar.findAllMatches(body[part]).setColor(self.data['Color'])
        self.Avatar.findAllMatches("**/hands").setColor(AvatarAttributes().getColor('white'))
        
    def generate(self):
        head = loader.loadModel('phase_3/models/char/%s-heads-%s.bam' % (self.data['Animal'], self.data['HeadType']))
        torso = loader.loadModel('phase_3/models/char/%s-torso-%s.bam' % (self.data['Weight'], self.data['Gender']))
        legs = loader.loadModel('phase_3/models/char/%s-legs.bam' % (self.data['Height']))
        
        if(self.data['HeadLength'] == 'short'):
            self.removeOtherParts(head.findAllMatches('**/*long*'), None)
        else:
            self.removeOtherParts(head.findAllMatches('**/*short*'), None)
        muzzleParts = head.findAllMatches('**/*muzzle*')
        if(self.data['Animal'] != 'dog'):
            for partNum in range(0, muzzleParts.getNumPaths()):
                part = muzzleParts.getPath(partNum)
                if not 'neutral' in part.getName():
                    part.hide()
        self.removeOtherParts(legs.findAllMatches('**/boots*') + legs.findAllMatches('**/shoes'), None)
        torsoAnims = self.generateAnims(torso=True)
        legsAnims = self.generateAnims(legs=True)
        self.Avatar = Actor({'head' : head, 'torso' : torso, 'legs' : legs}, {'torso' : torsoAnims, 'legs' : legsAnims})
        self.Avatar.attach('head', 'torso', 'def_head')
        self.Avatar.attach('torso', 'legs', 'joint_hips')
        if(self.data['Gender'] == 'girl'):
            femaleEyes = loader.loadTexture('phase_3/maps/eyesFemale.jpg', 'phase_3/maps/eyesFemale_a.rgb')
            try:
                self.Avatar.find('**/eyes').setTexture(femaleEyes, 1)
            except: pass
            try:
                self.Avatar.find('**/eyes-%s' % (self.data['HeadLength'])).setTexture(femaleEyes, 1)
            except: pass
        # Reseat pupils of old head models
        pupils = head.findAllMatches('**/*pupil*')
        for pupil in pupils:
            pupil.setY(0.02)
        self.setColor()
        shadow = ShadowCaster(self.Avatar)
        shadow.initializeDropShadow()
        self.Avatar.setPythonTag("AvatarInstance", self)
        
    def getAvatar(self):
        return self.Avatar
        
        