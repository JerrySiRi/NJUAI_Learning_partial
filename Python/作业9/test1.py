
class keymin(dict):
    def __init__(self,dict1):
        self.dictt=dict1#这个对象的字典
        self.strr='kmin'
    def sorting(self):
        dict2={'kmin':list(sorted(self.dictt.keys())),'kmax':list(reversed(sorted(self.dictt.keys()))),
               'vmin':list(sorted(self.dictt.values())),'vmax':list(reversed(sorted(self.dictt.values())))}
        return dict2[self.strr]

    def ranging(self):
        c=self.sorting()#返回的是一个列表
        d={}
        for i in c:
            d[i]=self.dictt[i]
        print(d)

class keymax(keymin):
    def __init__(self, dict1):
        keymin.__init__(self,dict1)  # 这个对象的字典，通过父类来进行初始化！
        self.strr = 'kmax'

class valuemin(keymin):
    def __init__(self, dict1):
        self.dictt = dict1  # 这个对象的字典
        self.strr = 'vmin'

    def ranging(self):
        c = self.sorting()  # 返回的是一个列表,是值从小到大的排列
        d = {}
        for i in c:
            for j in self.dictt.keys():
                if self.dictt[j]==i:
                    d[j]=i
        print(d)

class valuemax(valuemin):
    def __init__(self, dict1):
        self.dictt = dict1  # 这个对象的字典
        self.strr = 'vmax'

a={1:2,6:5,3:14,8:3}
key1=keymin(a)
key1.ranging()

key2=keymax(a)
key2.ranging()

key3=valuemin(a)
key3.ranging()

key4=valuemax(a)
key4.ranging()

