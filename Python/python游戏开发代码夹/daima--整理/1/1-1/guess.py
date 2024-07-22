import random

guessesTaken = 0

print('你好，你是谁?')
myName = input()

number = random.randint(1, 20)
print('奥, ' + myName + ', 你很年轻啊，年龄1到20之间？')

for guessesTaken in range(6):
    print('猜一猜') # Four spaces in front of "print".
    guess = input()
    guess = int(guess)

    if guess < number:
        print('太小!') # Eight spaces in front of "print"

    if guess > number:
        print('太大！')

    if guess == number:
        break

if guess == number:
    guessesTaken = str(guessesTaken + 1)
    print('厉害 ' + myName + '你猜对了，' + guessesTaken + '很正确!')

if guess != number:
    number = str(number)
    print('别猜了，我年龄是： ' + number + '.')
