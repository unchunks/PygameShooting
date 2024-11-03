import pygame

class Bullet:
    def __init__(self, size, x, y, speedX, speedY, color):
        self.size = size
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY
        self.color = color

    def move(self):
        self.x += self.speedX
        self.y += self.speedY

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)
