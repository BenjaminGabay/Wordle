from os import system, name
from numpy import sort
import statistics

WORD_LENGTH = 5
STARTING_GUESS = "tares"
VOWELS = "aeiou"
CONS = "qwrtypsdfghjklzxcvbnm"

def clear(): 
    if name == 'nt':
        _ = system('cls')   # for windows
    else:
        _ = system('clear') # for mac and linux(here, os.name is 'posix')

def importWordList():
    wordList = []
    with open('wordList.txt') as f:
        wordList = [line.strip() for line in f]
    wordList.sort()
    return wordList

def getPossibleResults(prevRes=''):
    possRes = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    for m in range(3):
                        res = ""
                        if i == 0:
                            res += 'b'
                        if i == 1:
                            res += 'y'
                        if i == 2:
                            res += 'g'
                        if j == 0:
                            res += 'b'
                        if j == 1:
                            res += 'y'
                        if j == 2:
                            res += 'g'
                        if k == 0:
                            res += 'b'
                        if k == 1:
                            res += 'y'
                        if k == 2:
                            res += 'g'
                        if l == 0:
                            res += 'b'
                        if l == 1:
                            res += 'y'
                        if l == 2:
                            res += 'g'
                        if m == 0:
                            res += 'b'
                        if m == 1:
                            res += 'y'
                        if m == 2:
                            res += 'g'
                        possRes.append(res)
    for i in [i for i in range(WORD_LENGTH) if prevRes[i] == 'g']:
        possRes = [r for r in possRes if r[i] == 'g']
    return possRes

def standardLetterFrequency():
    freq = {}
    with open('freq2.txt') as f:
        lines = [line.strip() for line in f]
    for line in lines:
        freq[(line[0]).lower()] = float(line[2:])
    return freq

def updateWordList(guess, result, wordList):
    greenLettersLoc = [(i, guess[i]) for i in range(WORD_LENGTH) if result[i] == 'g']
    yellowLettersLoc = [(i, guess[i]) for i in range(WORD_LENGTH) if result[i] == 'y']
    blackLettersLoc = [(i, guess[i]) for i in range(WORD_LENGTH) if result[i] == 'b']
    greenLetters = [l for i,l in greenLettersLoc]
    yellowLetters = [l for i,l in yellowLettersLoc]
    blackLetters = [l for i,l in blackLettersLoc]
    blackOnlyLetters = [l for l in blackLetters if l not in greenLetters and l not in yellowLetters]
    ygLetters = [l for l in yellowLetters if l in greenLetters]
    bgLetters = [l for l in blackLetters if l in greenLetters]
    ybLetters = [l for l in blackLetters if l in yellowLetters]
    for i,l in greenLettersLoc:
        wordList = [word for word in wordList if word[i] == l]
    for i,l in yellowLettersLoc:
        wordList = [word for word in wordList if l in word and word[i] != l]
    for l in ygLetters:
        wordList = [word for word in wordList if word.count(l) > 1]
    for l in blackOnlyLetters:
        wordList = [word for word in wordList if l not in word]
    for l in bgLetters:
        wordList = [word for word in wordList if word.count(l) == greenLetters.count(l)]
    for i,l in blackLettersLoc:
        if l in ybLetters:
            wordList = [word for word in wordList if word.count(l) == (yellowLetters.count(l)+greenLetters.count(l)) and word[i] != l]
    return wordList

def getResult(guess,answer):
    result = ['','','','','']
    for i in range(WORD_LENGTH):
        if guess[i] == answer[i]:
            result[i] = 'g'            
        elif guess[i] in answer:
            result[i] = 'y'
        else:
            result[i] = 'b'
    temp = ""
    for i in range(WORD_LENGTH):
        if result[i] != 'g':
            temp += answer[i]
    for i in range(WORD_LENGTH):
        if result[i] == 'y' and guess[i] not in temp:
            result[i] = 'b'
        else:
            temp = temp.replace(guess[i],'',1)
    r = ""
    for x in result:
        r += x
    return r

def getGuess(wordList,possRes):
    wordScores = []
    for w in wordList:
        score = []
        for r in possRes:
            l = len(updateWordList(w,r,wordList))
            if l != 0:
                score.append(l)
        if len(score) > 0:
            wordScores.append((round(statistics.mean(score),4),w))
    wordScores.sort()
    return wordScores[0][1]

def main():
    # clear()
    fullWordList = importWordList()
    answer = input("Answer: ").lower()
    # possRes = getPossibleResults()
    startingGuess = STARTING_GUESS
    # startingGuess = getGuess(fullWordList,possRes)
    count = 0
    guess = ""
    result = ""
    wordList = fullWordList.copy()
    firstGuess = True
    while len(wordList) > 1:
        count += 1
        if firstGuess:
            guess = startingGuess
            firstGuess = False
        else:
            guess = getGuess(wordList,getPossibleResults(result))
        if guess != answer:
            result = getResult(guess,answer)
            print("     " + guess + "     " + str(result))
            wordList = updateWordList(guess,result,wordList)
            if len(wordList) ==  1:
                count += 1
        else:
            wordList = [answer]
    print(str(count) + " - " + answer)


if __name__ == "__main__":
    main()