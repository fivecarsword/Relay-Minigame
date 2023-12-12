import tkinter
import random
import math
import os
from typing import List
from .GameBase import * 

MAZE_WIDTH = 14
MAZE_HEIGHT = 7

PLAYER_SPEED = 10
GAMEOVER_TIME = 20

PATH = os.path.dirname(os.path.abspath(__file__))

class Maze(Game):
    def __init__(self, screen: tkinter.Canvas):
        super().__init__(screen)

        self.max_time = GAMEOVER_TIME

        self.is_countdown = True

        self.maze = [[True] * (2 * MAZE_WIDTH - 1) for _ in range(2 * MAZE_HEIGHT - 1)]

        start_pos = Vector(random.randrange(0, MAZE_WIDTH), random.randrange(0, MAZE_HEIGHT))
        self.maze[start_pos.y * 2][start_pos.x * 2] = False

        self.stack = [(start_pos, [Vector(1, 0), Vector(-1, 0), Vector(0, 1), Vector(0, -1)])]

        self.block_size = Vector(WIDTH / (MAZE_WIDTH + 2), HEIGHT / (MAZE_HEIGHT + 2))
        self.offset = self.block_size.copy()

        self.snow = [[False] * (2 * MAZE_WIDTH - 1) for _ in range(2 * MAZE_HEIGHT - 1)]

        self.floor_images = [tkinter.PhotoImage(file=f"{PATH}/image/Maze/floor{i}.png") for i in range(16)]

        self.floors = [[None] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]

        for i in range(MAZE_HEIGHT):
            for j in range(MAZE_WIDTH):
                id = self.screen.create_image(0, 0, image=self.floor_images[0])
                pos = Vector(self.block_size.x * j, self.block_size.y * i) + self.offset 
                self.screen.moveto(id, pos.x, pos.y)

                self.floors[i][j] = id

        self.box = tkinter.PhotoImage(file=f"{PATH}/image/Maze/box.png")

        self.screen.create_image(self.block_size.x * MAZE_WIDTH + self.block_size.x / 2, self.block_size.y * MAZE_HEIGHT + self.block_size.y / 2, image = self.box)

        self.screen.create_rectangle(self.block_size.x, self.block_size.y, WIDTH - self.block_size.x, HEIGHT - self.block_size.y, width=3)

        for i in range(MAZE_HEIGHT):
            for j in range(MAZE_WIDTH - 1):
                p0 = Vector(self.block_size.x * (j + 1), self.block_size.y * i) + self.offset
                p1 = Vector(self.block_size.x * (j + 1), self.block_size.y * (i + 1)) + self.offset

                self.screen.create_line(p0.x, p0.y, p1.x, p1.y, fill="black", width=3, tags=f"{i * 2},{1 + j * 2}")
                    
        for i in range(MAZE_HEIGHT - 1):
            for j in range(MAZE_WIDTH):
                p0 = Vector(self.block_size.x * j, self.block_size.y * (i + 1)) + self.offset
                p1 = Vector(self.block_size.x * (j + 1), self.block_size.y * (i + 1)) + self.offset
                
                self.screen.create_line(p0.x, p0.y, p1.x, p1.y, fill="black", width=3, tags=f"{1 + i * 2},{j * 2}")

        self.player : Player = Player(self.screen, self)

        self.update_game(0)
        self.update_screen()

    def start(self):
        self.generate_maze()
    
    def update_game(self, dt: float):
        self.player.update_game(dt)

        if self.player.maze_position == Vector(MAZE_WIDTH - 1, MAZE_HEIGHT - 1):
            self.is_clear = True
            self.is_gameover = True
        
        if self.play_time >= GAMEOVER_TIME:
            self.is_gameover = True
    
    def update_screen(self):
        self.player.update_screen()
        
    def generate_maze(self):
        if len(self.stack) == 0:
            super().start()
            return
        
        pos, offsets = self.stack[-1]

        self.screen.after(5, self.generate_maze)

        if len(offsets) == 0:
            self.stack.pop()
            return
        
        while len(offsets) != 0:
            offset = offsets.pop(random.randrange(0, len(offsets)))

            next_pos = pos + offset

            if 0 <= next_pos.x < MAZE_WIDTH and 0 <= next_pos.y < MAZE_HEIGHT and self.maze[next_pos.y * 2][next_pos.x * 2]:
                self.maze[next_pos.y * 2][next_pos.x * 2] = False
                self.maze[pos.y * 2 + offset.y][pos.x * 2 + offset.x] = False

                self.screen.delete(f"{pos.y * 2 + offset.y},{pos.x * 2 + offset.x}")

                self.stack.append((next_pos, [Vector(1, 0), Vector(-1, 0), Vector(0, 1), Vector(0, -1)]))

                return

    def check_snow(self, maze_x, maze_y):
        # up right down left
        result = [False, False, False, False]

        if maze_y != 0:
            result[0] = self.snow[2 * maze_y - 1][2 * maze_x]
        
        if maze_x != MAZE_WIDTH - 1:
            result[1] = self.snow[2 * maze_y][2 * maze_x + 1]
        
        if maze_y != MAZE_HEIGHT - 1:
            result[2] = self.snow[2 * maze_y + 1][2 * maze_x]

        if maze_x != 0:
            result[3] = self.snow[2 * maze_y][2 * maze_x - 1]

        return result

    def update_floor(self, maze_x, maze_y):
        walls = self.check_snow(maze_x, maze_y)

        index = 0

        for i, j in enumerate((1, 2, 4, 8)):
            index += (walls[i]) * j
        
        self.screen.itemconfig(self.floors[maze_y][maze_x], image=self.floor_images[index])

