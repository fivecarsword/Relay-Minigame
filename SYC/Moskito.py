# 직접 작성
import tkinter 
import random
import math
import time
import os

width = 1280
height = 720

GAMEOVER_TIME = 10

PATH = os.path.dirname(os.path.abspath(__file__))

class Moskito:
    def __init__(self, canvas):
        self.is_clear = False
        self.is_gameover = False

        self.play_time = 0
        self.max_time = GAMEOVER_TIME

        self.is_countdown = True

        self.next_move = None

        self.cvs = canvas
        
        # 유튜브 영상 인용
        self.moskito_img = tkinter.PhotoImage(file = f"{PATH}/image/Moskito/Moskito.1.png")
        self.button = tkinter.Button(self.cvs, image= self.moskito_img, command=self.clicked)
        # 직접 작성
        self.screen_img = tkinter.PhotoImage(file=f"{PATH}/image/Moskito/living room.png")
        self.cvs.create_image(width/2, height/2, image = self.screen_img) 

    def start(self):
        self.btn_move()
        self.Time_check()

    def clicked(self):
        self.cvs.after_cancel(self.next_move)
        self.Clear()
    # 유튜브 영상 인용
    def btn_move(self):
        if self.is_gameover:
            return
        
        speed_x = random.randint(20, 1260)
        speed_y = random.randint(20, 700)
        delay = random.randint(500, 1000)
        self.button.place(x=speed_x, y=speed_y)
        self.next_move = self.cvs.after(delay, self.btn_move)
        end = time.time()
    # 직접 작성
    def Time_check(self):
        if self.is_gameover:
            return

        if(self.play_time >= GAMEOVER_TIME):
            self.Gameover()
        self.play_time+=1
        self.cvs.after(1000, self.Time_check)
        
    def Clear(self):
        self.is_clear = True
        self.is_gameover = True
        self.button.place_forget()

    def Gameover(self):
        self.is_gameover = True
        self.button.place_forget()

#유튜브  https://www.youtube.com/watch?v=ppcfsrJmgxM&list=LL&index=2
'''
모기
"https://kr.freepik.com/free-vector/sticker-design-with-a-mosquito-cartoon-character-isolated_19747425.htm#query=%EB%AA%A8%EA%B8%B0&position=0&from_view=search&track=sph&uuid=e3084b27-c608-4add-af95-cd89e771a5f4"
배경
"https://www.freepik.com/free-vector/living-room-interior-composition-with-indoor-view-modern-apartment-with-wall-paintings-pot-plants-vector-illustration_32471936.htm#page=3&query=living%20room&position=24&from_view=search&track=ais&uuid=aec00963-6e9e-40f1-bb52-f9a0b85a352d"

출처 Freepik
'''