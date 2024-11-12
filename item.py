import pygame
import values
import sys
import os

class Item:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.color = values.item_colors["ITEM_" + self.type + "_COLOR"]
        self.speed = values.ITEM_SPEED
        self.size = values.ITEM_SIZE
        self.hue = 0

        if self.type == "BULLET":
            source_y = 0
        if self.type == "HEAL":
            source_y = 5
        if self.type == "SPEED":
            source_y = 10
        image_path = self.resource_path("images/item.png")
        image = pygame.image.load(image_path)
        clip_rect = pygame.Rect(0, source_y, 5, 5)
        image = image.subsurface(clip_rect) # クリップ
        self.image = pygame.transform.scale(image, (self.size, self.size))  # リサイズ

    # PyInstallerでパッケージングされた場合の画像パスを取得
    def resource_path(self, relative_path):
        """ 画像ファイルへのパスを返す """
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, relative_path)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.speed

    def enhancement(self, player):
        if   self.type == "HEAL":
            player = self.heal_life(player)
        elif self.type == "SPEED":
            player = self.speed_enhance(player)
        elif self.type == "BULLET":
            player = self.bullet_enhance(player)
        return player

    def heal_life(self, player):
        player.lives += 1
        return player

    def speed_enhance(self, player):
        player.speed += 5
        return player

    def bullet_enhance(self, player):
        player.bullet_level = 2
        player.timestamp = pygame.time.get_ticks()
        return player
