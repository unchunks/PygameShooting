# ゲーム設定
FPS: int = 60
FRAME_TIME: int = int(1000 / FPS)  # ms

# ウィンドウのデフォルトサイズ
INIT_WIDTH: int = 1440
INIT_HEIGHT: int = 850

# 色の定義
RED: tuple[int, int, int] = (255, 0, 0)
GREEN: tuple[int, int, int] = (0, 255, 0)
BLUE: tuple[int, int, int] = (0, 0, 255)
WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0)
YELLOW: tuple[int, int, int] = (255, 255, 0)
CYAN: tuple[int, int, int] = (0, 255, 255)
MAGENTA: tuple[int, int, int] = (255, 0, 255)
GRAY: tuple[int, int, int] = (128, 128, 128)
ORANGE: tuple[int, int, int] = (255, 165, 0)
PURPLE: tuple[int, int, int] = (128, 0, 128)
PINK: tuple[int, int, int] = (255, 192, 203)
BROWN: tuple[int, int, int] = (165, 42, 42)
GOLD: tuple[int, int, int] = (255, 215, 0)
SILVER: tuple[int, int, int] = (192, 192, 192)
LIGHT_BLUE: tuple[int, int, int] = (173, 216, 230)
DARK_GREEN: tuple[int, int, int] = (0, 100, 0)
SKY_BLUE: tuple[int, int, int] = (135, 206, 235)
OLIVE: tuple[int, int, int] = (128, 128, 0)
MAROON: tuple[int, int, int] = (128, 0, 0)
NAVY: tuple[int, int, int] = (0, 0, 128)
TEAL: tuple[int, int, int] = (0, 128, 128)
LAVENDER: tuple[int, int, int] = (230, 230, 250)
BEIGE: tuple[int, int, int] = (245, 245, 220)
TURQUOISE: tuple[int, int, int] = (64, 224, 208)
INDIGO: tuple[int, int, int] = (75, 0, 130)
VIOLET: tuple[int, int, int] = (238, 130, 238)
MINT: tuple[int, int, int] = (189, 252, 201)
SALMON: tuple[int, int, int] = (250, 128, 114)
CHOCOLATE: tuple[int, int, int] = (210, 105, 30)

# 方向
LEFT: tuple[int, int] = (-1, 0)
RIGHT: tuple[int, int] = (1, 0)
UP: tuple[int, int] = (0, -1)
DOWN: tuple[int, int] = (0, 1)
LEFT_UP: tuple[int, int] = (-1, -1)
LEFT_DOWN: tuple[int, int] = (-1, 1)
RIGHT_UP: tuple[int, int] = (1, -1)
RIGHT_DOWN: tuple[int, int] = (1, 1)

# アイテムのデフォルト最大数
ITEM_NUM: int = 2

ITEM_SPEED: int = 3
ITEM_SIZE: int = 5

item_colors: dict[str, tuple[int, int, int]] = {
    "ITEM_HEAL_COLOR"   : TEAL,
    "ITEM_SPEED_COLOR"  : LIGHT_BLUE,
    "ITEM_BULLET_COLOR" : SALMON,
}
item_types: list[str] = ["HEAL", "SPEED", "BULLET"]
item_weights: list[int] = [2, 3, 1]

# プレイヤー
PLAYER_SIZE : int = 30
PLAYER_SPEED: int = 10
PLAYER_LIVES: int = 3
PLAYER_COLOR: tuple[int, int, int] = WHITE

PLAYER_BULLET_SIZE : int = 5
PLAYER_BULLET_SPEED: int = 15
PLAYER_BULLET_COLOR: tuple[int, int, int]  = GREEN

# 敵のデフォルト最大数
ENEMY_NUM: int = 10

enemy_values: dict[str, int | tuple[int, int, int]] = {
    # 静止
    "ENEMY_SIZE_STOP"  : 40,
    "ENEMY_SPEED_STOP" : 0,
    "ENEMY_LIVES_STOP" : 5,
    "ENEMY_COLOR_STOP" : RED,
    "ENEMY_SCORE_STOP" : 40,

    "ENEMY_BULLET_SIZE_STOP"  : 10,
    "ENEMY_BULLET_SPEED_STOP" : 8,
    "ENEMY_BULLET_COLOR_STOP" : MAGENTA,

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

    "ENEMY_BULLET_SIZE_BOSS"  : 10,
    "ENEMY_BULLET_SPEED_BOSS" : 15,
    "ENEMY_BULLET_COLOR_BOSS" : SILVER,
}

ENEMY_SCORE_TOTAL: int = enemy_values["ENEMY_SCORE_STOP"] + enemy_values["ENEMY_SCORE_STRAIGHT"] + enemy_values["ENEMY_SCORE_ZIGZAG"] + enemy_values["ENEMY_SCORE_FAST"] + enemy_values["ENEMY_SCORE_BOSS"]
# 敵の種類
enemy_types: list[str] = ["STOP", "STRAIGHT", "ZIGZAG", "FAST", "BOSS"]
# 各選択肢に対応する重み（選ばれる確率）
enemy_weights: list[float] = [
    ENEMY_SCORE_TOTAL / enemy_values["ENEMY_SCORE_STOP"],
    ENEMY_SCORE_TOTAL / enemy_values["ENEMY_SCORE_STRAIGHT"],
    ENEMY_SCORE_TOTAL / enemy_values["ENEMY_SCORE_ZIGZAG"],
    ENEMY_SCORE_TOTAL / enemy_values["ENEMY_SCORE_FAST"],
    ENEMY_SCORE_TOTAL / enemy_values["ENEMY_SCORE_BOSS"] / 5
]