from os import system, name
from numpy import sort
import statistics

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

def importAnswerList():
    answers = []
    with open('answers.txt') as f:
        answers = [line.strip() for line in f]
    answers.sort()
    return answers

def getPossibleResults():
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
    return possRes

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

def getGuess(wordList):
    posRes = getPossibleResults()
    wordScores = []
    for w in wordList:
        score = []
        for r in posRes:
            l = len(updateWordList(w,r,wordList))
            if l != 0:
                score.append(l)
        wordScores.append((round(statistics.mean(score),4),w))
    wordScores.sort()
    print(wordScores[:5])
    return [w for s,w in wordScores[:min(5,len(wordScores))]]
    
    
    
    
    # posRes = getPossibleResults()
    # wordScores = []
    # for w in wordList:
    #     # score = 0
    #     score = []
    #     # score = set()
    #     for r in posRes:
    #         l = len(updateWordList(w,r,wordList))
    #         if l != 0:
    #             score.append(l)
    #         # if score == 0:
    #         #     score = len(updateWordList(w,r,wordList))
    #         # else:
    #         #     score = (score + len(updateWordList(w,r,wordList))) / 2
    #         # score.update(updateWordList(w,r,wordList))
    #         # print(score)
    #     # wordScores.append((statistics.median(score),round(statistics.mean(score),2),w))
    #     wordScores.append((round(statistics.mean(score),4),w))
        
    #     # print(w + " - " + str(len(score)))
    # wordScores.sort()
    # # print(wordScores)
    # # maxScore = wordScores[0][0]
    # f = open("test3.txt", "w")
    # for s1,s2,w in wordScores:
    #     # f.write(w + " - " + str(s) + " - " + str(round(float(s)/maxScore,4)) + "\n")
    #     f.write(w + " - " + str(s1) + " - " + str(s2) + "\n")
    # f.close()
    # # wordScores = [(round(float(s)/maxScore,4),w) for s,w in wordScores]

    # # sumVal = sum(letterFreq.values())
    # # # for x in letterFreq:
    # # letterFreq[x] = float(letterFreq[x]) / sumVal
    # # print(wordScores[:5])
    # return [w for s1,s2,w in wordScores[:min(5,len(wordScores))]]
    # return wordScores[0][1]


    # letterFreq = standardLetterFrequency()
    # letterLocFreq = [{},{},{},{},{}]
    # for w in wordList:
    #     for i in range(WORD_LENGTH):
    #         l = w[i]
    #         n = w.count(l)
    #         if n > 1:
    #             if l*n not in letterLocFreq[i]:
    #                 letterLocFreq[i][l*n] = 0.0
    #             letterLocFreq[i][l*n] += 1.0
    #             if l*n not in letterFreq:
    #                 letterFreq[l*n] = 0.0
    #             letterFreq[l*n] += 1.0 / n
    #         if l not in letterLocFreq[i]:
    #             letterLocFreq[i][l] = 0
    #         letterLocFreq[i][l] += 1
    #         if l not in letterFreq:
    #             letterFreq[l] = 0
    #         letterFreq[l] += 1
    # sumVal = sum(letterFreq.values())
    # for x in letterFreq:
    #     letterFreq[x] = float(letterFreq[x]) / sumVal
    # wordScores = []
    # for w in wordList:
    #     score = 0
    #     numVow = 0
    #     for l in w:
    #         if l in VOWELS:
    #             numVow += 1
    #     for i in range(WORD_LENGTH):
    #         l = w[i]
    #         n = w.count(l)
    #         if n > 1:
    #             score += letterLocFreq[i][l*n] / n * letterFreq[l*n]
    #             score += letterLocFreq[i][l] / n * letterFreq[l]
    #         elif l in VOWELS:
    #             score += letterLocFreq[i][l] * letterFreq[l] / max(1,numVow-1)
    #         else:
    #             score += letterLocFreq[i][l] * letterFreq[l]
    #     wordScores.append((score,w))

    # wordScores.sort(reverse=True)
    # return wordScores[0][1]

def main():
    # clear()
    # fullWordList = importWordList()
    fullWordList = importAnswerList()
    # getPossibleResults()
    print("Recommended Guesses: " + str(getGuess(fullWordList)))


    # answers = importAnswerList()

    # totalGuesses = 0
    # count = 0
    # # for a in answers[:5]:
    # for a in answers:
    #     wordList = fullWordList.copy()
    #     guesses = []
    #     count = 0
    #     while len(wordList) > 1:
    #         count += 1
    #         guess = getGuess(wordList)
    #         if guess != a:
    #             result = getResult(guess,a)
    #             guesses.append((guess,result))
    #             # print("     " + guess + "     " + str(result))
    #             wordList = updateWordList(guess,result,wordList)
    #             if len(wordList) ==  1:
    #                 count += 1
    #         else:
    #             wordList = [a]
        
    #     # print(str(count) + " - " + a)
    #     if count > 6:
    #         # print(str(count) + " - " + a + " - " + str(guesses))
    #         print(str(count) + " - " + a)
    #     totalGuesses += count
    
    # # print("Average Guesses: " + str(float(totalGuesses) / 5))
    # print("Average Guesses: " + str(round(float(totalGuesses) / len(answers),4)))

# def getResult(guess,answer):
#     result = ['','','','','']
#     for i in range(WORD_LENGTH):
#         if guess[i] == answer[i]:
#             result[i] = 'g'            
#         elif guess[i] in answer:
#             result[i] = 'y'
#         else:
#             result[i] = 'b'
#     temp = ""
#     for i in range(WORD_LENGTH):
#         if result[i] != 'g':
#             temp += answer[i]
#     for i in range(WORD_LENGTH):
#         if result[i] == 'y' and guess[i] not in temp:
#             result[i] = 'b'
#         else:
#             temp = temp.replace(guess[i],'',1)
#     r = ""
#     for x in result:
#         r += x
#     return r


if __name__ == "__main__":
    main()