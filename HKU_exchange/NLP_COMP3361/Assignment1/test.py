
a=[('a',2),('b',1)]
def list_sort(item):
    return item[1]
a.sort(key=list_sort)
print(a)