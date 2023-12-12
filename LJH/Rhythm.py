import tkinter
import random
import math
import os
from typing import List

from LJH.GameBase import Game, Vector

from .GameBase import *

NOTE_SIZE = Vector(80, 80)

NOTE_TIME = 2

NOTE_SUMMON_DELAY = 0.25
NOTE_SUMMON_PROBABLITY = 0.4

STAND_DELAY = 0.4

LEFT = 0
DOWN = 1
UP = 2
RIGHT = 3

G = 600
GIFT_SPEED = 700

CLEAR_TIME = 10

PATH = os.path.dirname(os.path.abspath(__file__))

class Rhythm(Game):
    def __init__(self, screen: tkinter.Canvas):
        super().__init__(screen)

        self.max_time = CLEAR_TIME

        self.background_image = tkinter.PhotoImage(file=f"{PATH}/image/Rhythm/background.png")
        screen.create_image(WIDTH / 2, HEIGHT / 2, image=self.background_image)

        self.dance_images = [tkinter.PhotoImage(file=f"{PATH}/image/Rhythm/dance{i}.png") for i in range(5)]

        self.dance_id = self.screen.create_image(WIDTH / 2, HEIGHT * 2 / 3, image=self.dance_images[4])

        self.dance_time = 0

        self.note_lists : List[List[Note]] = [[], [], [], []]

        self.missed_notes : List[Note] = []

        self.pads_position = Vector(WIDTH / 2 - NOTE_SIZE.x * 2.75, NOTE_SIZE.y * 1.2)
        self.pads : List[Pad] = []

        self.note_summon_time = 0

        self.note_images = [tkinter.PhotoImage(file=f"{PATH}/image/Rhythm/note{i}.png") for i in range(4)]
        self.pad_images = [tkinter.PhotoImage(file=f"{PATH}/image/Rhythm/pad{i}.png") for i in range(4)]

        for i in range(4):
            pad = Pad(self.screen, self, i, self.note_lists[i], self.pads_position + Vector(NOTE_SIZE.x, 0) * i * 1.5)
            pad.update_screen()

            self.pads.append(pad)
        
        self.gifts : List[Gift] = []

        self.screen.bind("<space>", lambda e : self.summon_gift())
    
    def start(self):
        super().start()

        self.screen.bind("<KeyPress-Left>", self.pads[0].press)
        self.screen.bind("<KeyRelease-Left>", self.pads[0].release)

        self.screen.bind("<KeyPress-Down>", self.pads[1].press)
        self.screen.bind("<KeyRelease-Down>", self.pads[1].release)

        self.screen.bind("<KeyPress-Up>", self.pads[2].press)
        self.screen.bind("<KeyRelease-Up>", self.pads[2].release)

        self.screen.bind("<KeyPress-Right>", self.pads[3].press)
        self.screen.bind("<KeyRelease-Right>", self.pads[3].release)

    
    def update_game(self, dt: float):
        self.note_summon_time += dt

        for notes in self.note_lists:
            for note in notes:
                note.update_game(dt)
        
        i = 0
        while i < len(self.missed_notes):
            note = self.missed_notes[i]
            
            note.update_game(dt)

            if note.position.y + note.offset.y + note.size.y < 0:
                note.kill()
                self.missed_notes.pop(i)

                self.is_gameover = True
            else:
                i += 1     

        for pad in self.pads:
            pad.update_game(dt)
        
        while self.note_summon_time >= NOTE_SUMMON_DELAY:
            self.note_summon_time -= NOTE_SUMMON_DELAY
            self.summon_note()

        self.dance_time += dt

        if self.dance_time >= STAND_DELAY:
            self.dance_time = 0
            self.screen.itemconfig(self.dance_id, image=self.dance_images[4])
        
        i = 0
        while i < len(self.gifts):
            self.gifts[i].update_game(dt)

            if self.gifts[i].is_killed:
                self.gifts.pop(i)
            else:
                i += 1

        if self.play_time >= CLEAR_TIME:
            self.is_clear = True
            self.is_gameover = True

    def update_screen(self):
        for notes in self.note_lists:
            for note in notes:
                note.update_screen()

        for note in self.missed_notes:
            note.update_screen()

        for gift in self.gifts:
            gift.update_screen()
    
    def summon_note(self):
        if random.random() <= NOTE_SUMMON_PROBABLITY:
            arrow = random.randrange(0, 4)
            self.note_lists[arrow].append(Note(self.screen, self, arrow, self.pads[arrow].position))
    
    def summon_gift(self):
        gift = Gift(self.screen, self, Vector(WIDTH, HEIGHT))
        gift.velocity = Vector(-random.random() * 0.7 - 0.3, -random.random() * 0.7 - 0.3).normalized() * GIFT_SPEED
        gift.update_screen()

        self.gifts.append(gift)

        gift = Gift(self.screen, self, Vector(0, HEIGHT))
        gift.position -= Vector(gift.size.x, 0)
        gift.velocity = Vector(random.random() / 2 + 0.5, -random.random() / 2 - 0.5).normalized() * GIFT_SPEED
        gift.update_screen()

        self.gifts.append(gift)

class Pad(GameObject):
    def __init__(self, screen: tkinter.Canvas, game: Game, arrow : int, notes : List["Note"], position: Vector = Vector(0, 0)):
        super().__init__(screen, game, position)

        self.arrow = arrow
        self.notes = notes

        self.size = NOTE_SIZE

        self.pressed = False

        self.id = screen.create_image(0, 0, image=self.game.pad_images[arrow])
    
    def update_game(self, dt: float):
        super().update_game(dt)
        
        if len(self.notes) > 0 and self.notes[0].offset.y < 0 and not self.notes[0].check_correct():
            self.game.missed_notes.append(self.notes.pop(0))

    def press(self, e):
        if self.pressed:
            return
        
        if len(self.notes) > 0 and self.notes[0].check_correct():
            self.screen.itemconfig(self.game.dance_id, image=self.game.dance_images[self.arrow])
            self.game.dance_time = 0
            self.notes.pop(0).kill()
            self.game.summon_gift()

        self.pressed = True

    def release(self, e):
        self.pressed = False


class Note(GameObject):
    def __init__(self, screen: tkinter.Canvas, game: Game, arrow : int, position: Vector = Vector(0, 0)):
        super().__init__(screen, game, position)

        self.arrow = arrow

        self.time = 0
        
        self.size = NOTE_SIZE

        self.id = screen.create_image(0, 0, image=self.game.note_images[arrow])

        self.offset = Vector(0, HEIGHT)

    def check_correct(self) -> bool:
        if abs(self.offset.y) <= self.size.y:
            return True
        
        return False
    
    def update_game(self, dt: float):
        super().update_game(dt)

        self.time += dt
        
        self.offset = Vector(0, HEIGHT) - HEIGHT * Vector(0, self.time / NOTE_TIME)

class Gift(GameObject):
    def __init__(self, screen: tkinter.Canvas, game: Game, position: Vector = Vector(0, 0)):
        super().__init__(screen, game, position)

        self.image = tkinter.PhotoImage(file=f"{PATH}/image/Rhythm/gift{random.randrange(0, 10)}.png")

        self.id = self.screen.create_image(0, 0, image=self.image)
        self.size = Vector(50, 50)

    def update_game(self, dt: float):
        super().update_game(dt)

        self.velocity += Vector(0, 1) * G * dt

        if self.position.y > HEIGHT:
            self.kill()