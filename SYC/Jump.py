#점프게임
import tkinter
import random
import time
import math
import os

WIDTH = 1280
HEIGHT = 720

# 기존 코드
FPS = 60
DELTATIME = 1 / FPS

MAX_FLOOR_GAP = 150

G = 1300

CLEAR_TIME = 10

PATH = os.path.dirname(os.path.abspath(__file__))

class Jump:
    def __init__(self, canvas):

        self.max_time = CLEAR_TIME

        self.is_countdown = False

        self.is_clear = False
        self.is_gameover = False

        self.play_time = 0

        self.left_key = False
        self.right_key = False
        self.up_key = False

        self.speed = 200

        self.jump_count = 0

        self.canvas = canvas

        self.player_width = 50
        self.player_height = 100
        self.player_speed = 400
        self.player_jump_power = 800
        self.player_x = WIDTH / 2 - self.player_width / 2
        self.player_y = HEIGHT * 2 / 3 - self.player_height / 2
        self.player_velocity_x = 0
        self.player_velocity_y = 0

        self.screen_img = tkinter.PhotoImage(file=PATH + "/image/Jump/volcano.png")
        self.canvas.create_image(WIDTH/2, HEIGHT/2, image = self.screen_img) 

        self.player_img = tkinter.PhotoImage(file=PATH + "/image/Jump/Plant3.png")
        self.player_id = canvas.create_image(25, 50, image = self.player_img)

        # 직접 작성
        self.lava_image = tkinter.PhotoImage(file=PATH + "/image/Jump/Lava.png")
        self.lava = canvas.create_image(WIDTH/2, 2 * HEIGHT, image = self.lava_image)
        self.lava_y = 680

        # 기존 코드
        self.floor_width = 120
        self.floor_height = 30
        self.floors = []

        id = canvas.create_rectangle(0, 0, self.floor_width, self.floor_height, fill="gray")
        self.floors.append([self.player_x + self.player_width / 2 - self.floor_width / 2, self.player_y + self.player_height, id])

        self.score = 0

        self.update_canvas()

    def start(self):
        self.canvas.bind("<KeyPress>", self.key_press)
        self.canvas.bind("<KeyRelease>", self.key_release)
        
        self.Time_check()
        self.update()
        self.lava_up()
    
    def check_collision(self, rect1, rect2):
        if (rect1[0] < rect2[0] < rect1[0] + rect1[2] or rect2[0] < rect1[0] < rect2[0] + rect2[2]) and (rect1[1] < rect2[1] < rect1[1] + rect1[3] or rect2[1] < rect1[1] < rect2[1] + rect2[3]):
            return True
        
        return False

    def key_press(self, event):
        if event.keysym == "Left":
            self.left_key = True
        elif event.keysym == "Right":
            self.right_key = True
        elif event.keysym == "Up":
            if self.jump_count <= 1:
                self.player_velocity_y = - self.player_jump_power
                self.jump_count += 1

    def key_release(self, event):
        if event.keysym == "Left":
            self.left_key = False
        elif event.keysym == "Right":
            self.right_key = False

    def update(self):
        if(self.is_gameover == False):
            while self.floors[0][1] > HEIGHT:
                id = self.floors[0][2]
                
                self.floors.pop(0)

                self.canvas.delete(id)

            while self.floors[-1][1] > 0:
                self.score += 1
                id = self.canvas.create_rectangle(0, 0, self.floor_width, self.floor_height, fill = "gray")
                self.floors.append([random.random() * (WIDTH - self.floor_width), self.floors[-1][1] - ((MAX_FLOOR_GAP / 5) + random.random() * MAX_FLOOR_GAP * 4 / 5), id])
                self.lava_down()
            self.player_velocity_x = 0

            if self.left_key:
                self.player_velocity_x -= self.player_speed
            if self.right_key:
                self.player_velocity_x += self.player_speed
            
            self.player_velocity_y += G * DELTATIME
            
            self.player_x += self.player_velocity_x * DELTATIME
            self.player_y += self.player_velocity_y * DELTATIME
            
            if self.player_x + self.player_width < 0:
                self.player_x += WIDTH + self.player_width
            if self.player_x > WIDTH:
                self.player_x -= WIDTH + self.player_width

            for x, y, id in self.floors:
                if self.check_collision((self.player_x, self.player_y + self.player_height * 4 / 5, self.player_width, self.player_height / 5), (x, y, self.floor_width, self.floor_height)):
                    if self.player_velocity_y > 0:
                        
                        self.player_y = y - self.player_height
                        self.player_velocity_y = 0
                        self.jump_count = 0
            
            if self.player_y < HEIGHT / 2:
                t = HEIGHT / 2 - self.player_y

                self.player_y = HEIGHT / 2

                for floor in self.floors:
                    floor[1] += t
            # 직접 작성
            if self.player_y + self.player_height > self.lava_y:
                self.Gameover()

            self.update_canvas()
            self.canvas.after(int(DELTATIME * 1000), self.update)

    def update_canvas(self):
        self.canvas.moveto(self.player_id, self.player_x, self.player_y)

        for x, y, id in self.floors:
            self.canvas.moveto(id, x, y)

        self.canvas.tag_raise(self.player_id)
    # 직접 작성
    def lava_down(self):
        if self.lava_y < HEIGHT:
            self.lava_y += 20
            self.canvas.moveto(self.lava,0,self.lava_y)

    def lava_up(self):  
        if(self.is_gameover == False):
            self.lava_y -= 5
            self.canvas.moveto(self.lava,0,self.lava_y)
            self.canvas.after(300-self.speed, self.lava_up)
        
    def Time_check(self):
        if(self.is_gameover == False):
            if(self.play_time >= CLEAR_TIME):
                self.Clear()
            self.play_time += 1
            self.canvas.after(1000, self.Time_check)
        
    def Clear(self):
        self.is_clear = True
        self.is_gameover = True

    def Gameover(self):
        self.is_gameover = True

'''
출처    
<a href="https://kr.freepik.com/free-vector/
jurassic-period-landscape-with-volcano-and-
meteor_7743408.htm#query=volcanic%20eruption&
position=41&from_view=search&track=ais&uuid=48d98fd6-225e-479d-bc5c-03d43703726b">
작가 upklyak</a> 출처 Freepik   
'''