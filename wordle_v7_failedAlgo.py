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

def importAnswerList():
    answers = []
    with open('answers.txt') as f:
        answers = [line.strip() for line in f]
    answers.sort()
    return answers

def standardLetterFrequency():
    freq = {}
    with open('freq2.txt') as f:
        lines = [line.strip() for line in f]
    for line in lines:
        freq[(line[0]).lower()] = float(line[2:])
    return freq

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

def printInstructions():
    print("Welcome to the Wordle Assistant. After each guess it will return a list of all possible words remaining.")
    print("First, enter in your guess.")
    print("Then, you will enter the result of that guess as a five letter word: \'b\' if the letter at that position was black, \'y\' if the letter at that position was yellow, and \'g\' if the letter at that position was green.")
    print("For example, if your guess result was [black, black, green, green, yellow], then you would input \"bbggy\".")
    print("Capitalization does not matter, the assistant is not case sensitive. If you want to end/escape the program just type \"done\" for your guess. Enjoy!\n")

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

def makeGuess(rec,wordList):
    guess = input("Guess: ").lower()
    if guess == "done":
        print()
        return []
    if guess == "":
        guess = rec
    if len(guess) != WORD_LENGTH:
        print("ERROR: Guess must be 5 letters\n")
        return "",makeGuess()
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
    # guesses.append((guess,result))
    return result,updateWordList(guess,result,wordList)

def recommendGuess(wordList,possRes):
    wordScores = []
    for w in wordList:
        score = []
        for r in possRes:
            l = len(updateWordList(w,r,wordList))
            if l != 0:
                score.append(l)
        wordScores.append((round(statistics.mean(score),4),w))
    wordScores.sort()
    print(wordScores[:5])
    return [w for s,w in wordScores[:min(5,len(wordScores))]]

def main():
    clear()
    printInstructions()
    wordList = importWordList()
    startingGuess = STARTING_GUESS
    # startingGuess = getGuess(fullWordList,possRes)
    # wordList = importAnswerList()
    result = ""
    rec = []
    firstGuess = True
    while len(wordList) > 1:
        if firstGuess:
            rec.append(startingGuess)
            firstGuess = False
        else:
            rec = recommendGuess(wordList,getPossibleResults(result))
        print("Recommended Guesses: " + str(rec))
        result,wordList = makeGuess(rec[0],wordList)
        if len(wordList) == 0:
            print("ERROR: No possible words remaining")
        elif len(wordList) == 1:
            print("\nAnswer: " + wordList[0] + "\n")
        else:
            print(str(wordList) + "\n" + str(len(wordList)) + " words remaining\n")
            # print(str(len(wordList)) + " words remaining\n")



if __name__ == "__main__":
    main()