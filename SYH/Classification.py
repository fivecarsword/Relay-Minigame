from tkinter import *
import random
import os

screen_width = 1280
screen_height = 720

GAMEOVER_TIME = 10

PATH = os.path.dirname(os.path.abspath(__file__))

class Create:
    def __init__(self, game):
        self.game = game

        self.rand = random.randint(0, 2)
        self.x = screen_width/2+600
        self.y = screen_height/2
        self.img = self.game.image_list1[self.rand]
        self.ch = self.game.canvas.create_image(self.x, self.y, image = self.img, tags = self.game.tag_list[self.rand])

    def move(self):
        self.game.is_moving = True
        self.x -= 20
        self.game.canvas.coords(self.ch, self.x, self.y)
        if(self.x>screen_width/2-300):
            self.game.canvas.after(10, self.move)
        else:
            self.game.canvas.delete(self.ch)
            self.game.ch_row_list.remove(self)
            self.game.is_moving = False

class Classification:
    def __init__(self, canvas):
        self.is_countdown = True

        self.play_time = 0
        self.max_time = GAMEOVER_TIME
        
        self.is_clear = False
        self.is_gameover = False

        self.ch_count = 15
        self.count = self.ch_count
        self.i = 3

        self.is_moving = False

        self.dx = screen_width/2
        self.dy = screen_height/2

        self.canvas = canvas

        self.bg_img = PhotoImage(file = f"{PATH}/image/Classification/background.png")
        self.aaa = canvas.create_image(screen_width/2, screen_height/2, image = self.bg_img)

        #image

        self.cat1 = PhotoImage(file = f"{PATH}/image/Classification/냥1.png")
        self.cat2 = PhotoImage(file = f"{PATH}/image/Classification/냥2.png")

        self.dog1 = PhotoImage(file = f"{PATH}/image/Classification/멍1.png")
        self.dog2 = PhotoImage(file = f"{PATH}/image/Classification/멍2.png")

        self.man1 = PhotoImage(file = f"{PATH}/image/Classification/인1.png")
        self.man2 = PhotoImage(file = f"{PATH}/image/Classification/인2.png")

        self.image_list1 = [self.cat1, self.dog1, self.man1]
        self.image_list2 = [self.cat2, self.dog2, self.man2]

        self.tag_list = ["cat", "dog", "man"]


        self.local_crrent_x = [screen_width/2+600]
        self.ch_row_list = [Create(self),Create(self), Create(self)]
        self.ch_row_list[0].x = screen_width/2
        self.ch_row_list[1].x = screen_width/2+300
        self.ch_row_list[2].x = screen_width/2+600
        self.canvas.coords(self.ch_row_list[0].ch, screen_width/2, screen_height/2)
        self.canvas.coords(self.ch_row_list[1].ch, screen_width/2+300, screen_height/2)
        self.canvas.coords(self.ch_row_list[2].ch, screen_width/2+600, screen_height/2)

        self.count_text = self.canvas.create_text(screen_width/2, 120, text = "남은 수 "+str(self.count), font=("System", 50), fill="black")

    def start(self):
        self.canvas.after(1000, self.Time)

        button = Button(self.canvas, text = "개",font = ("System", 40),  command=self.bt_dog)
        self.canvas.create_window(screen_width/2-280, 600, window=button, tag="BT")
        # button.place(x=screen_width/2-300, y = 600)

        button = Button(self.canvas, text = "고양이",font = ("System", 40), command=self.bt_cat)
        self.canvas.create_window(screen_width/2-50, 600, window=button, tag="BT")
        # button.place(x=screen_width/2 - 100, y = 600)

        button = Button(self.canvas, text = "인간",font = ("System", 40), command=self.bt_man)
        self.canvas.create_window(screen_width/2+190, 600, window=button, tag="BT")
        # button.place(x=screen_width/2+190, y = 600)

    def Time(self):
        if self.is_gameover:
            return

        if(self.play_time >= GAMEOVER_TIME):
            self.is_gameover = True
            self.canvas.delete("BT")
        else:
            self.play_time += 1
            self.canvas.after(1000, self.Time)

    def Clear_ck(self):
        if(self.count == 0):
            self.is_clear = True
            self.is_gameover = True
            self.canvas.delete("BT")
    
    def move_2(self):
        if(len(self.ch_row_list) == 4):
            self.ch_row_list[1].x = screen_width/2
            self.ch_row_list[2].x = screen_width/2+300
            self.ch_row_list[3].x = screen_width/2+600
            self.canvas.coords(self.ch_row_list[1].ch, screen_width/2, screen_height/2)
            self.canvas.coords(self.ch_row_list[2].ch, screen_width/2+300, screen_height/2)
            self.canvas.coords(self.ch_row_list[3].ch, screen_width/2+600, screen_height/2)
        elif(len(self.ch_row_list) == 3):
            self.ch_row_list[1].x = screen_width/2
            self.ch_row_list[2].x = screen_width/2+300
            self.canvas.coords(self.ch_row_list[1].ch, screen_width/2, screen_height/2)
            self.canvas.coords(self.ch_row_list[2].ch, screen_width/2+300, screen_height/2)
        elif(len(self.ch_row_list) == 2):
            self.ch_row_list[1].x = screen_width/2
            self.canvas.coords(self.ch_row_list[1].ch, screen_width/2, screen_height/2)

    def bt_dog(self):
        if (self.canvas.itemcget(self.ch_row_list[0].ch, "tag") == "dog"and self.is_moving == False):
            self.canvas.itemconfig(self.ch_row_list[0].ch, image = self.image_list2[1])
            self.ch_row_list[0].move()
            if(self.i<self.ch_count):
                self.ch_row_list.append(Create(self))
            self.move_2()
            self.count-=1
            self.canvas.itemconfig(self.count_text, text = "남은 수 "+str(self.count))
            self.i += 1 
            self.Clear_ck()
            
    def bt_cat(self):
        if (self.canvas.itemcget(self.ch_row_list[0].ch, "tag") == "cat"and self.is_moving == False):
            self.canvas.itemconfig(self.ch_row_list[0].ch, image = self.image_list2[0])
            self.ch_row_list[0].move()
            if(self.i<self.ch_count):
                self.ch_row_list.append(Create(self))
            self.move_2()
            self.count-=1
            self.canvas.itemconfig(self.count_text, text = "남은 수 "+str(self.count))
            self.i += 1 
            self.Clear_ck()
            
    def bt_man(self):
        if (self.canvas.itemcget(self.ch_row_list[0].ch, "tag") == "man"and self.is_moving == False):
            self.canvas.itemconfig(self.ch_row_list[0].ch, image = self.image_list2[2])
            self.ch_row_list[0].move()
            if(self.i<self.ch_count):
                self.ch_row_list.append(Create(self))
            self.move_2()
            self.count-=1
            self.canvas.itemconfig(self.count_text, text = "남은 수 "+str(self.count))
            self.i += 1
            self.Clear_ck()