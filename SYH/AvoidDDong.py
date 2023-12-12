from tkinter import*
import random
import os

WIDTH = 1280
HEIGHT = 720

FONT = ("System", 30)

CLEAR_TIME = 10

PATH = os.path.dirname(os.path.abspath(__file__))

p_width = 50
p_heigt = 90

class DDong():
    def __init__(self, game):
        self.game = game
        self.dx = random.randint(0, 1280)
        self.speed = random.randint(25, 50)
        self.speed /= 5
        self.dy = 0
        self.ddong = self.game.canvas.create_image(self.dx, self.dy, image = self.game.ddong_img)  
        self.Ddong_main()
        self.delete = False
    def Ddong_main(self):
        if(self.game.is_gameover == False):
            if(self.dy <= HEIGHT-60):
                self.Ddong_fall()
                self.game.canvas.after(10, self.Ddong_main)
            elif(self.dy >= HEIGHT-70):
                self.Ddong_break()

    def Ddong_fall(self):
        self.dy += self.speed
        self.game.canvas.move(self.ddong, 0, self.speed)
        if(self.dx <= self.game.player_dx+p_width/2 and self.dx >= self.game.player_dx-p_width/2 and self.dy >= self.game.player_dy-p_heigt+20 ):
            self.game.is_gameover = True
        
    
    def Ddong_break(self):
        self.game.canvas.itemconfig(self.ddong, image = self.game.ddong_img2)
        self.delete = True
        self.game.canvas.after(500, self.Ddong_delete)
        
    def Ddong_delete(self):
        self.game.ddong_list.remove(self.game.ddong_list[0])
        self.game.canvas.delete(self.ddong)


