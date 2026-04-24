import time
import random

class Player :
    height = 300
    width = 400
    middle = 150

    def __init__(self,window,canvas,xstart,ystart,xend,yend,color):
        self.canvas = canvas
        self.window = window
        self.xstart = xstart
        self.ystart = ystart
        self.xend = xend
        self.yend = yend
        self.color = color
        self.player = canvas.create_rectangle(xstart,ystart,xend,yend,fill=color)
        self.radius = (yend-ystart)/2

    def up(self):
        global state
        state = 1
        while state == 1:
            if self.canvas.coords(self.player)[1] < 2:
                break
            else:
                self.shift_up()
                self.window.update()
                time.sleep(0.02)

    def down(self):  
        global state
        state = 2
        while state == 2:
            if self.canvas.coords(self.player)[3] > self.height-2:
                break
            else:
                self.shift_down()
                self.window.update()
                time.sleep(0.02)

    def stop(self):
        global state
        state = 0

    def shift_up(self):
        self.canvas.move(self.player,0,-5)

    def shift_down(self):
        self.canvas.move(self.player,0,5)

    def coords(self):
        return {"top": self.canvas.coords(self.player)[1], "bottom": self.canvas.coords(self.player)[3], "middle": (self.canvas.coords(self.player)[1]+self.canvas.coords(self.player)[3])/2}
    

class Ball:
    xv = random.choice([7,-7])
    yv = 0
    angle = 4

    def __init__(self,window,canvas,xstart,ystart,xend,yend,color,score1,score2,P1,P2):
        self.canvas = canvas
        self.window = window
        self.xstart = xstart
        self.ystart = ystart
        self.xend = xend
        self.yend = yend
        self.color = color
        self.score1 = score1
        self.score2 = score2
        self.P1 = P1
        self.P2 = P2
        self.ball = canvas.create_rectangle(xstart,ystart,xend,yend,fill=color)

    def hit_paddle(self,paddle,bc):
        global xv,yv
        if paddle["top"]-3 <= bc["height"] and bc["height"] <= paddle["bottom"]+3:
            mid = (paddle["top"] + paddle["bottom"])/2
            self.yv = -(mid-bc["height"]) / self.angle
            self.xv *= -1

    def hit_wall(self,bc):
        global xv,yv
        if bc["top"] >= self.P1.height-3 or bc["bottom"] <= 3:
            self.yv *= -1

    def reset(self):
        global xv,yv
        self.canvas.moveto(self.ball,195,145)
        self.xv = random.choice([7,-7])
        self.yv = 0
        time.sleep(0.25)

    def coords(self):
        b = self.canvas.coords(self.ball)
        return {"left": b[0], "right":b[2], "top":b[1], "bottom":b[3], "height": (b[1]+b[3])//2}

    def increasespeed(self,change):
        global xv,yv
        if abs(self.xv >= 15):
            self.xv = 16
        else:
            self.xv += change

    def move(self):
        global xv,yv
        self.canvas.move(self.ball,self.xv,self.yv)
        self.window.update()
        time.sleep(0.04)

class AI:

    centerstop = False
    aistop = False

    def __init__(self,window,canvas,player,ball):
        self.window = window
        self.canvas = canvas
        self.player = player
        self.ball = ball

    def center(self):
        self.aistop = True
        while abs(self.player.coords()["middle"]-self.player.middle) > 3 and not self.centerstop:
            if self.player.coords()["middle"] < self.player.middle:
                self.player.shift_down()
            else:
                self.player.shift_up()
            time.sleep(0.02)
        self.aistop = False
    
    def hitball(self,direction):
        self.centerstop = True
        location = random.randint(-int(self.player.radius-3),int(self.player.radius-3))
        goal = self.predict(direction)
        while True and not self.aistop:
            player = self.player.coords()
            if player["middle"] + location < goal:
                self.player.shift_down()
            else:
                self.player.shift_up()

            if player["bottom"] >= self.player.height-2:
                break
            if player["top"] <= 2:
                break
            if player["middle"] + location > goal-3 and player["middle"] + location < goal+3:
                break

            time.sleep(0.02)
        self.centerstop = False
               
    
    def predict(self,direction):
        bc = self.ball.coords()

        distance = 0
        if direction == "right":
            distance = self.ball.yv * ((self.player.width-17-bc[direction])/self.ball.xv)
        if direction == "left":
            distance = self.ball.yv * -((bc[direction]-17)/self.ball.xv)

        finalpos = bc["height"] + distance
        if distance <= 0:
            finalpos = abs(finalpos)
        if finalpos > 300:
            finalpos = self.player.height - (distance - (self.player.height - bc["height"]))

        return finalpos





        
