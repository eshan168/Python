from tkinter import *
from ClassPong import *
import threading


P1score = 0
P2score = 0

running = True

def pause(event):
    global running,ball
    running = not running
    if running:
        threading.Thread(target=run,args=(ball,)).start()

def run(ball):
    global P1,P2,P1score,P2score,score_1,score_2
    while running:

        bc = ball.coords()

        ball.hit_wall(bc)

        if bc["right"] >= P1.width-17:
            ball.hit_paddle(P1.coords(),bc)
            ball.increasespeed(-0.5)
            threading.Thread(target=ai.center,args=()).start()

        if bc["left"] <= 17:
            ball.hit_paddle(P2.coords(),bc)
            ball.increasespeed(0.5)
            if ball.xv > 0:
                threading.Thread(target=ai.hitball,args=("right",)).start()

        if bc["right"] > P1.width:
            P1score += 1
            canvas.itemconfigure(score_2, text=P1score)
            threading.Thread(target=ai.center,args=()).start()
            ball.reset()

        if bc["left"] < 0:
            P2score += 1
            canvas.itemconfigure(score_1, text=P2score)
            threading.Thread(target=ai.center,args=()).start()
            ball.reset()

        ball.move()

window = Tk()
window.title("Pong")
canvas = Canvas(window,width=400,height=300,bg="black")
canvas.pack()

canvas.create_line(200,5,200,297,fill="white",width=3)

score_1 = canvas.create_text(300,20,text=P1score,fill="white",font="Arial 20")
score_2 = canvas.create_text(100,20,text=P2score,fill="white",font="Arial 20")

P1 = Player(window,canvas,385,125,395,180,"white")
P2 = Player(window,canvas,5,125,15,180,"white")

ball = Ball(window,canvas,195,145,205,155,"white",score_1,score_2,P1,P2)

ai = AI(window,canvas,P1,ball)

# window.bind("<KeyPress-Down>", lambda event: threading.Thread(target=P1.down(), args=()).start())
# window.bind("<KeyRelease-Down>", lambda event: threading.Thread(target=P1.stop(), args=()).start())
# window.bind("<KeyPress-Up>", lambda event: threading.Thread(target=P1.up(), args=()).start())
# window.bind("<KeyRelease-Up>", lambda event: threading.Thread(target=P1.stop(), args=()).start())

window.bind("<KeyPress-Down>", lambda event: threading.Thread(target=P2.down(), args=()).start())
window.bind("<KeyRelease-Down>", lambda event: threading.Thread(target=P2.stop(), args=()).start())
window.bind("<KeyPress-Up>", lambda event: threading.Thread(target=P2.up(), args=()).start())
window.bind("<KeyRelease-Up>", lambda event: threading.Thread(target=P2.stop(), args=()).start())

window.bind("<KeyPress-w>", lambda event: threading.Thread(target=P2.up(), args=()).start())
window.bind("<KeyRelease-w>", lambda event: threading.Thread(target=P2.stop(), args=()).start())
window.bind("<KeyPress-s>", lambda event: threading.Thread(target=P2.down(), args=()).start())
window.bind("<KeyRelease-s>", lambda event: threading.Thread(target=P2.stop(), args=()).start())

window.bind("<space>", pause)

threading.Thread(target=run,args=(ball,)).start()

window.mainloop()
