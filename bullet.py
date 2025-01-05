import pygame

class Bullet:
    def __init__(self, size, x: int, y: int, speedX: int, speedY: int, color: tuple[int, int, int]):
        self.size: int = size
        self.x: int = x
        self.y: int = y
        self.speedX: int = speedX
        self.speedY: int = speedY
        self.color: tuple[int, int, int] = color

    def move(self):
        self.x += self.speedX
        self.y += self.speedY

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)
