import pygame
import values
import colorsys

class Item:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.color = values.item_colors["ITEM_" + self.type + "_COLOR"]
        self.speed = values.ITEM_SPEED
        self.size = values.ITEM_SIZE
        self.hue = 0

    def update_color(self):
        r, g, b = self.color
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # 彩度の変化方向を保持するフラグ（初期値はTrueで増加方向）
        if not hasattr(self, "s_increasing"):
            self.s_increasing = True

        # 彩度を増加または減少させる
        if self.s_increasing:
            v += (5.0 / 255.0)
            if v >= 1.0:
                v = 1.0
                self.s_increasing = False  # 彩度が最大値に達したので減少方向に切り替える
        else:
            v -= (5.0 / 255.0)
            if v <= 0.5:
                v = 0.5
                self.s_increasing = True  # 彩度が最小値に達したので増加方向に切り替える
        
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        self.color = (int(r * 255), int(g * 255), int(b * 255))

    def draw(self, window):
        self.update_color()
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)

    def move(self):
        self.y += self.speed

    def enhancement(self, player):
        if   self.type == "HEAL":
            self.heal_life(player)
        elif self.type == "SPEED":
            self.speed_enhance(player)
        elif self.type == "BULLET":
            self.bullet_enhance(player)
        return player

    def heal_life(self, player):
        player.lives += 1

    def speed_enhance(self, player):
        player.speed += 1

    def bullet_enhance(self, player):
        player.bullet_level += 1
