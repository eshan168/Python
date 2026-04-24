from tkinter import *
import math
import random

field = [0,0,0,0,0,0,0,0,0]
turn = {1:"X",-1:"O",0:"None"}
move = 1

def press(event):
    global move,field,turn
    xcor = event.x//100
    ycor = event.y//100
    index = int((xcor) + 3*ycor)
    if field[index] != 0:
        return None
    place(index)

def place(index:int):
    global field,turn,move
    xcor = (index%3)*100
    ycor = (index//3)*100
    Label(window,text=turn[move],font=("Arial",40)).place(x=xcor+28,y=ycor+20)
    field[index] = move
    print(turn[check(field,move)])
    move *= -1

def check(field:list,move:int):
    if sum(field[0:3])/move == 3: return move
    if sum(field[3:6])/move == 3: return move
    if sum(field[6:9])/move == 3: return move
    if sum(field[::3])/move == 3: return move
    if sum(field[1::3])/move == 3: return move
    if sum(field[2::3])/move == 3: return move
    if sum(field[::4])/move == 3: return move
    if sum(field[2:7:2])/move == 3: return move
    else:
        return 0

def empty(field:list):
    empty = [i for i in range(len(field)) if field[i] == 0]
    return empty

def randomizer(moves:list):
    m = max(moves)
    ran = [i for i in range(len(moves)) if moves[i] == m]
    return random.choice(ran)

def reset():
    global field,window,canvas,move
    field = [0,0,0,0,0,0,0,0,0]
    move = 1
    window.destroy()
    main()  

def comp(board:list,maximizer:bool,depth:int):

    global move
    turn = -1 if field.count(0)%2 == 0 else 1
    pos = empty(board)
    wins = []

    if board.count(0) == 1:
        board[pos[0]] = turn
        res = check(board,turn)/move
        board[pos[0]] = 0
        return res

    for i in pos:
        board[i] = turn
        res = check(board,turn)/move
        if res != 0: 
            wins.append(res/depth)
        else:
            wins.append(comp(board,not maximizer,depth+1)/depth)
        board[i] = 0
        
    if depth == 1:
        print(wins)
        return pos[randomizer(wins)]

    if maximizer:
        return max(wins)

    if not maximizer:
        return min(wins)


def AI(event):
    global move,field
    if field.count(0) <= 1:
        place(field.index(0))
        return
    if field.count(0) == 9:
        place(4) 
        return

    ai = comp(field,True,1)
    place(ai)


def main():
    global window,canvas

    window = Tk()
    window.title("Tic-Tac-Toe")
    window.geometry("300x325")

    canvas = Canvas(window,width=300,height=300)
    canvas.pack()

    label = "                    Reset                    "
    Button(window,text=label,command=reset).place(x=70,y=300)

    canvas.create_line(0,100,300,100,fill="black",width=3)
    canvas.create_line(0,200,300,200,fill="black",width=3)
    canvas.create_line(100,0,100,300,fill="black",width=3)
    canvas.create_line(200,0,200,300,fill="black",width=3)

    window.bind("<Button-1>",press)
    window.bind("<space>",AI)

    window.mainloop()

if __name__ == "__main__":
    main()
