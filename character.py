from bullet import Bullet
from actor import Actor

class Character(Actor):
    def __init__(self, size: int, x: int, y: int, speed: int, lives: int, color: tuple, bullet_size: int, bullet_speed: int, bullet_color: tuple, image_path: str):
        super().__init__(
            size,
            x,
            y,
            speed,
            color,
            image_path
        )
        self.lives: int = lives
        self.bullet_size: int = bullet_size
        self.bullet_speed: int = bullet_speed
        self.bullet_color: tuple[int, int, int] = bullet_color

    def shoot(self, direction: tuple[int, int]) -> Bullet:
        return Bullet(
            self.bullet_size, 
            self.x + self.size // 2, 
            self.y, 
            direction[0] * self.bullet_speed / 3,
            direction[1] * self.bullet_speed, 
            self.bullet_color,
        )
