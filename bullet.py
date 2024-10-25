import values

# NOTE: 座標は中心
class Bullet:
    def __init__(self, canvas, size, x, y, speed, color):
        self.canvas = canvas
        self.width = size
        self.height = size
        self.x = x
        self.y = y
        self.speed = speed
        self.shape = self.canvas.create_rectangle(
            self.x - self.width/2, self.y - self.height/2, self.x + self.width/2, self.y + self.height/2, fill=color
        )

    # dirは+1（下）か-1（上）
    def move(self, dir):
        self.y += (self.speed * dir)
        self.canvas.coords(self.shape, self.x - self.width/2, self.y - self.height/2, self.x + self.width/2, self.y + self.height/2)
        if self.y < 0 or self.y > values.HEIGHT:
            self.canvas.delete(self.shape)
            return False
        return True
    
    def hit_test(self, actor):
        # 敵の弾とプレイヤーの衝突判定
        bullet_coords = self.canvas.bbox(self.shape)
        actor_coords = self.canvas.bbox(actor.shape)
        if bullet_coords and actor_coords:
            if (bullet_coords[2] > actor_coords[0] and  # bullet's right edge > player's left edge
                bullet_coords[0] < actor_coords[2] and  # bullet's left edge < player's right edge
                bullet_coords[3] > actor_coords[1] and  # bullet's bottom edge > player's top edge
                bullet_coords[1] < actor_coords[3]):    # bullet's top edge < player's bottom edge
                return True
        return False
