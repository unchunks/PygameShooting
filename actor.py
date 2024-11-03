import pygame
import values
from bullet import *

class Actor:
    def __init__(self, size: int, x: int, y: int, speed: int, lives: int, color: tuple):
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.lives = lives
        self.color = color
        self.bullet_level = 1

    def move(self, dx, dy):
        pass

    def fire(self, bullets: list):
        pass

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))
