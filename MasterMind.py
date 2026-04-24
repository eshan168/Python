import sys
import random

# Setting values and color keys
colors = ["R", "O", "Y", "G", "B", "P"]
responses = ["L", "W", "N"]

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
responseKey = {0:noPositonOrColor, 1:colorOnly, 2:positionAndColor,}

code = ""
codeHashMap = {}
cracked = False

def clearLines(lines: int):
    for line in range(lines):
        sys.stdout.write('\033[A')
        sys.stdout.write('\033[K')

def blankLines(lines: int):
    print("\n" * lines)

def colorCode(code: str):
    colorCode = " "
    for color in code:
        colorCode += colorKey[color]+" "
    return colorCode

def colorResponse(response: str):
    coloredResponse = " "
    for color in response:
        coloredResponse += responseKey[color]+" "
    return coloredResponse

def getRandomCode():
    global code

    for i in range(4):
        color = random.choice(colors)
        code += color

        if color in codeHashMap:
            codeHashMap[color] += 1
        else:
            codeHashMap[color] = 1

def getUserGuess():
    guess = ""
    validCode = False

    while not validCode:
        validCode = True
        guess = input("Guess: ").strip().upper()
        if len(guess) != 4:
            validCode = False
        for color in guess:
            if color not in colors:
                validCode = False
        clearLines(1)
    return guess

def getResponse(guess: str):
    global cracked

    response = []
    correctNum = 0

    # Hashmap of code to make sure there aren't repetitions
    # When the code only has one of a certain color and the guess has two of that color prevent two yellows
    hashMap = codeHashMap.copy()

    for i in range(len(guess)):
        if guess[i] == code[i]:
            response.append(2)
            hashMap[guess[i]] -= 1
            correctNum += 1

    for i in range(len(guess)):
        if guess[i] in code and hashMap[guess[i]] > 0:
            response.append(1)
            hashMap[guess[i]] -= 1

    if correctNum >= 4:
        cracked = True
    
    response += [0] * (4-len(response))

    clearLines(1)
    print(f"|{colorCode(guess)}|   |{colorResponse(response)}|")


def play():
    getRandomCode()
    print(code)
    print(f"Red: {red} \nOrange: {orange} \nYellow: {yellow} \nGreen: {green} \nBlue: {blue} \nPurple: {purple} \n")
    print(f"Color and position correct: {positionAndColor} \nWrong position but color is in code: {colorOnly} \nWrong color and position: {noPositonOrColor}\n")

    for guesses in range(10):
        print("")

        getResponse(getUserGuess())

        if (cracked):
            break

    if cracked:
        print("\nCode Cracked!\n")

    reset()

def reset():
    global code,codeHashMap,cracked

    code = ""
    codeHashMap = {}
    cracked = False

    input("Play Again? ")
    blankLines(3)

    play()

if __name__ == "__main__":
    play()





