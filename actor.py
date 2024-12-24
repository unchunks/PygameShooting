import pygame
from bullet import *
import sys
import os

class Actor:
    def __init__(self, size: int, x: int, y: int, speed: int, lives: int, color: tuple, bullet_size: int, bullet_speed: int, bullet_color: tuple, image_path: str):
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.lives = lives
        self.color = color
        self.bullet_size = bullet_size
        self.bullet_speed = bullet_speed
        self.bullet_color = bullet_color
        self.bullet_level = 1
        self.image_path = image_path

    # PyInstallerでパッケージングされた場合の画像パスを取得
    def resource_path(self, relative_path):
        """ 画像ファイルへのパスを返す """
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, relative_path)

    def move(self, direction: tuple, reverse: bool = False):
        if reverse:
            self.x -= direction[0] * self.speed
            self.y -= direction[1] * self.speed
        else:
            self.x += direction[0] * self.speed
            self.y += direction[1] * self.speed

    def shoot(self, direction: tuple) -> Bullet:
        return Bullet(
            self.bullet_size, 
            self.x + self.size // 2, 
            self.y, 
            direction[0] * self.bullet_speed / 3,
            direction[1] * self.bullet_speed, 
            self.bullet_color,
        )

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))
