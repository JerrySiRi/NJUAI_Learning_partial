a = [1,2,3]
b = [4,5,6]
temp = list(zip(a,b))
temp_1 = [(1,4),(2,5),(3,6)]
x,y = zip(*temp_1)
print(list(y))