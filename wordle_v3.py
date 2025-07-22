from os import system, name

WORD_LENGTH = 5
# wordList = []
guesses = []

def clear(): 
    if name == 'nt':
        _ = system('cls')   # for windows
    else:
        _ = system('clear') # for mac and linux(here, os.name is 'posix')

def importWordList():
    global wordList
    with open('allowedGuesses.txt') as f:
        wordList = [line.strip() for line in f]
    with open('answers.txt') as f:
        wordList.extend([line.strip() for line in f])
    wordList.sort()
    # return wordList

def printInstructions():
    print("Welcome to the Wordle Assistant. After each guess it will return a list of all possible words remaining (some edge cases still in progress).")
    print("First, enter in your guess.")
    print("Then, you will enter the result of that guess as a five letter word: \'b\' if the letter at that position was black, \'y\' if the letter at that position was yellow, and \'g\' if the letter at that position was green.")
    print("For example, if your guess result was [black, black, green, green, yellow], then you would input \"bbggy\".")
    print("Capitalization does not matter, the assistant is not case sensitive. If you want to end/escape the program just type \"done\" for your guess. Enjoy!\n")

# def updateWordList(guess, result, wordList):
def updateWordList(guess, result):
    global wordList
    greenLettersLoc = [(i, guess[i]) for i in range(WORD_LENGTH) if result[i] == 'g']
    yellowLettersLoc = [(i, guess[i]) for i in range(WORD_LENGTH) if result[i] == 'y']
    greenLetters = [l for i,l in greenLettersLoc]
    yellowLetters = [l for i,l in yellowLettersLoc]
    blackLetters = [guess[i] for i in range(WORD_LENGTH) if result[i] == 'b']
    ygLetters = [l for l in yellowLetters if l in greenLetters]
    bgLetters = [l for l in blackLetters if l in greenLetters]
    blackOnlyLetters = [l for l in blackLetters if l not in greenLetters]
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
    # return wordList

def makeGuess():
    guess = input("Guess: ").lower()
    if guess == "done":
        print()
        # return []
        return True
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
    # wordList = updateWordList(guess, result, wordList)
    updateWordList(guess, result)
    # return wordList
    return False

def reccomendGuess(wordList):
    return ""

def main():
    clear()
    printInstructions()
    importWordList()

    done = False

    while not done:
        done = makeGuess()
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