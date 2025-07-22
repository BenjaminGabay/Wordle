from os import system, name

def clear(): 
    if name == 'nt':
        _ = system('cls')   # for windows
    else:
        _ = system('clear') # for mac and linux(here, os.name is 'posix')

def importWordList():
    with open('allowedGuesses.txt') as f:
        wordList = [line.strip() for line in f]
    with open('answers.txt') as f:
        wordList.extend([line.strip() for line in f])
    wordList.sort()
    return wordList

def printInstructions():
    print("Welcome to the Wordle Assistant. After each guess it will return a list of all possible words remaining (some edge cases still in progress).")
    print("First, enter in your guess.")
    print("Then, you will enter the result of that guess as a five letter word: \'b\' if the letter at that position was black, \'y\' if the letter at that position was yellow, and \'g\' if the letter at that position was green.")
    print("For example, if your guess result was [black, black, green, green, yellow], then you would input \"bbggy\".")
    print("Capitalization does not matter, the assistant is not case sensitive. If you want to end/escape the program just type \"done\" for your guess. Enjoy!\n")

def updateWordList(guess, result, wordList):
    greenLettersLoc = [(i, guess[i]) for i in range(5) if result[i] == 'g']
    yellowLettersLoc = [(i, guess[i]) for i in range(5) if result[i] == 'y']
    greenLetters = [l for i,l in greenLettersLoc]
    yellowLetters = [l for i,l in yellowLettersLoc]
    blackLetters = [guess[i] for i in range(5) if result[i] == 'b']
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
    return wordList

def main():
    clear()
    printInstructions()
    wordList = importWordList()
    guesses = []

    while len(wordList) > 1:
        guess = input("Guess: ").lower()
        if guess == "done":
            print()
            return
        elif len(guess) == 5:
            if guess not in wordList:
                print("WARNING: Guess is not in remaining word list. Type \"back\" in result input to guess again")
            result = input("Result: ").lower()
            if result == "back":
                print("FIXME")
            if len(result) == 5:
                valid = True
                for r in result:
                    if r != 'b' and r != 'y' and r != 'g':
                        valid = False
                        print("ERROR: Invalid result letter \'" + r +"\'. Terminating...Please restart.\n")
                        print("FIXME")
                        return
                if valid:
                    guesses.append((guess,result))
                    wordList = updateWordList(guess, result, wordList)
                    if len(wordList) == 0:
                        print("ERROR: No possible words remaining")
                        return
                    if len(wordList) == 1:
                        print()
                        break
                    print(str(wordList) + "\n" + str(len(wordList)) + "\n")
            else:
                print("ERROR: Result must be 5 letters\n")
        else:
            print("ERROR: Guess must be 5 letters\n")
    # print(guesses)
    print("Answer: " + wordList[0] + "\n")


if __name__ == "__main__":
    main()