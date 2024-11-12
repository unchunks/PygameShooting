import pygame
from actor import Actor
from bullet import *
import values
import sys
import os

# プレイヤークラス
class Player(Actor):
    def __init__(self):
        super().__init__(
            values.PLAYER_SIZE, 
            values.WIDTH // 2, 
            values.HEIGHT - 2 * values.PLAYER_SIZE, 
            values.PLAYER_SPEED, 
            values.PLAYER_LIVES, 
            values.PLAYER_COLOR
        )
        self.timestamp = 0
        image_path = self.resource_path("images/player.png")
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (self.size, self.size))  # リサイズ

    # PyInstallerでパッケージングされた場合の画像パスを取得
    def resource_path(self, relative_path):
        """ 画像ファイルへのパスを返す """
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, relative_path)

    def move(self, dir):
        pass

    def fire(self) -> list:
        bullets = []
        if pygame.time.get_ticks() - self.timestamp > 5000:
            self.bullet_level = 1
        if self.bullet_level == 1:
            # 中央
            bullets.append(Bullet(
                values.PLAYER_BULLET_SIZE, 
                self.x + self.size // 2, 
                self.y, 
                0,
                -values.PLAYER_BULLET_SPEED, 
                values.PLAYER_BULLET_COLOR,
            ))
        elif self.bullet_level > 1:
            # 中央
            bullets.append(Bullet(
                values.PLAYER_BULLET_SIZE, 
                self.x + self.size // 2, 
                self.y, 
                0,
                -values.PLAYER_BULLET_SPEED,
                values.PLAYER_BULLET_COLOR,
            ))
            # 右上
            bullets.append(Bullet(
                values.PLAYER_BULLET_SIZE, 
                self.x + self.size // 2, 
                self.y, 
                values.PLAYER_BULLET_SPEED / 3,
                -values.PLAYER_BULLET_SPEED, 
                values.PLAYER_BULLET_COLOR,
            ))
            # 左上
            bullets.append(Bullet(
                values.PLAYER_BULLET_SIZE, 
                self.x + self.size // 2, 
                self.y, 
                -values.PLAYER_BULLET_SPEED / 3,
                -values.PLAYER_BULLET_SPEED, 
                values.PLAYER_BULLET_COLOR,
            ))
        return bullets

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