class AvoidDDong:
    def __init__(self, canvas):
        self.canvas = canvas

        self.play_time = 0
        self.max_time = CLEAR_TIME

        self.is_countdown = False

        self.ddong_list = []
        self.ddong_count = 0

        self.ddong_name_list = ["인간의 똥", "개의 똥", "고양이의 똥", "소의 똥", "말의 똥", "돼지의 똥", "쥐의 똥", "새의 똥", "토끼의 똥", "양의 똥", "코끼리의 똥", "원숭이의 똥", "곤충의 배설물", "곰의 똥", "뱀의 똥", "돌고래의 똥", "고래의 똥", "사슴의 똥", "오리의 똥", "펭귄의 똥", "악어의 똥", "거북의 똥", "바다표범의 똥", "독수리의 똥", "새우의 똥", "게의 똥", "고슴도치의 똥", "바다마크릴의 똥", "햄스터의 똥", "비버의 똥","정희도의 똥", "이정호의 똥", "손영휘의 똥", "손예찬의 똥", "오크 히어로의 똥", "물개의 똥", "앵무새의 똥", "해마의 똥", "히어로인 피스톨의 똥", "판다의 똥", "크로커다일의 똥", "양어리의 똥", "오징어의 똥", "죽치고기의 똥", "염소의 똥", "기린의 똥", "뱀의 똥", "푸마의 똥", "고래 상어의 똥", "까마귀의 똥", "토끼의 똥", "호랑이의 똥", "페가수스의 똥", "드래곤의 똥"]

        #image
        self.bg = PhotoImage(file=f"{PATH}/image/Avoid DDong/background.png")

        self.stand1 = PhotoImage(file=f"{PATH}/image/Avoid DDong/stand1.png")
        self.stand2 = PhotoImage(file=f"{PATH}/image/Avoid DDong/stand2.png")

        self.left1 = PhotoImage(file=f"{PATH}/image/Avoid DDong/left1.png")
        self.left2 = PhotoImage(file=f"{PATH}/image/Avoid DDong/left2.png")

        self.right1 = PhotoImage(file=f"{PATH}/image/Avoid DDong/right1.png")
        self.right2 = PhotoImage(file=f"{PATH}/image/Avoid DDong/right2.png")

        self.ddong_img = PhotoImage(file=f"{PATH}/image/Avoid DDong/ddong.png")
        self.ddong_img2 = PhotoImage(file=f"{PATH}/image/Avoid DDong/ddong2.png")

        self.canvas.create_image(WIDTH/2, HEIGHT/2, image = self.bg)

        self.distance = 0

        self.is_moving = False

        self.ld_pushed = False
        self.rd_pushed = False

        self.count_creat = canvas.create_text(150, 697, text="생성된 똥: "+str(self.ddong_count), font=FONT, fill="white")
        self.time = canvas.create_text(WIDTH/2, 697, text="똥을 피해라!!!", font=FONT, fill="white")
        self.ddong_name = canvas.create_text(WIDTH-170, 697, text="", font=FONT, fill="white")

        self.player_dx = WIDTH/2
        self.player_dy = HEIGHT-95

        self.player = canvas.create_image(WIDTH/2, HEIGHT-95, image = self.stand1)

        self.is_clear = False
        self.is_gameover = False
    
    def start(self):
        self.Creat_ddong()

        self.canvas.bind("<KeyPress-Left>", self.LD)
        self.canvas.bind("<KeyPress-Right>", self.RD)
        self.canvas.bind("<KeyRelease-Left>",self.Left_Up)
        self.canvas.bind("<KeyRelease-Right>", self.Right_Up)
        self.Animation()
        self.Move()
        self.Time_check()
        
    def Animation(self):
        if(self.is_gameover == False):
            if(self.distance == 0):
                self.Stand1()
            elif(self.distance < 0):
                self.Left1()
            elif(self.distance > 0):
                self.Right1()

    def Stand1(self):
        if(self.is_gameover == False):
            if(self.distance == 0):
                self.canvas.itemconfig(self.player, image = self.stand1)
                self.canvas.after(150, self.Stand2)

    def Stand2(self):
        if(self.is_gameover == False):
            if(self.distance == 0):
                self.canvas.itemconfig(self.player, image = self.stand2)
                self.canvas.after(150, self.Stand1)
    def Left1(self):
        if(self.is_gameover == False):
            if(self.distance < 0):
                self.canvas.itemconfig(self.player, image = self.left1)
                self.canvas.after(150, self.Left2)

    def Left2(self):
        if(self.is_gameover == False):
            if(self.distance < 0):
                self.canvas.itemconfig(self.player, image = self.left2)
                self.canvas.after(150, self.Left1)

    def Right1(self):
        if(self.is_gameover == False):
            if(self.distance > 0):
                self.canvas.itemconfig(self.player, image = self.right1)
                self.canvas.after(150, self.Right2)
    def Right2(self):
        if(self.is_gameover == False):
            if(self.distance > 0):
                self.canvas.itemconfig(self.player, image = self.right2)
                self.canvas.after(150, self.Right1)

    #키입력 함수
    def Move(self):
        if(self.is_gameover == False):
            self.player_dx += self.distance
            self.canvas.move(self.player, self.distance, 0)
            self.canvas.after(10, self.Move)
            if(0>self.player_dx):
                self.player_dx +=5
                self.canvas.move(self.player, +5, 0)
            if(1280<self.player_dx):
                self.player_dx -=5
                self.canvas.move(self.player, -5, 0)
        

    def Left_Down(self):
        if(0<self.player_dx and self.player_dx<1500 and self.ld_pushed):
            #distance = -5
            self.canvas.after(10, self.Left_Down)

    def LD(self, e):
        if(self.ld_pushed == False and self.is_moving == False):
            self.distance = -5
            self.ld_pushed = True
            self.Animation()
            self.Left_Down()

    def Right_Down(self):
        if(-100 <self.player_dx and self.player_dx<1280 and self.rd_pushed):
            #distance = 5

            self.canvas.after(10, self.Right_Down)

    def RD(self, e):
        if(self.rd_pushed == False and self.is_moving == False):
            self.distance = 5
            self.rd_pushed = True
            self.Animation()
            self.Right_Down()

    def Left_Up(self, e):
        self.ld_pushed = False
        if(self.rd_pushed == False):
            self.distance = 0
            self.is_moving = False
            self.Animation()
        if(self.distance<0):
            self.distance = 0
            self.is_moving = False
            self.Animation()        

    def Right_Up(self, e):
        self.rd_pushed = False
        if(self.ld_pushed == False):
            self.distance = 0
            self.is_moving = False
            self.Animation()
        if(self.distance>0):
            self.distance = 0
            self.is_moving = False
            self.Animation()

    def Time_check(self):
        if(self.is_gameover == False):
            if(self.play_time >= CLEAR_TIME):
                self.is_clear = True
                self.is_gameover = True
            else:
                self.play_time+=1
                self.canvas.after(1000, self.Time_check)

    def Creat_ddong(self):
        if(self.is_gameover == False):
            self.ddong_list.append(DDong(self))
            self.canvas.after(100, self.Creat_ddong)
            self.ddong_count += 1
            self.canvas.itemconfig(self.count_creat, text = "생성된 똥: "+ str(self.ddong_count))
            self.canvas.itemconfig(self.ddong_name, text =  random.choice(self.ddong_name_list))