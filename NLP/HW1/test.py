a = 0.05
decay = 0.99
 
for i in range(300):
    a *= decay
    print(a)