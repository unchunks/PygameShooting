import pygame
import values
from actor import Actor
from player import Player

class Item(Actor):
    def __init__(self, x: int, y: int, type: str):
        super().__init__(
            values.ITEM_SIZE,
            x,
            y,
            values.ITEM_SPEED,
            values.item_colors["ITEM_" + type + "_COLOR"],
            "images/item.png"
        )
        self.type = type
        if self.type == "BULLET":
            source_y = 0
        if self.type == "HEAL":
            source_y = 5
        if self.type == "SPEED":
            source_y = 10
        image = pygame.image.load(self.image_path)
        clip_rect = pygame.Rect(0, source_y, 5, 5)
        image = image.subsurface(clip_rect) # クリップ
        self.image = pygame.transform.scale(image, (self.size, self.size))  # リサイズ

    def move(self):
        super().move(values.DOWN)

    def enhancement(self, player):
        if   self.type == "HEAL":
            player = self.heal_life(player)
        elif self.type == "SPEED":
            player = self.speed_enhance(player)
        elif self.type == "BULLET":
            player = self.bullet_enhance(player)
        return player

    def heal_life(self, player) -> Player:
        player.lives += 1
        return player

    def speed_enhance(self, player) -> Player:
        player.speed += 5
        return player

    def bullet_enhance(self, player) -> Player:
        player.bullet_level = 2
        player.timestamp = pygame.time.get_ticks()
        return player
