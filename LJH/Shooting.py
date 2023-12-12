import tkinter
import random
import math
import os
from typing import List
from .GameBase import *

PLAYER_ACCELERATION = 700
BULLET_SPEED = 400

BULLET_SUMMON_DELAY = 0.3
AIM_BULLET_SUMMON_DELAY = 2

AING_ANIMATION_DELAY = 1

CLEAR_TIME = 10

PATH = os.path.dirname(os.path.abspath(__file__))

class Shooting(Game):
    def __init__(self, screen: tkinter.Canvas):
        super().__init__(screen)

        self.max_time = CLEAR_TIME

        self.background_image = tkinter.PhotoImage(file=f"{PATH}/image/Shooting/background.png")
        self.screen.create_image(WIDTH / 2, HEIGHT / 2, image=self.background_image)

        self.bullets : List[Bullet] = []
        self.player : Player = Player(self.screen, self, Vector(WIDTH / 2, HEIGHT / 2))
        self.player.position -= self.player.size / 2

        self.bullet_summon_time = 0
        self.aim_bullet_summon_time = 0

        self.update_screen()

    def summon_bullet(self):
        bullet = Bullet(self.screen, self)

        side = random.randint(0, 3)

        x = 0
        y = 0

        # top
        if side == 0:
            x = random.randint(0, WIDTH)
            y = -bullet.size.y
        # right
        elif side == 1:
            x = WIDTH
            y = random.randint(0, HEIGHT)
        # bottom
        elif side == 2:
            x = random.randint(0, WIDTH)
            y = HEIGHT
        # left
        elif side == 3:
            x = -bullet.size.x
            y = random.randint(0, HEIGHT)

        radian = random.random() * math.pi + (math.pi / 2) * side

        direction = Vector(math.cos(radian), math.sin(radian))

        bullet.position = Vector(x, y)
        bullet.velocity = direction * BULLET_SPEED
        
        self.bullets.append(bullet)
    
    def summon_aim_bullet(self):
        bullet = Bullet(self.screen, self)

        side = random.randint(0, 3)

        x = 0
        y = 0

        # top
        if side == 0:
            x = random.randint(0, WIDTH)
            y = -bullet.size.y
        # right
        elif side == 1:
            x = WIDTH
            y = random.randint(0, HEIGHT)
        # bottom
        elif side == 2:
            x = random.randint(0, WIDTH)
            y = HEIGHT
        # left
        elif side == 3:
            x = -bullet.size.x
            y = random.randint(0, HEIGHT)

        bullet.position = Vector(x, y)
        
        direction = (self.player.position - bullet.position).normalized()

        bullet.velocity = direction * BULLET_SPEED
        
        self.bullets.append(bullet)
        
    def update_game(self, dt: float):
        self.bullet_summon_time += dt
        self.aim_bullet_summon_time += dt

        while self.bullet_summon_time >= BULLET_SUMMON_DELAY:
            self.summon_bullet()
            self.bullet_summon_time -= BULLET_SUMMON_DELAY
        while self.aim_bullet_summon_time >= AIM_BULLET_SUMMON_DELAY:
            self.summon_aim_bullet()
            self.aim_bullet_summon_time -= AIM_BULLET_SUMMON_DELAY

        for bullet in self.bullets:
            bullet.update_game(dt)
        
        i = 0
        while i < len(self.bullets):
            if self.bullets[i].is_killed:
                self.bullets.pop(i)
            else:
                i += 1
        
        self.player.update_game(dt)

        for bullet in self.bullets:
            if self.player.collision_circle_rect(bullet):
                bullet.kill()
                self.is_gameover = True
                return
        
        if self.play_time >= CLEAR_TIME:
            self.is_clear = True
            self.is_gameover = True

    def update_screen(self):
        for bullet in self.bullets:
            bullet.update_screen()

        self.player.update_screen()


class Bullet(CircleGameObject):
    def __init__(self, screen: tkinter.Canvas, game : Shooting, position: Vector = Vector(0, 0)):
        super().__init__(screen, game, position)

        self.snow = tkinter.PhotoImage(file=f"{PATH}/image/Shooting/snow.png")

        self.size = Vector(20, 20)
        self.id = self.screen.create_image(0, 0, image=self.snow)

        self.radius = 10

    def update_game(self, dt: float):
        super().update_game(dt)

        if self.position.x < -self.size.x or self.position.x > WIDTH or self.position.y < -self.size.y or self.position.y > HEIGHT:
            self.kill()

class Player(CircleGameObject):
    def __init__(self, screen: tkinter.Canvas, game : Shooting, position: Vector = Vector(0, 0)):
        super().__init__(screen, game, position)

        self.aing_images = [tkinter.PhotoImage(file=f"{PATH}/image/Shooting/aing{i}.png") for i in range(2)]
        self.animation_time = 0

        self.size = Vector(60, 60)
        self.id = self.screen.create_image(0, 0, image=self.aing_images[0])

        self.radius = 30

        self.left_key = False
        self.right_key = False
        self.up_key = False
        self.down_key = False

        self.screen.bind("<KeyPress>", self.key_press)
        self.screen.bind("<KeyRelease>", self.key_release)
    
    def update_game(self, dt: float):
        self.animation_time += dt
        self.animation_time %= AING_ANIMATION_DELAY

        index = int(self.animation_time / AING_ANIMATION_DELAY * len(self.aing_images))
        self.screen.itemconfig(self.id, image=self.aing_images[index])

        dx = 0
        dy = 0

        if self.left_key:
            dx -= 1
        if self.right_key:
            dx += 1
        if self.up_key:
            dy -= 1
        if self.down_key:
            dy += 1
        
        self.velocity += Vector(dx, dy).normalized() * PLAYER_ACCELERATION * dt

        super().update_game(dt)

        if self.position.x < 0 or self.position.x + self.size.x > WIDTH or self.position.y < 0 or self.position.y + self.size.y > HEIGHT:
            self.position -= self.velocity * dt

    def key_press(self, e):
        if e.keysym == "Left":
            self.left_key = True
        elif e.keysym == "Right":
            self.right_key = True
        elif e.keysym == "Up":
            self.up_key = True
        elif e.keysym == "Down":
            self.down_key = True

    def key_release(self, e):
        if e.keysym == "Left":
            self.left_key = False
        elif e.keysym == "Right":
            self.right_key = False
        elif e.keysym == "Up":
            self.up_key = False
        elif e.keysym == "Down":
            self.down_key = False