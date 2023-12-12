from tkinter import*
import random
import time
import os

root_width = 1280
root_height = 720

PATH = os.path.dirname(os.path.abspath(__file__))

class HORSE:
    def __init__(self, x, y, img, tag, game):
        self.game = game

        self.x = x
        self.y = y
        self.img = img
        self.tag = tag

    def make_horse(self):
        self.game.canvas.create_image(self.x, self.y, image = self.img, tags = self.tag)

    def move_horse(self):
        random_int = self.game.speed//random.randint(1,10)
        #print(random_int)
        if(self.game.speed>350):
            random_int = 350
        self.x += random_int

        #print(self.tag, self.x, self.y)
        self.game.canvas.coords(self.tag, self.x, self.y)

    def move_horse_player(self):
        self.x += 50
        self.game.canvas.coords(self.tag, self.x, self.y)

    def Clear_Check(self):
        if(self.x >= 1200):
            if(self.tag == "horse7"):
                self.game.Clear()
            else:
                self.game.Gameover()

class Race:
    def __init__(self, canvas):
        self.is_countdown = False

        self.play_time = 0
        self.max_time = 1

        self.speed = 350

        self.horse_width = 80
        self.horse_height = 80

        self.canvas = canvas

        #이미지 불러오기
        self.background = PhotoImage(file=f"{PATH}/image/Race/background.png")#배경
        self.canvas.create_image(root_width/2, root_height/2, image = self.background, tag = "background")

        self.horse_image1 = PhotoImage(file=f"{PATH}/image/Race/horse_1.png")#말1
        self.horse_image2 = PhotoImage(file=f"{PATH}/image/Race/horse_2.png")#말2
        self.horse_image3 = PhotoImage(file=f"{PATH}/image/Race/horse_3.png")#말3
        self.horse_image4 = PhotoImage(file=f"{PATH}/image/Race/horse_4.png")#말4
        self.horse_image5 = PhotoImage(file=f"{PATH}/image/Race/horse_5.png")#말5
        self.horse_image6 = PhotoImage(file=f"{PATH}/image/Race/horse_6.png")#말6
        self.horse_image7 = PhotoImage(file=f"{PATH}/image/Race/horse_7.png")#말7

        self.horse1 = 0
        self.horse2 = 0
        self.horse3 = 0
        self.horse4 = 0
        self.horse5 = 0
        self.horse6 = 0
        self.horse7 = 0

        self.horse_image_list = [self.horse_image1,self.horse_image2,self.horse_image3,self.horse_image4,self.horse_image5,self.horse_image6,self.horse_image7]
        self.horse_list = [self.horse1,self.horse2,self.horse3,self.horse4,self.horse5,self.horse6,self.horse7]

        self.is_clear = False
        self.is_gameover = False
        self.is_start = False
        self.can_move = True

        #말 이미지 생성
        for i in range(7):
            self.horse_list[i] = HORSE(self.horse_width/2+10, i*103+(self.horse_height/2)+10, self.horse_image_list[i] ,"horse"+str(i+1), self)
            self.horse_list[i].make_horse()

        self.txt = canvas.create_text(root_width/2, 3 * root_height/4, text = "달리세요!!!\n<-   ->  연타", font=("System", 70))

    def Clear(self):
        self.is_clear = True
        self.is_gameover = True

    def Gameover(self):
        self.is_gameover = True

    def start(self):
        self.is_start = True

        self.canvas.bind("<KeyPress-Left>", self.KeyPressed)
        self.canvas.bind("<KeyPress-Right>", self.KeyPressed)

        self.canvas.bind("<KeyRelease-Left>",self.KeyRelease)
        self.canvas.bind("<KeyRelease-Right>", self.KeyRelease)

        self.Update()

    def Update(self):
        if(self.is_clear or self.is_gameover):
            pass
        else:
            for i in range(6):
                self.horse_list[i].move_horse()
                self.horse_list[i].Clear_Check()
            self.canvas.after(500, self.Update)

    def KeyPressed(self, e):
        if(self.can_move and self.is_start and self.is_gameover == False):
            self.horse_list[6].move_horse_player()
            self.horse_list[6].Clear_Check()
            self.can_move = False

    def KeyRelease(self, e):
        self.can_move = True
        