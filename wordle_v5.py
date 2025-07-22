from os import system, name

from numpy import sort

WORD_LENGTH = 5
wordList = []
guesses = []

def clear(): 
    if name == 'nt':
        _ = system('cls')   # for windows
    else:
        _ = system('clear') # for mac and linux(here, os.name is 'posix')

def importWordList():
    global wordList
    with open('wordList.txt') as f:
        wordList = [line.strip() for line in f]
    wordList.sort()

def printInstructions():
    print("Welcome to the Wordle Assistant. After each guess it will return a list of all possible words remaining.")
    print("First, enter in your guess.")
    print("Then, you will enter the result of that guess as a five letter word: \'b\' if the letter at that position was black, \'y\' if the letter at that position was yellow, and \'g\' if the letter at that position was green.")
    print("For example, if your guess result was [black, black, green, green, yellow], then you would input \"bbggy\".")
    print("Capitalization does not matter, the assistant is not case sensitive. If you want to end/escape the program just type \"done\" for your guess. Enjoy!\n")

def updateWordList(guess, result):
    global wordList
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
    # ybgLetters = [l for l in blackLetters if l in yellowLetters and l in greenLetters]
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

def makeGuess(rec):
    guess = input("Guess: ").lower()
    if guess == "done":
        print()
        return True
    if guess == "":
        guess = rec
    if len(guess) != WORD_LENGTH:
        print("ERROR: Guess must be 5 letters\n")
        return makeGuess()
    if guess not in wordList:
        print("WARNING: Guess is not in remaining word list. Type \"back\" in result input to guess again")
    result = input("Result: ").lower()
    if result == "back":
        return makeGuess()
    if len(result) != WORD_LENGTH:
        print("ERROR: Result must be 5 letters\n")
        return makeGuess()
    for r in result:
        if r != 'b' and r != 'y' and r != 'g':
            print("ERROR: Invalid result letter \'" + r +"\'\n")
            return makeGuess()
    guesses.append((guess,result))
    updateWordList(guess, result)
    return False



def recommendGuess():
    global wordList
    global guesses
    # print(wordList)
    # print(guesses)
    # letterFreq = [0] * 26
    # letterFreq = [[chr(l+97), 0] for l in range(26)]
    # print(letterFreq)
    letterFreq = {}
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
    # print(letterFreq)
    # print(sum(letterFreq.values()))
    sumVal = sum(letterFreq.values())
    for x in letterFreq:
        letterFreq[x] = float(letterFreq[x]) / sumVal
    # print(letterFreq)
    wordScores = []
    for w in wordList:
        score = 0
        for i in range(WORD_LENGTH):
            l = w[i]
            n = w.count(l)
            if n > 1:
                score += letterLocFreq[i][l*n] / n * letterFreq[l*n]
                score += letterLocFreq[i][l] / n * letterFreq[l]
            else:
                score += letterLocFreq[i][l] * letterFreq[l]
        wordScores.append((score,w))

    # print(letterLocFreq)
    # print(letterFreq)
    # print(guessL)
    wordScores.sort(reverse=True)
    # print(guessL)
    # print(wordScores[:5])
    wordScores = [(round(s,2),w) for s,w in wordScores]
    print(wordScores[:5])
    return [w for s,w in wordScores[:min(5,len(wordScores))]]

def main():
    clear()
    printInstructions()
    importWordList()
    done = False
    while not done:
        rec = recommendGuess()
        print("Recommended Guesses: " + str(rec))
        done = makeGuess(rec[0])
        if not done:
            if len(wordList) == 0:
                print("ERROR: No possible words remaining")
                done = True
            elif len(wordList) == 1:
                print("\nAnswer: " + wordList[0] + "\n")
                done = True
            else:
                print(str(wordList) + "\n" + str(len(wordList)) + " words remaining\n")



if __name__ == "__main__":
    main()