class Player(GameObject):
    def __init__(self, screen: tkinter.Canvas, game: Maze, position: Vector = Vector(0, 0)):
        super().__init__(screen, game, position)

        self.maze_position = Vector()

        self.left_key = False
        self.right_key = False
        self.up_key = False
        self.down_key = False

        self.screen.bind("<KeyPress>", self.key_press)
        self.screen.bind("<KeyRelease>", self.key_release)

        self.dx = 0
        self.dy = 0

        self.santa = tkinter.PhotoImage(file=f"{PATH}/image/Maze/santa.png")

        self.size = Vector(self.santa.width(), self.santa.height())
        self.id = self.screen.create_image(0, 0, image = self.santa)

    def update_game(self, dt: float):
        super().update_game(dt)

        dx = 0
        dy = 0

        if self.left_key:
            self.dx -= PLAYER_SPEED * dt
        if self.right_key:
            self.dx += PLAYER_SPEED * dt
        if self.up_key:
            self.dy -= PLAYER_SPEED * dt
        if self.down_key:
            self.dy += PLAYER_SPEED * dt

        if self.dx >= 1:
            self.dx = 0
            dx = 1
        elif self.dx <= -1:
            self.dx = 0
            dx = -1
        if self.dy >= 1:
            self.dy = 0
            dy = 1
        elif self.dy <= -1:
            self.dy = 0
            dy = -1

        x = self.maze_position.x
        y = self.maze_position.y

        if 0 <= x + dx < MAZE_WIDTH and not self.game.maze[y * 2][x * 2 + dx]:
            self.maze_position.x += dx

            self.game.snow[2 * y][2 * x] = True
            self.game.snow[2 * y][2 * (x + dx)] = True
            self.game.snow[2 * y][2 * x + dx] = True

            self.game.update_floor(x, y)
            self.game.update_floor(x + dx, y)

        x = self.maze_position.x
        y = self.maze_position.y

        if 0 <= y + dy < MAZE_HEIGHT and not self.game.maze[y * 2 + dy][x * 2]:
            self.maze_position.y += dy

            self.game.snow[2 * y][2 * x] = True
            self.game.snow[2 * (y + dy)][2 * x] = True
            self.game.snow[2 * y + dy][2 * x] = True
        
            self.game.update_floor(x, y)
            self.game.update_floor(x, y + dy)

        self.position.x = self.maze_position.x * self.game.block_size.x
        self.position.y = self.maze_position.y * self.game.block_size.y

        self.position += self.game.offset

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