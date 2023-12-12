import tkinter

import time

WIDTH = 1280
HEIGHT = 720

class Vector:
    def __init__(self, x : float = 0, y : float = 0):
        self.x : float = x
        self.y : float = y

    def __round__(self):
        return Vector(round(self.x), round(self.y))

    def __eq__(self, other : "Vector") -> bool:
        if (self.x == other.x and self.y == other.y):
            return True
        return False

    def __add__(self, other : "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other : "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __pos__(self) -> "Vector":
        return Vector(self.x, self.y)

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y)

    def __mul__(self, other : float) -> "Vector":
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other : float) -> "Vector":
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other : float) -> "Vector":
        return Vector(self.x / other, self.y / other)

    def __floordiv__(self, other : float) -> "Vector":
        return Vector(self.x // other, self.y // other)

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def copy(self) -> "Vector":
        return Vector(self.x, self.y)

    def length(self) -> float:
        return (self.x * self.x + self.y * self.y) ** 0.5

    def normalized(self) -> "Vector":
        if self.x == 0 and self.y == 0:
            return Vector(0, 0)
        return self / self.length()
    
    def normalize(self) -> None:
        if self.x == 0 and self.y == 0:
            return
        length = self.length()

        self.x /= length
        self.y /= length

class Game:
    def __init__(self, screen : tkinter.Canvas):
        self.screen : tkinter.Canvas = screen

        self.is_clear : bool = False
        self.is_gameover : bool = False

        self.play_time = 0
        self.max_time = 0

        self.is_countdown = False

        self.pre_time = 0
    
    def start(self):
        self.pre_time = time.time()
        self.update()

    def update(self):
        if self.is_gameover:
            return
        
        cur_time = time.time()

        dt = cur_time - self.pre_time
        self.pre_time = cur_time

        self.play_time += dt

        self.update_game(dt)
        
        self.update_screen()

        self.screen.after(1, self.update)

    def update_game(self, dt : float):
        pass

    def update_screen(self):
        pass

class GameObject:
    def __init__(self, screen : tkinter.Canvas, game : Game, position : Vector = Vector(0, 0)):
        self.id : int = ""

        self.screen : tkinter.Canvas = screen
        self.game = game

        self.position : Vector = position.copy()
        self.pre_position : Vector = position + Vector(10, 10)
        self.velocity : Vector = Vector()
        self.size : Vector = Vector()

        self.offset : Vector = Vector()

        self.is_killed : bool = False

    def kill(self):
        self.screen.delete(self.id)
        self.is_killed = True

    def update_game(self, dt : float):
        self.position += self.velocity * dt

    def update_screen(self):
        pos = round(self.position + self.offset)
        if self.pre_position != pos:
            self.pre_position = pos
            self.screen.moveto(self.id, pos.x, pos.y)

    def collision(self, other : "GameObject") -> bool:
        if (self.position.x <= other.position.x <= self.position.x + self.size.x or other.position.x <= self.position.x <= other.position.x + other.size.x) and (self.position.y <= other.position.y <= self.position.y + self.size.y or other.position.y <= self.position.y <= other.position.y + other.size.y):
            return True

        return False

class CircleGameObject(GameObject):
    def __init__(self, screen: tkinter.Canvas, game : Game, position: Vector = Vector(0, 0)):
        super().__init__(screen, game, position)

        self.radius = 0
    
    def collision_circle_rect(self, other : GameObject):
        p = self.position + self.size / 2

        if p.x < other.position.x:
            p.x = other.position.x
        elif p.x > other.position.x + other.size.x:
            p.x = other.position.x + other.size.x
        if p.y < other.position.y:
            p.y = other.position.y
        elif p.y > other.position.y + other.size.y:
            p.y = other.position.y + other.size.y
        
        if (self.position + self.size / 2 - p).length() <= self.radius:
            return True

        return False

    def collision_circle_circle(self, other : "CircleGameObject"):
        if (self.position - other.position).length() < self.radius + other.radius:
            return True
        
        return False