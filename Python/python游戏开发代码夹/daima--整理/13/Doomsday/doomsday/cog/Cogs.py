from direct.showbase.DirectObject import DirectObject
from doomsday.cog.Attributes import Attributes
from doomsday.cog.Cog import Cog
from doomsday.cog.Suit import Suit
from doomsday.cog.Head import Head
from doomsday.base import TextureBank
from panda3d.core import VBase4
import copy, random

atr = Attributes()
sales = atr.getDept(0)
money = atr.getDept(1)
legal = atr.getDept(2)
corp = atr.getDept(3)
aSize = atr.getASize()
bSize = atr.getBSize()
cSize = atr.getCSize()

class Cogs(DirectObject):
    
    def __init__(self):
        self.cogs = [
        Cog(name='Flunky', dept=corp, suit=Suit('C', 4 / cSize), 
            head=Head('C', 'flunky', accessory="glasses"), 
            handColor=corp.getHandColor(), height=4.88, 
            minLevel=1, maxLevel=5),
        Cog(name='Pencil Pusher', dept=corp, suit=Suit('B', 3.35 / bSize),
            head=Head('B', 'pencilpusher'), handColor=corp.getHandColor(),
            height=5, minLevel=2, maxLevel=6),
        Cog(name='Yesman', dept=corp, suit=Suit('A', 4.125 / aSize),
            head=Head('A', 'yesman'), handColor=corp.getHandColor(),
            height=5.28, minLevel=3, maxLevel=7),
        Cog(name='Micromanager', dept=corp, suit=Suit('C', 2.5 / cSize),
            head=Head('C', 'micromanager'), handColor=corp.getHandColor(),
            height=5.25, minLevel=4, maxLevel=8),
        Cog(name='Downsizer', dept=corp, suit=Suit('B', 4.5 / bSize),
            head=Head('B', 'beancounter'), handColor=corp.getHandColor(),
            height=6.08, minLevel=5, maxLevel=9),
        Cog(name='Head Hunter', dept=corp, suit=Suit('A', 6.5 / aSize),
            head=Head('A', 'headhunter'), handColor=corp.getHandColor(),
            height=7.45, minLevel=6, maxLevel=10),
        Cog(name='Corporate Raider', dept=corp, suit=Suit('C', 6.75 / cSize),
            head=Head('C', 'tightwad', headTex=TextureBank.getTexture('corporate_raider')), handColor=Attributes().getHandColor('corporate_raider'),
            height=8.23, minLevel=7, maxLevel=11),
        Cog(name='The Big Cheese', dept=corp, suit=Suit('A', 7 / aSize),
            head=Head('A', 'bigcheese'), handColor=Attributes().getHandColor('big_cheese'),
            height=7.34, minLevel=8, maxLevel=12), 
        Cog(name='Bottom Feeder', dept=legal, suit=Suit('C', 4 / cSize), 
            head=Head('C', 'tightwad', headTex=TextureBank.getTexture('bottom_feeder')), 
            handColor=legal.getHandColor(), height=4.81, 
            minLevel=1, maxLevel=5),
        Cog(name='Bloodsucker', dept=legal, suit=Suit('B', 4.375 / bSize),
            head=Head('B', 'movershaker', headTex=TextureBank.getTexture('blood_sucker')), handColor=Attributes().getHandColor('blood_sucker'),
            height=6.17, minLevel=2, maxLevel=6),
        Cog(name='Double Talker', dept=legal, suit=Suit('A', 4.25 / aSize),
            head=Head('A', 'twoface', headTex=TextureBank.getTexture('double_talker')), handColor=legal.getHandColor(),
            height=5.63, minLevel=3, maxLevel=7),
        Cog(name='Ambulance Chaser', dept=legal, suit=Suit('B', 4.35 / bSize),
            head=Head('B', 'ambulancechaser'), handColor=legal.getHandColor(),
            height=6.39, minLevel=4, maxLevel=8),
        Cog(name='Backstabber', dept=legal, suit=Suit('A', 4.5 / aSize),
            head=Head('A', 'backstabber'), handColor=legal.getHandColor(),
            height=6.71, minLevel=5, maxLevel=9),
        Cog(name='Spin Doctor', dept=legal, suit=Suit('B', 5.65 / bSize),
            head=Head('B', 'telemarketer', headTex=TextureBank.getTexture('spin_doctor')), handColor=Attributes().getHandColor('spin_doctor'),
            height=7.9, minLevel=6, maxLevel=10),
        Cog(name='Legal Eagle', dept=legal, suit=Suit('A', 7.125 / aSize),
            head=Head('A', 'legaleagle'), handColor=Attributes().getHandColor('legal_eagle'),
            height=8.27, minLevel=7, maxLevel=11),
        Cog(name='Big Wig', dept=legal, suit=Suit('A', 7 / aSize),
            head=Head('A', 'bigwig'), handColor=legal.getHandColor(),
            height=8.69, minLevel=8, maxLevel=12),
        Cog(name='Short Change', dept=money, suit=Suit('C', 3.6 / cSize), 
            head=Head('C', 'coldcaller'), 
            handColor=money.getHandColor(), height=4.77, 
            minLevel=1, maxLevel=5),
        Cog(name='Penny Pincher', dept=money, suit=Suit('A', 3.55 / aSize),
            head=Head('A', 'pennypincher'), handColor=Attributes().getHandColor('penny_pincher'),
            height=5.26, minLevel=2, maxLevel=6),
        Cog(name='Tightwad', dept=money, suit=Suit('C', 4.5 / cSize),
            head=Head('C', 'tightwad'), handColor=money.getHandColor(),
            height=5.41, minLevel=3, maxLevel=7), 
        Cog(name='Bean Counter', dept=money, suit=Suit('B', 4.4 / bSize),
            head=Head('B', 'beancounter'), handColor=money.getHandColor(),
            height=5.95, minLevel=4, maxLevel=8),
        Cog(name='Number Cruncher', dept=money, suit=Suit('A', 5.25 / aSize),
            head=Head('A', 'numbercruncher', headTex=TextureBank.getTexture("number_cruncher")), handColor=money.getHandColor(),
            height=7.22, minLevel=5, maxLevel=9),
        Cog(name='Money Bags', dept=money, suit=Suit('C', 5.3 / cSize), 
            head=Head('C', 'moneybags'), 
            handColor=money.getHandColor(), height=6.97, 
            minLevel=6, maxLevel=10),
        Cog(name='Loan Shark', dept=money, suit=Suit('B', 6.5 / bSize),
            head=Head('B', 'loanshark'), handColor=Attributes().getHandColor('loan_shark'),
            height=8.58, minLevel=7, maxLevel=11),
        Cog(name='Robber Baron', dept=money, suit=Suit('A', 7 / aSize),
            head=Head('A', 'yesman', headTex=TextureBank.getTexture('robber_baron')), handColor=money.getHandColor(),
            height=8.95, minLevel=8, maxLevel=12),                      
        Cog(name='Cold Caller', dept=sales, suit=Suit('C', 3.5 / cSize), 
            head=Head('C', 'coldcaller', headColor=VBase4(0.25, 0.35, 1.0, 1.0)), 
            handColor=Attributes().getHandColor("cold_caller"), height=4.63, 
            minLevel=1, maxLevel=5),
        Cog(name='Telemarketer', dept=sales, suit=Suit('B', 3.75 / bSize),
            head=Head('B', 'telemarketer'), handColor=sales.getHandColor(),
            height=5.24, minLevel=2, maxLevel=6),
        Cog(name='Name Dropper', dept=sales, suit=Suit('A', 4.35 / aSize),
            head=Head('A', 'numbercruncher', headTex=TextureBank.getTexture("name_dropper")), handColor=sales.getHandColor(),
            height=5.98, minLevel=3, maxLevel=7), 
        Cog(name='Glad Hander', dept=sales, suit=Suit('C', 4.75 / cSize),
            head=Head('C', 'gladhander'), handColor=sales.getHandColor(),
            height=6.4, minLevel=4, maxLevel=8),
        Cog(name='Mover &\nShaker', dept=sales, suit=Suit('B', 4.75 / bSize),
            head=Head('B', 'movershaker'), handColor=sales.getHandColor(),
            height=6.7, minLevel=5, maxLevel=9),
        Cog(name='Two-Face', dept=sales, suit=Suit('A', 5.75 / aSize), 
            head=Head('A', 'twoface'), 
            handColor=sales.getHandColor(), height=7.61, 
            minLevel=6, maxLevel=10),
        Cog(name='The Mingler', dept=sales, suit=Suit('A', 5.75 / aSize),
            head=Head('A', 'twoface', headTex=TextureBank.getTexture("mingler")), handColor=sales.getHandColor(),
            height=7.61, minLevel=7, maxLevel=11),
        Cog(name='Mr. Hollywood', dept=sales, suit=Suit('A', 7.0 / aSize),
            head=Head('A', 'yesman'), handColor=sales.getHandColor(),
            height=8.95, minLevel=8, maxLevel=12),   
        ]
        
    def generateCog(self, name = None, dept = None, level = None, skeleton = False, waiter = False):
        if(name != None):
            for cog in self.cogs:
                if(cog.getName() == name):
                    genCog = copy.copy(cog)
                    genCog.generate(skeleton, waiter)
                    genCog.setLevel(level)
        elif(dept != None):
            availableCogs = []
            for cog in self.cogs:
                if(cog.getDept().getDept() == dept):
                    if(level != None):
                        levelCurve = cog.getLevelCurve()
                        minLevel = levelCurve[0]
                        maxLevel = levelCurve[1]
                        if(minLevel <= level and maxLevel >= level):
                            availableCogs.append(cog)
                    else:
                        availableCogs.append(cog)
            genCog = copy.copy(availableCogs[random.randrange(len(availableCogs))])
            genCog.generate(skeleton, waiter)
        elif(level != None):
            availableCogs = []
            for cog in self.cogs:
                levelCurve = cog.getLevelCurve()
                minLevel = levelCurve[0]
                maxLevel = levelCurve[1]
                if(minLevel <= level and maxLevel >= level):
                    availableCogs.append(cog)
            genCog = copy.copy(availableCogs[random.randrange(len(availableCogs))])
            genCog.setLevel(level)
            genCog.generate(skeleton, waiter)
        else:
            genCog = copy.copy(self.cogs[random.randrange(len(self.cogs))])
            genCog.generate(skeleton, waiter)
        return genCog
    
    def getCogHead(self, cogName):
        for cog in self.cogs:
            if(cog.getName() == cogName):
                hCog = copy.copy(cog)
                hCog.generate()
                head = hCog.getHead()
                hCog.cleanUp()
                del hCog
                return head
            