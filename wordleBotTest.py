from os import system, name

from numpy import sort

WORD_LENGTH = 5
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

def getGuess(wordList):
    letterFreq = standardLetterFrequency()
    # letterFreq = {}
    letterLocFreq = [{},{},{},{},{}]
    for w in wordList:
        for i in range(WORD_LENGTH):
            l = w[i]
            n = w.count(l)
            if n > 1:
                if l*n not in letterLocFreq[i]:
                    letterLocFreq[i][l*n] = 0.0
                letterLocFreq[i][l*n] += 1.0
                if l*n not in letterFreq:
                    letterFreq[l*n] = 0.0
                letterFreq[l*n] += 1.0 / n
            if l not in letterLocFreq[i]:
                letterLocFreq[i][l] = 0
            letterLocFreq[i][l] += 1
            if l not in letterFreq:
                letterFreq[l] = 0
            letterFreq[l] += 1
    sumVal = sum(letterFreq.values())
    for x in letterFreq:
        letterFreq[x] = float(letterFreq[x]) / sumVal
    wordScores = []
    for w in wordList:
        score = 0
        numVow = 0
        for l in w:
            if l in VOWELS:
                numVow += 1
        for i in range(WORD_LENGTH):
            l = w[i]
            n = w.count(l)
            if n > 1:
                score += letterLocFreq[i][l*n] / n * letterFreq[l*n]
                score += letterLocFreq[i][l] / n * letterFreq[l]
            elif l in VOWELS:
                score += letterLocFreq[i][l] * letterFreq[l] / max(1,numVow-1)
                # score += letterLocFreq[i][l] * letterFreq[l] / numVow
            else:
                score += letterLocFreq[i][l] * letterFreq[l]
        wordScores.append((score,w))

    wordScores.sort(reverse=True)
    # wordScores = [(round(s,2),w) for s,w in wordScores]
    # return [w for s,w in wordScores[:min(5,len(wordScores))]]
    return wordScores[0][1]

def main():
    # clear()
    fullWordList = importWordList()
    answer = input("Answer: ").lower()
    count = 0
    wordList = fullWordList.copy()
    while len(wordList) > 1:
        count += 1
        guess = getGuess(wordList)
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