import tkinter
import tkinter.font
import random
import sys
from typing import List

from LJH import *
from LJH.GameBase import Game, Vector

WIDTH = 1280
HEIGHT = 720

SWITCH_TIME = 2

BUTTON_SIZE = Vector(200, 60)

IMAGE_SPEED_MIN = 200
IMAGE_SPEED_MAX = 400

IMAGE_SUMMON_DELAY = 0.3

BUTTON_COLOR = "green3"
ACTIVE_COLOR = "green2"

message_font = ("Impact", 150,)
grade_font = ("Gill Sans", 180, "bold")
info_font = ("Consolas", 30)
button_font = ("Consolas", 35)

class Start(Game):
    def __init__(self, screen: tkinter.Canvas, start_command, exit_command, switch_bgm_command, is_playing_bgm):
        super().__init__(screen)

        self.start_command = start_command
        self.exit_command = exit_command
        self.switch_bgm_command = switch_bgm_command

        self.title_image = tkinter.PhotoImage(file="image/title.png")
        self.title_id = self.screen.create_image(WIDTH / 2, HEIGHT / 3, image=self.title_image)

        self.backgroud_image = tkinter.PhotoImage(file="image/background.png")

        self.background1 = Background(self.screen, self, self.backgroud_image)
        self.background2 = Background(self.screen, self, self.backgroud_image)

        self.background1.velocity = Vector((IMAGE_SPEED_MIN + IMAGE_SPEED_MAX) / 2, 0)
        self.background2.velocity = Vector((IMAGE_SPEED_MIN + IMAGE_SPEED_MAX) / 2, 0)

        self.background2.position.x = self.background1.position.x + self.background1.size.x

        self.background1.other = self.background2
        self.background2.other = self.background1

        self.start_id = None
        self.exit_id = None

        self.images = load_all_images()

        self.image_objects : List[ImageObject] = []

        self.image_summon_time = 0

        self.is_playing_bgm = is_playing_bgm

        self.bgm_on_image = tkinter.PhotoImage(file="image/bgm_on.png")
        self.bgm_off_image = tkinter.PhotoImage(file="image/bgm_off.png")

        self.update_screen()

    def start(self):
        super().start()

        self.start_button = tkinter.Button(self.screen, text="Start", font=button_font, bg=BUTTON_COLOR, activebackground=ACTIVE_COLOR, relief="solid", overrelief="groove", cursor="hand2", command=self.run_start)
        self.exit_button = tkinter.Button(self.screen, text="Exit", font=button_font, bg=BUTTON_COLOR, activebackground=ACTIVE_COLOR, relief="solid", overrelief="groove", cursor="hand2", command=self.exit_command)
        
        bgm_image = self.bgm_on_image if self.is_playing_bgm else self.bgm_off_image
        self.bgm_button = tkinter.Button(self.screen, image = bgm_image, font=button_font, bg=BUTTON_COLOR, activebackground=ACTIVE_COLOR, relief="solid", overrelief="groove", cursor="hand2", command=self.switch_bgm)

        self.start_id = self.screen.create_window(WIDTH / 2, HEIGHT / 2 + 2 * BUTTON_SIZE.y, width = BUTTON_SIZE.x, height = BUTTON_SIZE.y, window = self.start_button)
        self.exit_id = self.screen.create_window(WIDTH / 2, HEIGHT / 2 + 3 * BUTTON_SIZE.y + 20, width = BUTTON_SIZE.x, height = BUTTON_SIZE.y, window = self.exit_button)
        self.bgm_id = self.screen.create_window(WIDTH / 2 + BUTTON_SIZE.x / 2 + 50, HEIGHT / 2 + 3 * BUTTON_SIZE.y + 20, width=60, height=60, window=self.bgm_button)
    
    def update_game(self, dt: float):
        self.background1.update_game(dt)
        self.background2.update_game(dt)
        
        self.image_summon_time += dt

        while self.image_summon_time >= IMAGE_SUMMON_DELAY:
            self.image_summon_time -= IMAGE_SUMMON_DELAY
            self.summon_image_object()

        i = 0
        while i < len(self.image_objects):
            self.image_objects[i].update_game(dt)

            if self.image_objects[i].is_killed:
                self.image_objects.pop(i)
            else:
                i += 1

    def update_screen(self):
        self.screen.tag_raise(self.title_id)

        self.background1.update_screen()
        self.background2.update_screen()
        
        for ob in self.image_objects:
            ob.update_screen()

    def run_start(self):
        self.is_gameover = True
        self.start_command()
        self.screen.delete(self.start_id)
        self.screen.delete(self.exit_id)
        self.screen.delete(self.bgm_id)
    
    def switch_bgm(self):
        self.switch_bgm_command()
        self.is_playing_bgm ^= True

        if self.is_playing_bgm:
            self.bgm_button.config(image=self.bgm_on_image)
        else:
            self.bgm_button.config(image=self.bgm_off_image)

    def summon_image_object(self):
        index = random.randrange(0, len(self.images))

        ob = ImageObject(self.screen, self, self.images[index])
        
        y = random.randint(0, HEIGHT - ob.size.y)
        ob.position = Vector(- ob.size.x, y)
        ob.velocity = Vector(random.randint(IMAGE_SPEED_MIN, IMAGE_SPEED_MAX), 0)

        self.image_objects.append(ob)

