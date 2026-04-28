# Based off 3blue1brown wordle bot

# Average Turns based for each version
# no bias: 4.685185185185183
# actualCodeBias=1: 4.394290123456754
# actualCodeBias=4 average turns: 4.356481481481449
# sqrt(P(actualCode)): 4.364197530864163
# minimum score given entropy and P(actualCode): 4.360339506172806

import sys
import math
import time

# Turning color strings into list of numbers so it's easier for the solver
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

# Compute hash map of each possible code to save time while calculuating a move
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

# Average number of turns to solve the code after a certain amount of entropy
# entropyToTurns = {10.34: 4.6852, 4.17: 2.7698412698412698, 2.58: 2.2450980392156863, 0.0: 1.0, 3.0: 2.35, 1.58: 2.0852713178294575, 6.29: 3.3974358974358974, 3.32: 2.525, 1.0: 2.0, 3.58: 2.6875, 2.0: 2.1, 5.75: 3.175925925925926, 3.17: 2.2666666666666666, 6.98: 3.6587301587301586, 3.7: 2.5384615384615383, 4.81: 2.9523809523809526, 7.99: 3.9645669291338583, 5.88: 3.135593220338983, 4.64: 3.0, 2.81: 2.2857142857142856, 2.32: 2.2454545454545456, 3.91: 2.4, 6.75: 3.509259259259259, 4.09: 2.588235294117647, 4.32: 2.725, 4.25: 2.9210526315789473, 5.13: 3.1714285714285713, 5.46: 3.159090909090909, 7.79: 3.779279279279279, 5.64: 3.1, 4.39: 2.761904761904762, 4.0: 2.75, 8.11: 3.9057971014492754, 5.29: 2.9743589743589745, 3.81: 2.5, 4.91: 2.9, 5.25: 2.9210526315789473, 5.39: 3.0238095238095237, 4.75: 2.888888888888889, 6.34: 3.6419753086419755, 3.46: 2.5454545454545454}
# Equation: Turns = 0.0066(Entropy)^2 + 0.2306(Entropy) + 1.6453
def entropyToTurns(entropy: float):
    return 0.0066*entropy**2 + 0.2306*entropy + 1.6453

def clearLines(lines: int):
    for line in range(lines):
        sys.stdout.write('\033[A')
        sys.stdout.write('\033[K')

def blankLines(lines: int):
    print("\n" * lines)

# Turn code list into a colored string in the terminal
def colorCode(code):
    colorCode = " "
    for color in code:
        if isinstance(code, list):
            colorCode += colorKey[numbersToColors[color]]+" "
        else:
            colorCode += colorKey[color]+" "
    return colorCode

# Turn response list into a colored string in the terminal
def colorResponse(response: str):
    coloredResponse = " "
    for color in response:
        coloredResponse += responseKey[color]+" "
    return coloredResponse

# Getting code list value in base 6
def baseSix(number: list):
    return 216*number[0] + 36*number[1] + 6*number[2] + number[3]

# Getting response list value in base 3 
def baseThree(number: list):
    return 27*number[0] + 9*number[1] + 3*number[2] + number[3]

# Turn a probability into bits of information for easier handling
def getBits(probability: float):
    if (probability == 0):
        return 0
    return math.log2(1/probability)

# Gets the code the use inputs
def getUserCode():
    global stringCode

    stringCode = ""
    validCode = False

    # Checks if code has valid color symbols and has a length of four
    # If not make the user keep inputing a code untill it's valid
    while not validCode:
        validCode = True
        stringCode = input("Enter Code: ").strip().upper()
        if len(stringCode) != 4:
            validCode = False
        for color in stringCode:
            if color not in colors:
                validCode = False
        clearLines(1)
    
    # Turn userinput into a 
    for color in stringCode:
        numberCode.append(colorsToNumbers[color])

# Return feedback given a code and a guess
def getFeedback(code:list, possibleMatch:list):
    response = []

    # Since each code is different they all have different values in base 6
    # Those base6 values are the indexes for the hashmap of that code
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
    minScore = 20

    if len(remainingCodes) == 1:
        return remainingCodes[0]

    for guess in possibleCodes:

        feedbackDistribution = [0] * 81
        meanInformation = 0

        probability = 1/len(remainingCodes)
        entropy = getBits(probability)

        for response in remainingCodes:
            # Each response has a different base 3 value so that can be used asa an index
            # A list of how many remainingCodes would give a certain feedback pattern for each pattern
            feedbackDistribution[baseThree(getFeedback(guess,response))] += 1

        for feedback in feedbackDistribution:
            meanInformation += feedback/len(remainingCodes) * getBits(feedback/len(remainingCodes))
        
        # Calculate the average score after a guess based on if it could be the code and the amount of information it provides
        # Higher entropy and probability of being a guess when there's only a few possibilities cause lower score
        if guess in remainingCodes:
            scoreEstimate = probability + entropyToTurns(entropy-meanInformation)*(1-probability) 
        else:
            scoreEstimate = entropyToTurns(entropy-meanInformation)
        
        # Store the guess that gives the lowest average score
        if scoreEstimate < minScore:
            bestGuess = guess
            minScore = scoreEstimate
    
    return bestGuess
    
# Update reminingCodes to codes that could still be the answer
def filterRemainingCodes(guess: list, feedback: list):
    global remainingCodes

    newRemainingCodes = []
    for code in remainingCodes:
        if getFeedback(code,guess) == feedback:
            newRemainingCodes.append(code)
    
    remainingCodes = newRemainingCodes

# main function to take user input and let computer solve it
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

        # check if code is correct
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

# Run through all possible codes and record amoutn of turns needed for each one
def simulate():
    # Store first guess since it takes the most time to compute and it won't change
    firstGuess = computerGuess()
    averageTries = 0

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

# Returns how many turns on average it takes to solve a code after a certain entropy
# Used to give bias to guesses that could be the answer in the solver 
def entropyToAverageScore():
    firstGuess = computerGuess()
    entropyToTries = {10.34: 4.6852}
    entropyCount = {10.34: 1}

    for code in possibleCodes:
        tries = 0
        entropyPerTurn = {}

        while True:

            if tries == 0:
                guess = firstGuess
            else:
                guess = computerGuess()

            feedback = getFeedback(code,guess)
            filterRemainingCodes(guess,feedback)     
            tries += 1

            if sum(feedback) >= 8:
                break
        
            # Recrods entropy on each turn
            entropyPerTurn[round(getBits(1/len(remainingCodes)), 2)] = tries

        # Creating dictionary of how long it took to solve the code after each entropy value
        for entropy in entropyPerTurn.keys():
            if entropy in entropyCount:
                entropyCount[entropy] += 1
                entropyToTries[entropy] += tries-entropyPerTurn[entropy]
            else: 
                entropyCount[entropy] = 1
                entropyToTries[entropy] = tries-entropyPerTurn[entropy]

        resetSim()
    
    for entropy in entropyToTries.keys():
        entropyToTries[entropy] /= entropyCount[entropy]
        
    return entropyToTries
    
def resetSim():
    global remainingCodes
    remainingCodes = possibleCodes.copy()

if __name__ == "__main__":
    playGame()

    # averageTries = simulate()
    # print(averageTries)

    # entropyToTurns = entropyToAverageScore()
    # print(entropyToTurns)
