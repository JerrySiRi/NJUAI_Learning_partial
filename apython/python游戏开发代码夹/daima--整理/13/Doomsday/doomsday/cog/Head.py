from direct.showbase.DirectObject import DirectObject

class Head(DirectObject):
    
    def __init__(self, headBank, head, headTex=None, headColor=None, accessory=None):
        self.headBank = headBank
        self.head = head
        self.headTex = headTex
        self.headColor = headColor
        self.accessory = accessory
        self.headObj = None
        
        if(self.head == 'flunky'):
            print("Received this accessory: %s." % (self.accessory))
        
    def generate(self, accessory=None):
        heads = loader.loadModel('phase_4/models/char/suit%s-heads.bam' % (self.headBank))
        self.headObj = heads.find('**/' + self.head)
        self.headObj.setName("Head")
        if(accessory != None):
            self.accessory = heads.find('**/%s' % (accessory))
            if(self.accessory.isEmpty() == False):
                self.accessory.reparentTo(self.headObj)
        if(self.headTex != None):
            self.headObj.setTexture(loader.loadTexture(self.headTex), 1)
        if(self.headColor != None):
            self.headObj.setColor(self.headColor)
        heads.removeNode()
        return self.headObj
    
    def attemptAccessoryFix(self):
        heads = loader.loadModel('phase_4/models/char/suit%s-heads.bam' % (self.headBank))
        if(self.accessory != None):
            self.accessory = heads.find('**/%s' % (self.accessory))
            if(self.accessory.isEmpty() == False):
                self.accessory.reparentTo(self.headObj)
        if(self.headObj.getChildren().size() == 0):
            print("Still cannot fix accessory?")
            print("Accessory: %s." % (self.accessory))
        heads.removeNode()
        
    def getAccessory(self):
        return self.accessory
    
    def hasAccessory(self):
        if(self.accessory != None):
            return True
        else:
            return False
        
    def getHead(self):
        return self.headObj
        