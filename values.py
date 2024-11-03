# ゲーム設定
FPS = 60
FRAME_TIME = int(1000 / FPS)  # ms

# キャンバスのサイズ
WIDTH = 800
HEIGHT = 600

# 色の定
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 100, 0)
SKY_BLUE = (135, 206, 235)
OLIVE = (128, 128, 0)
MAROON = (128, 0, 0)
NAVY = (0, 0, 128)
TEAL = (0, 128, 128)
LAVENDER = (230, 230, 250)
BEIGE = (245, 245, 220)
TURQUOISE = (64, 224, 208)
INDIGO = (75, 0, 130)
VIOLET = (238, 130, 238)
MINT = (189, 252, 201)
SALMON = (250, 128, 114)
CHOCOLATE = (210, 105, 30)

ITEM_NUM = 2

ITEM_SPEED = 3
ITEM_SIZE = 5

item_colors = {
    "ITEM_HEAL_COLOR"   : TEAL,
    "ITEM_SPEED_COLOR"  : LIGHT_BLUE,
    "ITEM_BULLET_COLOR" : SALMON,
}

item_types = ["HEAL", "SPEED", "BULLET"]
item_weights = [1, 1, 1]

# プレイヤー
PLAYER_SIZE  = 30
PLAYER_SPEED = 10
PLAYER_LIVES = 5
PLAYER_COLOR = WHITE

PLAYER_BULLET_SIZE   = 5
PLAYER_BULLET_SPEED  = 15
PLAYER_BULLET_COLOR  = GREEN

ENEMY_NUM = 10

enemy_values = {
    # 直線移動
    "ENEMY_SIZE_STRAIGHT"  : 40,
    "ENEMY_SPEED_STRAIGHT" : 5,
    "ENEMY_LIVES_STRAIGHT" : 5,
    "ENEMY_COLOR_STRAIGHT" : ORANGE,
    "ENEMY_SCORE_STRAIGHT" : 50,

    "ENEMY_BULLET_SIZE_STRAIGHT"  : 10,
    "ENEMY_BULLET_SPEED_STRAIGHT" : 15,
    "ENEMY_BULLET_COLOR_STRAIGHT" : PINK,

    # ジグザグ（波）
    "ENEMY_SIZE_ZIGZAG"  : 40,
    "ENEMY_SPEED_ZIGZAG" : 5,
    "ENEMY_LIVES_ZIGZAG" : 8,
    "ENEMY_COLOR_ZIGZAG" : TURQUOISE,
    "ENEMY_SCORE_ZIGZAG" : 80,

    "ENEMY_BULLET_SIZE_ZIGZAG"  : 10,
    "ENEMY_BULLET_SPEED_ZIGZAG" : 15,
    "ENEMY_BULLET_COLOR_ZIGZAG" : SKY_BLUE,

    # 静止
    "ENEMY_SIZE_STOP"  : 40,
    "ENEMY_SPEED_STOP" : 0,
    "ENEMY_LIVES_STOP" : 5,
    "ENEMY_COLOR_STOP" : RED,
    "ENEMY_SCORE_STOP" : 40,

    "ENEMY_BULLET_SIZE_STOP"  : 10,
    "ENEMY_BULLET_SPEED_STOP" : 10,
    "ENEMY_BULLET_COLOR_STOP" : MAGENTA,

    # 素早い
    "ENEMY_SIZE_FAST"  : 30,
    "ENEMY_SPEED_FAST" : 10,
    "ENEMY_LIVES_FAST" : 3,
    "ENEMY_COLOR_FAST" : INDIGO,
    "ENEMY_SCORE_FAST" : 200,

    "ENEMY_BULLET_SIZE_FAST"  : 10,
    "ENEMY_BULLET_SPEED_FAST" : 30,
    "ENEMY_BULLET_COLOR_FAST" : MINT,

    # ボス
    "ENEMY_SIZE_BOSS"  : 80,
    "ENEMY_SPEED_BOSS" : 3,
    "ENEMY_LIVES_BOSS" : 30,
    "ENEMY_COLOR_BOSS" : GOLD,
    "ENEMY_SCORE_BOSS" : 1000,

    "ENEMY_BULLET_SIZE_BOSS"  : 15,
    "ENEMY_BULLET_SPEED_BOSS" : 15,
    "ENEMY_BULLET_COLOR_BOSS" : SILVER,
}

ENEMY_SCORE_TOTAL = enemy_values["ENEMY_SCORE_STRAIGHT"] + enemy_values["ENEMY_SCORE_ZIGZAG"] + enemy_values["ENEMY_SCORE_STOP"] + enemy_values["ENEMY_SCORE_FAST"] + enemy_values["ENEMY_SCORE_BOSS"]
# 敵の種類
enemy_types = ["STRAIGHT", "ZIGZAG", "STOP", "FAST", "BOSS"]
# 各選択肢に対応する重み（選ばれる確率）
enemy_weights = [
    ENEMY_SCORE_TOTAL / enemy_values["ENEMY_SCORE_STRAIGHT"],
    ENEMY_SCORE_TOTAL / enemy_values["ENEMY_SCORE_ZIGZAG"],
    ENEMY_SCORE_TOTAL / enemy_values["ENEMY_SCORE_STOP"],
    ENEMY_SCORE_TOTAL / enemy_values["ENEMY_SCORE_FAST"],
    ENEMY_SCORE_TOTAL / enemy_values["ENEMY_SCORE_BOSS"]
]