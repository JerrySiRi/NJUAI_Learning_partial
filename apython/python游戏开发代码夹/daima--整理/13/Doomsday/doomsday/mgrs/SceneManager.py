from direct.showbase.DirectObject import DirectObject
from direct.directnotify import DirectNotifyGlobal

class SceneManager(DirectObject):
    __module__ = __name__
    
    notify = DirectNotifyGlobal.directNotify.newCategory('SceneManager')
    
    def __init__(self):
        self.scenes = []
        
    def createScene(self, name):
        if(render.find('**/' + name)):
            self.notify.warning("Cannot overwrite existing scene.")
            return None
        else:
            scene = Scene(render.attachNewNode(name))
            self.scenes.append(scene)
            return scene
        
    def removeScene(self, name):
        if(render.find('**/' + name)):
            node = render.find('**/' + name).removeNode()
            for scene in self.scenes:
                if(scene.getNode().getName() == name):
                    scene.delete()
                    self.scenes.remove(scene)
                    
class Scene(DirectObject):
    __module__ = __name__
    
    models = []
    
    def __init__(self, node):
        self.node = node
        
    def addModel(self, model):
        model.reparentTo(self.node)
        self.models.append(model)
        
    def getModel(self, name):
        for model in self.models:
            if(model.getName() == name):
                return model
        return None
        
    def removeModel(self, model):
        self.models.remove(model)
        
    def loadScene(self):
        self.node.show()
        
    def unloadScene(self):
        self.node.hide()
        
    def delete(self):
        self.node.removeNode()
        self.models = []
        
    def getNode(self):
        return self.node
        