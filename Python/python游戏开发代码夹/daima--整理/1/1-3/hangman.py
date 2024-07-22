import random
HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\  |
 / \  |
     ===''']
words = 'dog monkey chick hourse girl boy money'.split()

def getRandomWord(wordList):
    # 此函数从传递的字符串列表返回一个随机字符串。.
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]

def displayBoard(missedLetters, correctLetters, secretWord):
    print(HANGMAN_PICS[len(missedLetters)])
    print()

    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)): # 用正确的猜测字母替换空白
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks: # 在每个字母之间用空格显示秘密单词
        print(letter, end=' ')
    print()

def getGuess(alreadyGuessed):
    # 返回玩家输入的字母，这个功能确保玩家进入一个字母，而不是其他东西。
    while True:
        print('猜一个字母.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('请输入一个字母.')
        elif guess in alreadyGuessed:
            print('你已经猜到那个字母了，请继续!')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('请输入一个字母 ')
        else:
            return guess

def playAgain():
    # 如果玩家想继续玩，此函数返回true；否则，返回false .
    print('你还继续玩吗? (yes or no)')
    return input().lower().startswith('y')


print('H A N G M A N 游 戏')
missedLetters = ''
correctLetters = ''
secretWord = getRandomWord(words)
gameIsDone = False

while True:
    displayBoard(missedLetters, correctLetters, secretWord)

    # 让玩家输入一个字母
    guess = getGuess(missedLetters + correctLetters)

    if guess in secretWord:
        correctLetters = correctLetters + guess
        # 检查玩家是否赢了.
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetters = False
                break
        if foundAllLetters:
            print('是的，这个字母是"' + secretWord + '"! 我赢了!')
            gameIsDone = True
    else:
        missedLetters = missedLetters + guess

        # 检查玩家是否猜多次猜错 .
        if len(missedLetters) == len(HANGMAN_PICS) - 1:
            displayBoard(missedLetters, correctLetters, secretWord)
            print('你已经猜不对了!' + str(len(missedLetters)) + ' 猜错了' + str(len(correctLetters)) + ' 猜对了，这个单词是"' + secretWord + '"')
            gameIsDone = True

    # 但如果游戏完成，询问玩家是否想再玩一次。
    if gameIsDone:
        if playAgain():
            missedLetters = ''
            correctLetters = ''
            gameIsDone = False
            secretWord = getRandomWord(words)
        else:
            break
