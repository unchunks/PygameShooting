import pygame
from bullet import *
import sys
import os

class Actor:
    def __init__(self, size: int, x: int, y: int, speed: int, color: tuple[int, int, int], image_path: str):
        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.speed: int = speed
        self.color: tuple[int, int, int] = color
        self.image_path: str = self.resource_path(image_path)
        self.image = pygame.image.load(self.image_path)

    # PyInstallerでパッケージングされた場合の画像パスを取得
    def resource_path(self, relative_path: str) -> str:
        """ 画像ファイルへのパスを返す """
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, relative_path)

    def move(self, direction: tuple[int, int], reverse: bool = False):
        if reverse:
            self.x -= direction[0] * self.speed
            self.y -= direction[1] * self.speed
        else:
            self.x += direction[0] * self.speed
            self.y += direction[1] * self.speed

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