class Result(Game):
    def __init__(self, screen: tkinter.Canvas, back_command, score : int, play_time : int):
        super().__init__(screen)

        self.back_command = back_command

        self.backgroud_image = tkinter.PhotoImage(file="image/background.png")

        self.background1 = Background(self.screen, self, self.backgroud_image)
        self.background2 = Background(self.screen, self, self.backgroud_image)

        self.background1.velocity = -Vector((IMAGE_SPEED_MIN + IMAGE_SPEED_MAX) / 2, 0)
        self.background2.velocity = -Vector((IMAGE_SPEED_MIN + IMAGE_SPEED_MAX) / 2, 0)

        self.background2.position.x = self.background1.position.x + self.background1.size.x

        self.background1.other = self.background2
        self.background2.other = self.background1

        self.board_image = tkinter.PhotoImage(file="image/board.png")
        self.board_id = self.screen.create_image(WIDTH / 2, HEIGHT / 3, image=self.board_image)

        self.score = score
        self.play_time = int(play_time)

        h = self.play_time // 3600
        self.play_time %= 3600
        m = self.play_time // 60
        self.play_time %= 60
        s = self.play_time

        self.score_id = self.screen.create_text(WIDTH / 2, HEIGHT / 2 - 30, text=f"Score {self.score}", font=info_font)
        self.play_time_id = self.screen.create_text(WIDTH / 2, HEIGHT / 2 + 30, text="%02d:%02d:%02d" % (h, m, s), font=info_font)

        grade = "F"

        if self.score >= 50:
            grade = "S"
        elif self.score >= 30:
            grade = "A"
        elif self.score >= 20:
            grade = "B"
        elif self.score >= 10:
            grade = "C"
        elif self.score >= 5:
            grade = "D"

        self.grade_id = self.screen.create_text(WIDTH / 2, HEIGHT / 4, text=grade, font=grade_font)

        self.back_id = None

        self.images = load_all_images()

        self.image_objects : List[ImageObject] = []

        self.image_summon_time = 0

        self.update_screen()
    
    def start(self):
        super().start()
        back_button = tkinter.Button(self.screen, text="Back", font=button_font, bg=BUTTON_COLOR, activebackground=ACTIVE_COLOR, relief="solid", overrelief="groove", cursor="hand2", command=lambda : (self.back_command(), self.over()))
        self.back_id = self.screen.create_window(WIDTH / 2, HEIGHT * 3 / 4, width=BUTTON_SIZE.x, height=BUTTON_SIZE.y, window=back_button)
    
    def update_game(self, dt: float):
        self.background1.update_game(dt)
        self.background2.update_game(dt)

        self.image_summon_time += dt

        while self.image_summon_time >= IMAGE_SUMMON_DELAY:
            self.image_summon_time -= IMAGE_SUMMON_DELAY
            self.summon_image_object()

        i = 0
        while i < len(self.image_objects):
            self.image_objects[i].update_game(dt)

            if self.image_objects[i].is_killed:
                self.image_objects.pop(i)
            else:
                i += 1

    def update_screen(self):
        self.background1.update_screen()
        self.background2.update_screen()

        for ob in self.image_objects:
            ob.update_screen()
        
        self.screen.tag_raise(self.board_id)
        self.screen.tag_raise(self.score_id)
        self.screen.tag_raise(self.play_time_id)
        self.screen.tag_raise(self.grade_id)

    def over(self):
        self.is_gameover = True
        self.screen.delete(self.back_id)
    
    def summon_image_object(self):
        index = random.randrange(0, len(self.images))

        ob = ImageObject(self.screen, self, self.images[index])
        
        y = random.randint(0, HEIGHT - ob.size.y)
        ob.position = Vector(WIDTH, y)
        ob.velocity = - Vector(random.randint(IMAGE_SPEED_MIN, IMAGE_SPEED_MAX), 0)

        self.image_objects.append(ob)

class ImageObject(GameObject):
    def __init__(self, screen: tkinter.Canvas, game: Game, image: tkinter.PhotoImage, position: Vector = Vector(0, 0)):
        super().__init__(screen, game, position)

        self.image = image
        self.id = self.screen.create_image(-WIDTH, -HEIGHT, image=self.image)
        self.size = Vector(self.image.width(), self.image.height())
    
    def update_game(self, dt: float):
        super().update_game(dt)

        if self.position.x + self.size.x < 0 or self.position.x > WIDTH or self.position.y + self.size.y < 0 or self.position.y > HEIGHT:
            self.kill()

