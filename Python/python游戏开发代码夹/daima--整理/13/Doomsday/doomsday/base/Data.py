from direct.showbase.DirectObject import DirectObject
import configparser
from panda3d.core import VBase3

class Data(DirectObject):
        
    def saveGame(self):
        Toon = render.find('**/Toon')
        if(Toon != None):
            self.saveAvatar(Toon)
    
    def saveAvatar(self, toon):
        avatar = toon.getPythonTag("AvatarInstance")
        localAvatar = avatar.getAvatar()
        config = configparser.RawConfigParser()
        config.add_section('Avatar')
        config.set('Avatar', 'X', str(localAvatar.getX()))
        config.set('Avatar', 'Y', str(localAvatar.getY()))
        config.set('Avatar', 'Z', str(localAvatar.getZ()))
        config.set('Avatar', 'H', str(localAvatar.getH()))
        config.set('Avatar', 'P', str(localAvatar.getP()))
        config.set('Avatar', 'R', str(localAvatar.getR()))
        for key in avatar.getData().keys():
            print(key)
            if(avatar.getData()[key] != None):
                config.set('Avatar', key, str(avatar.getData()[key]))        
        #config.add_section('Gag')
        with open('data.ini', 'w') as configFile:
            config.write(configFile)
            
    def loadAvatar(self):
        config = configparser.ConfigParser()
        config.read('data.ini')
        pos = VBase3(float(config.get('Avatar', 'X')), float(config.get('Avatar', 'Y')), float(config.get('Avatar', 'Z')))
        hpr = VBase3(float(config.get('Avatar', 'H')), float(config.get('Avatar', 'P')), float(config.get('Avatar', 'R')))
        """
        ToonData = {'Animal' : None, 'Gender' : None, 'Weight' : None, 'Height' : None,
        'Color' : None, 'HeadType' : None, 'HeadLength' : None}
        
        for key in ToonData.keys()):
            ToonData[key] = config.get('Avatar', key)
            print ToonData[key]
        """
        
        
                