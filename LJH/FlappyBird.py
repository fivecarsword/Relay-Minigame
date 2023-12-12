import tkinter
import random
import math
import os
from typing import List
from .GameBase import *

G = Vector(0, 1500)

JUMP_SPEED = 500

WALL_WIDTH = 70
WALL_SPEED = 150

HOLE_HEIGHT = 180
WALL_GAP = 500

CLEAR_TIME = 10

PATH = os.path.dirname(os.path.abspath(__file__))

class FlappyBird(Game):
    def __init__(self, screen: tkinter.Canvas):
        super().__init__(screen)

        self.max_time = CLEAR_TIME

        self.background1 = Background(self.screen, self)
        self.background2 = Background(self.screen, self)

        self.background2.position.x = self.background1.position.x + self.background1.size.x

        self.background1.other = self.background2
        self.background2.other = self.background1

        self.walls : List[Wall]= []

        x = WIDTH / 2 - 35
        hole_y = HEIGHT / 2 - HOLE_HEIGHT / 2

        self.add_wall(x, hole_y)

        self.bird : Bird = Bird(self.screen, self, Vector(WIDTH / 5, HEIGHT / 5))

        self.update_game(0)
        self.update_screen()

    def start(self):
        super().start()
        self.screen.bind("<space>", self.bird.jump)
        self.screen.bind("<Up>", self.bird.jump)
    
    def update_game(self, dt: float):        
        self.background1.update_game(dt)
        self.background2.update_game(dt)

        self.update_walls(dt)

        self.bird.update_game(dt)

        for wall in self.walls:
            if self.bird.collision_circle_rect(wall):
                self.is_gameover = True
                return
        
        if self.bird.position.y + self.bird.size.y > HEIGHT or self.bird.position.y < 0:
            self.is_gameover = True
            return

        if self.play_time >= CLEAR_TIME:
            self.is_clear = True
            self.is_gameover = True
    
    def update_screen(self):
        self.background1.update_screen()
        self.background2.update_screen()

        self.bird.update_screen()

        for wall in self.walls:
            wall.update_screen()

    def update_walls(self, dt):
        while self.walls[0].position.x < -WALL_WIDTH:
            wall = self.walls.pop(0)

            wall.kill()

        while self.walls[-1].position.x < WIDTH:
            x = self.walls[-1].position.x + WALL_GAP

            hole_y = random.randint(HEIGHT / 20, HEIGHT * 19 / 20 - HOLE_HEIGHT)

            self.add_wall(x, hole_y)

        for wall in self.walls:
            wall.update_game(dt)

    def add_wall(self, x, hole_y):
        wall = Wall(self.screen, self)
        wall.position = Vector(x, hole_y - wall.size.y)
        wall.velocity = Vector(-WALL_SPEED, 0)

        self.walls.append(wall)

        wall = Wall(self.screen, self)
        wall.position = Vector(x, hole_y + HOLE_HEIGHT)
        wall.velocity = Vector(-WALL_SPEED, 0)

        self.walls.append(wall)

    def jump(self, e):
        self.bird.jump()

class Bird(CircleGameObject):
    def __init__(self, screen: tkinter.Canvas, game : FlappyBird, position: Vector = Vector(0, 0)):
        super().__init__(screen, game, position)

        self.bird_images : tkinter.PhotoImage = [tkinter.PhotoImage(file=f"{PATH}/image/Flappy Bird/bird{i}.png") for i in range(9)]

        self.size = Vector(60, 60)
        self.radius = 30

        self.id = self.screen.create_image(0, 0, image=self.bird_images[0])
    
    def update_screen(self):
        super().update_screen()

        dy = min(self.velocity.y, 1.5 * JUMP_SPEED) + JUMP_SPEED
        index = round((dy / (2.5 * JUMP_SPEED)) * 8)

        self.screen.itemconfig(self.id, image=self.bird_images[index])

    def update_game(self, dt: float):
        super().update_game(dt)

        self.velocity += G * dt
    
    def jump(self, e):
        self.velocity.y = -JUMP_SPEED

class Wall(GameObject):
    def __init__(self, screen: tkinter.Canvas, game : FlappyBird, position: Vector = Vector(0, 0)):
        super().__init__(screen, game, position)

        index = random.randrange(0, 2)

        self.image = tkinter.PhotoImage(file=f"{PATH}/image/Flappy Bird/wall{index}.png")

        self.size = Vector(self.image.width(), self.image.height())
    
        self.id = self.screen.create_image(0, 0, image=self.image)

class Background(GameObject):
    def __init__(self, screen: tkinter.Canvas, game: FlappyBird, position: Vector = Vector(0, 0)):
        super().__init__(screen, game, position)

        self.other : Background= None

        self.image = tkinter.PhotoImage(file=f"{PATH}/image/Flappy Bird/background.png")

        self.size = Vector(self.image.width(), self.image.height())

        self.id = self.screen.create_image(0, 0, image=self.image)

        self.velocity = Vector(-WALL_SPEED / 2, 0)

    def update_game(self, dt: float):
        super().update_game(dt)

        if self.position.x + self.size.x < 0:
            self.other.position.x = 0
            self.position.x = self.other.position.x + self.other.size.x - 2