class Background(GameObject):
    def __init__(self, screen: tkinter.Canvas, game: Game, image, position: Vector = Vector(0, 0)):
        super().__init__(screen, game, position)

        self.other : Background = None

        self.image = image

        self.size = Vector(self.image.width(), self.image.height())

        self.id = self.screen.create_image(0, 0, image=self.image)

    def update_game(self, dt: float):
        super().update_game(dt)

        if self.velocity.x < 0 and self.position.x + self.size.x < 0:
            self.other.position.x = 0
            self.position.x = self.other.position.x + self.other.size.x - 8
        elif self.velocity.x > 0 and self.position.x > self.size.x:
            self.other.position.x = 0
            self.position.x = self.other.position.x - self.other.size.x + 8

class Blind:
    def __init__(self, screen : tkinter.Canvas, game, life, score):
        self.screen : tkinter.Canvas = screen
        self.game = None

        self.heart_image = tkinter.PhotoImage(file="image/heart.png")

        self.rect = self.screen.create_rectangle(-10, 0, WIDTH, HEIGHT, fill="black")
        self.message = self.screen.create_text(WIDTH / 2, HEIGHT / 2, font=message_font)

        self.heart_size = Vector(60, 60)
        self.heart_pos = Vector(WIDTH / 2 - self.heart_size.x * 2, HEIGHT * 3 / 4 - 30)

        self.hearts = []

        self.score = self.screen.create_text(0, 0, font=info_font, fill="white")

        self.update_info(game, life, score)

        self.update(-100)
    
    def update_info(self, game, life = None, score = None):
        self.game = game

        text = ""

        color = "black"

        self.hearts.clear()

        score_text = ""

        if self.game != None:
            if self.game.is_clear:
                text = "CLEAR"
                color = "yellow"
            else:
                text = "FAIL"
                color = "gray"
            
            for i in range(life):
                id = self.screen.create_image(0, 0, image=self.heart_image)
                
                self.screen.moveto(id, 0, - HEIGHT)

                self.hearts.append(id)

            score_text = str(score)
            
        self.screen.itemconfig(self.score, text=score_text)

        self.screen.itemconfig(self.message, text=text, fill=color)

    def update(self, dt):
        y = 0

        if dt <= SWITCH_TIME * 2 / 3:
            percent = 3 * dt / SWITCH_TIME

            y = min(percent * HEIGHT - HEIGHT, 0)
        elif dt <= SWITCH_TIME:
            percent = 3 * (dt - SWITCH_TIME * 2 / 3) / SWITCH_TIME

            y = - percent * HEIGHT
        else:
            y = HEIGHT
        
        self.screen.moveto(self.rect, -5, y)
        self.screen.coords(self.message, WIDTH / 2, y + HEIGHT / 2)
        self.screen.coords(self.score, WIDTH / 2, self.heart_pos.y + self.heart_size.y + 40 + y)
        
        self.screen.tag_raise(self.rect)
        self.screen.tag_raise(self.message)
        self.screen.tag_raise(self.score)

        for i, id in enumerate(self.hearts):
            self.screen.moveto(id, self.heart_pos.x + self.heart_size.x * i * 1.5, self.heart_pos.y + y)

            self.screen.tag_raise(id)

def load_all_images():
    lst = []

    l = lambda file : lst.append(tkinter.PhotoImage(file=path+file+".png"))

    path = "LJH/image/Flappy Bird/"

    for i in range(9):
        l(f"bird{i}")
    l("wall0")
    l("wall1")

    path = "LJH/image/Maze/"

    l("box")
    l("santa")

    path = "LJH/image/Rhythm/"

    for i in range(4):
        l(f"dance{i}")
    for i in range(10):
        l(f"gift{i}")
    for i in range(4):
        l(f"note{i}")
    for i in range(4):
        l(f"pad{i}")

    path = "LJH/image/Shooting/"

    l("aing0")
    l("aing1")
    l("snow")

    path = "SYC/image/Jump/"

    l("Plant3")

    path = "SYC/image/Moskito/"

    l("Moskito.1")

    path = "SYH/image/Avoid DDong/"

    l("ddong")
    l("ddong2")
    l("left1")
    l("left2")
    l("right1")
    l("right2")
    l("stand1")
    l("stand2")

    path = "SYH/image/Classification/"

    l("냥1")
    l("냥2")
    l("멍1")
    l("멍2")
    l("인1")
    l("인2")

    path = "SYH/image/Race/"

    for i in range(1, 8):
        l(f"horse_{i}")

    return lst