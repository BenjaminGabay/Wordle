from os import system, name

def clear(): 
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def updateWordList(guess, result, wordList):
    # blackLetters = []
    # yellowLetters = []
    greenLetters = []
    for i in range(5):
        if result[i] == 'g':
            greenLetters.append(guess[i])
    newWordList = []
    for i in range(5):
        l = guess[i]
        r = result[i]
        newWordList.clear()
        if r != 'b' and r != 'y' and r != 'g':
            print("ERROR: Invalid result letter \'" + r +"\'")
            return newWordList
        if r == 'g':
            newWordList = [word for word in wordList if word[i] == l]
        else:
            for word in wordList:
                if r == 'y':
                    for j in range(5):
                        if word[j] == l and i != j:
                            newWordList.append(word)
                            break
                elif r == 'b' and greenLetters.count(l) == 0:
                    valid = True
                    for j in range(5):
                        if word[j] == l:
                            valid = False
                            break
                    if valid:
                        newWordList.append(word)
                else:
                    newWordList = wordList
        wordList = newWordList.copy()
        # print(wordList)
    return wordList

clear()

wordList = []
with open('allowedGuesses.txt') as f:
    wordList = [line.strip() for line in f]
with open('answers.txt') as f:
    wordList.extend([line.strip() for line in f])
wordList.sort()

print("Welcome to the Wordle Assistant. After each guess it will return a list of all possible words remaining (some edge cases still in progress).")
print("First, enter in your guess.")
print("Then, you will enter the result of that guess as a five letter word: \'b\' if the letter at that position was black, \'y\' if the letter at that position was yellow, and \'g\' if the letter at that position was green.")
print("For example, if your guess result was [black, black, green, green, yellow], then you would input \"bbggy\".")
print("Capitalization does not matter, the assistant is not case sensitive. If you want to end/escape the program just type \"done\" for your guess. Enjoy!\n")

while len(wordList) > 1:
    guess = input("Guess: ").lower()
    if guess == "done":
        break
    elif len(guess) == 5:
        result = input("Result: ").lower()
        if len(result) == 5:
            wordList = updateWordList(guess, result, wordList)
            if len(wordList) == 0:
                wordList.append("ERROR-Please Restart")
                break
            print(wordList)
            print()
        else:
            print("ERROR: Result must be 5 letters")
    else:
        print("ERROR: Guess must be 5 letters")
if len(wordList) == 1:
    print("Answer: " + wordList[0] + "\n")