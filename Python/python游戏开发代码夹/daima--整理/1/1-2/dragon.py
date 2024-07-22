import random
import time

def displayIntro():
    print('''这里是龙的世界，龙在洞穴中装满了宝藏。有些龙很友善，愿意与你分享宝藏。
而另外一些龙则很凶残，会吃掉闯入它们的洞穴的任何人。玩家站在两个洞前，一个山洞住着友善的龙，
另一个山洞住着饥饿的龙。玩家必须从这两个山洞之间选择一个。''')
    print()

def chooseCave():
    cave = ''
    while cave != '1' and cave != '2':
        print('你选择进入哪个洞穴？ ? (1 or 2)')
        cave = input()

    return cave

def checkCave(chosenCave):
    print('你正在慢慢的靠近这个山洞...')
    time.sleep(2)
    print('十分黑暗、阴暗，一片混沌 ...')
    time.sleep(2)
    print('突然一条巨龙跳了出来，他张开了大大的嘴巴 ...')
    print()
    time.sleep(2)

    friendlyCave = random.randint(1, 2)

    if chosenCave == str(friendlyCave):
         print('然后充满微笑的给你他的宝藏!')
    else:
         print('然后一口把你吃掉!')

playAgain = 'yes'
while playAgain == 'yes' or playAgain == 'y':
    displayIntro()
    caveNumber = chooseCave()
    checkCave(caveNumber)

    print('你还想再玩一次吗？ (yes or no)')
    playAgain = input()
