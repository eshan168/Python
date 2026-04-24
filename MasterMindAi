# Average turns: 4.394290123456754

import sys
import math
import time

colors = ["R", "O", "Y", "G", "B", "P"]
colorsToNumbers = {"R":0, "O":1, "Y":2, "G":3, "B":4, "P":5}
numbersToColors = {0:"R", 1:"O", 2:"Y", 3:"G", 4:"B", 5:"P"}

# Get list of all possible codes
possibleCodes = []
for num in range(1296):
    temp = []
    remaining = num
    while remaining > 0:
        temp.append(remaining % 6)
        remaining //= 6
    temp += [0] * (4-len(temp))
    possibleCodes.append(temp)

# Amount of possible codes left
remainingCodes = possibleCodes.copy()

# Hash map of each possible code to get faster responses
possibleCodesHash = []
for code in possibleCodes:
    hashMap = {}
    for color in code:
        if color in hashMap:
            hashMap[color] += 1
        else:
            hashMap[color] = 1
    possibleCodesHash.append(hashMap)

# For putting colors in the terminal
red = "\033[31mR"+"\033[0m"
orange = "\033[38;5;208mO"+"\033[0m"
yellow = "\033[33mY"+"\033[0m"
green = "\033[32mG"+"\033[0m"
blue = "\033[34mB"+"\033[0m"
purple = "\033[35mP"+"\033[0m"

positionAndColor = "\033[92mX"+"\033[0m"
colorOnly = "\033[93mX"+"\033[0m"
noPositonOrColor = "\033[90mX"+"\033[0m"

colorKey = {"R":red, "O":orange, "Y":yellow, "G":green, "B":blue, "P":purple}
responseKey = {0:noPositonOrColor, 1:colorOnly, 2:positionAndColor}

stringCode = ""
numberCode = []
cracked = False


def clearLines(lines: int):
    for line in range(lines):
        sys.stdout.write('\033[A')
        sys.stdout.write('\033[K')

def blankLines(lines: int):
    print("\n" * lines)

def colorCode(code):
    colorCode = " "
    for color in code:
        if isinstance(code, list):
            colorCode += colorKey[numbersToColors[color]]+" "
        else:
            colorCode += colorKey[color]+" "
    return colorCode

def colorResponse(response: str):
    coloredResponse = " "
    for color in response:
        coloredResponse += responseKey[color]+" "
    return coloredResponse

def baseSix(number: list):
    return 216*number[0] + 36*number[1] + 6*number[2] + number[3]

def baseThree(number: list):
    return 27*number[0] + 9*number[1] + 3*number[2] + number[3]

def getBits(probability: float):
    if (probability == 0):
        return 0
    return math.log2(1/probability)

def getUserCode():
    global stringCode

    stringCode = ""
    validCode = False

    while not validCode:
        validCode = True
        stringCode = input("Enter Code: ").strip().upper()
        if len(stringCode) != 4:
            validCode = False
        for color in stringCode:
            if color not in colors:
                validCode = False
        clearLines(1)
    
    for color in stringCode:
        numberCode.append(colorsToNumbers[color])

# Return feedback given a code and a guess
def getFeedback(code:list, possibleMatch:list):
    response = []
    codeHash = possibleCodesHash[baseSix(code)].copy()
    
    for i in range(len(code)):
        if possibleMatch[i] == code[i]:
            response.append(2)
            codeHash[possibleMatch[i]] -= 1
    
    for i in range(len(code)):
        if possibleMatch[i] in code and codeHash[possibleMatch[i]] > 0:
            response.append(1)
            codeHash[possibleMatch[i]] -=1

    response += [0] * (4-len(response))
    return response

# Looks at all possible guesses and chooses the one that reduces the remaining possibilities the most
# Goes through all the possible feedback patterns for each guess and calculates the average information gained
def computerGuess():
    bestGuess = [0,0,0,0]
    maxInformation = 0

    for guess in possibleCodes:

        feedbackDistribution = [0] * 81
        meanInformation = 0

        for response in remainingCodes:
            feedbackDistribution[baseThree(getFeedback(guess,response))] += 1

        for feedback in feedbackDistribution:
            meanInformation += feedback/len(remainingCodes) * getBits(feedback/len(remainingCodes))
        
        if guess in remainingCodes:
            meanInformation += 1/len(remainingCodes)
        
        if meanInformation > maxInformation:
            bestGuess = guess
            maxInformation = meanInformation
    
    return bestGuess
    
def filterRemainingCodes(guess: list, feedback: list):
    global remainingCodes

    newRemainingCodes = []
    for code in remainingCodes:
        if getFeedback(code,guess) == feedback:
            newRemainingCodes.append(code)
    
    remainingCodes = newRemainingCodes

def playGame():
    print(f"Red: {red} \nOrange: {orange} \nYellow: {yellow} \nGreen: {green} \nBlue: {blue} \nPurple: {purple} \n")
    getUserCode()

    print(f"Code: {colorCode(stringCode)}\n")
    print(f"Color and position correct: {positionAndColor} \nWrong position but color is in code: {colorOnly} \nWrong color and position: {noPositonOrColor}\n")

    for guesses in range(10):
        print("")
        
        if guesses == 0:
            clearLines(0)
        else:
            time.sleep(0.5)

        guess = computerGuess()
        feedback = getFeedback(numberCode,guess)
        filterRemainingCodes(guess,feedback)

        clearLines(1)
        print(f"|{colorCode(guess)}|   |{colorResponse(feedback)}|")

        # check is code is correct
        if sum(feedback) >= 8:
            break

    print("\nCode Cracked!\n")

    resetGame()

def resetGame():
    global stringCode,numberCode,cracked,remainingCodes

    stringCode = ""
    numberCode = []
    cracked = False

    remainingCodes = possibleCodes.copy()

    input("Play Again? ")
    blankLines(3)

    playGame()

def simulate():
    averageTries = 0
    firstGuess = computerGuess()

    for code in possibleCodes:
        tries = 0
        while True:

            # First guess computation take the most time
            if tries == 0:
                guess = firstGuess
            else:
                guess = computerGuess()

            feedback = getFeedback(code,guess)
            filterRemainingCodes(guess,feedback)     
            tries += 1

            if sum(feedback) >= 8:
                break
        print(tries)

        averageTries += tries/len(possibleCodes)
        resetSim()
        
    return averageTries
    
def resetSim():
    global remainingCodes
    remainingCodes = possibleCodes.copy()

if __name__ == "__main__":
    playGame()

    # averageTries = simulate()
    # blankLines(2)
    # print(averageTries)
