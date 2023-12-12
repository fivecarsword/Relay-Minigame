#에어하키 게임
# 직접 작성
import tkinter
import random
import math
import time

WIDTH = 1280
HEIGHT = 720

CLEAR_TIME = 10

class Paddle:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x + 20, y + 80, fill= color)
    # gpt 사용
    def move(self, dx, dy):
        current_pos = self.canvas.coords(self.id)
       
        if (
            current_pos[0] + dx > 0
            and current_pos[2] + dx < 1300
            and current_pos[1] + dy > 0
            and current_pos[3] + dy < 740
        ):
            self.canvas.move(self.id, dx, dy)
        
    def Left(self):
            current_pos = self.canvas.coords(self.id)
            if(current_pos[0]>WIDTH/2):
                self.move(-40, 0)

# 직접 작성
class Puck:
    def __init__(self, canvas, game):
        self.canvas = canvas
        self.game = game
        self.id = canvas.create_oval(290, 190, 310, 210, fill="red")
        self.dy = 300
        self.reset()

    def reset(self):
        self.canvas.coords(self.id, 290, 190, 310, 210)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])

    def move(self):
        self.canvas.move(self.id, self.speed_x, self.speed_y)
        self.dy+=self.speed_y

        self.game.canvas.move(self.game.left_paddle.id, 0, self.speed_y)
        self.puck_pos = self.canvas.coords(self.id)
        
        # gpt 사용
        # Check for collisions with walls
        if self.puck_pos[1] <= 0 or self.puck_pos[3] >= 720:
            self.speed_y = -self.speed_y

        # Check for collisions with paddles
        
        if (
            self.puck_pos[2] >= self.game.left_paddle.canvas.coords(self.game.left_paddle.id)[0]
            and self.puck_pos[0] <= self.game.left_paddle.canvas.coords(self.game.left_paddle.id)[2]
            and self.puck_pos[3] >= self.game.left_paddle.canvas.coords(self.game.left_paddle.id)[1]
            and self.puck_pos[1] <= self.game.left_paddle.canvas.coords(self.game.left_paddle.id)[3]
        ) or (
            self.puck_pos[0] <= self.game.right_paddle.canvas.coords(self.game.right_paddle.id)[2]
            and self.puck_pos[2] >= self.game.right_paddle.canvas.coords(self.game.right_paddle.id)[0]
            and self.puck_pos[3] >= self.game.right_paddle.canvas.coords(self.game.right_paddle.id)[1]
            and self.puck_pos[1] <= self.game.right_paddle.canvas.coords(self.game.right_paddle.id)[3]
        ):
            self.speed_x = -self.speed_x
            self.speed_y = random.randint(-7, 7)
            self.speed_y = -self.speed_y 

        # Check for scoring
        if self.puck_pos[0] <= 0 or self.puck_pos[2] >= 1280:
            self.game.Gameover()

class AirHockey:
    def __init__(self, canvas):
        self.play_time = 0

        self.max_time = CLEAR_TIME

        self.is_countdown = False

        self.is_clear = False
        self.is_gameover = False

        self.canvas = canvas
        self.canvas.config(bg="light cyan3")
        self.canvas.create_line(640, 0, 640, 720, fill = "midnight blue", width= 10)

        self.left_paddle = Paddle(self.canvas, 50, 200, "cyan2")
        self.right_paddle = Paddle(self.canvas, 950, 290, "yellow green")
        self.puck = Puck(self.canvas, self)
    
    def start(self):
        self.canvas.bind("<Up>", lambda event: self.right_paddle.move(0, -40))
        self.canvas.bind("<Down>", lambda event: self.right_paddle.move(0, 40))
        self.canvas.bind("<Left>", lambda event: self.right_paddle.Left())
        self.canvas.bind("<Right>", lambda event: self.right_paddle.move(40, 0))

        self.move_puck()
        self.Time_check()
        
    def move_puck(self):
        if (self.is_gameover == False):
            self.puck.move()
            self.canvas.after(10, self.move_puck)
    # 직접 작성
    def Time_check(self):
        if (self.is_gameover == False):
            if(self.play_time >= CLEAR_TIME):
                self.Clear()
            self.play_time += 1
            self.canvas.after(1000, self.Time_check)
        
    def Clear(self):
        self.is_clear = True
        self.is_gameover = True

    def Gameover(self):
        self.is_gameover = True