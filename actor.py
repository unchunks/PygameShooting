from bullet import *

# NOTE: 座標は中心
class Actor:
    def __init__(self, canvas, size, x, y, speed, lives, color):
        self.canvas = canvas
        self.width = size
        self.height = size
        self.x = x
        self.y = y
        self.speed = speed
        self.lives = lives
        self.shape = self.canvas.create_rectangle(
            self.x - self.width/2, self.y - self.height/2, self.x + self.width/2, self.y + self.height/2, fill=color
        )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.coords(self.shape, self.x - self.width/2, self.y - self.height/2, self.x + self.width/2, self.y + self.height/2)

    def fire(self, bullets, size, speed, color):
        bullets.append(Bullet(self.canvas, size, self.x, self.y, speed, color))
