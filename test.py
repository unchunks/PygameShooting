import pygame

# 初期化
pygame.init()

# 画面サイズ設定
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("スクロール可能な色と色の名前の一覧表示")

# 色の定義

colors = {
    "RED" :(255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "YELLOW": (255, 255, 0),
    "CYAN": (0, 255, 255),
    "MAGENTA": (255, 0, 255),
    "GRAY": (128, 128, 128),
    "ORANGE": (255, 165, 0),
    "PURPLE": (128, 0, 128),
    "PINK": (255, 192, 203),
    "BROWN": (165, 42, 42),
    "GOLD": (255, 215, 0),
    "SILVER": (192, 192, 192),
    "LIGHT_BLUE": (173, 216, 230),
    "DARK_GREEN": (0, 100, 0),
    "SKY_BLUE": (135, 206, 235),
    "OLIVE": (128, 128, 0),
    "MAROON": (128, 0, 0),
    "NAVY": (0, 0, 128),
    "TEAL": (0, 128, 128),
    "LAVENDER": (230, 230, 250),
    "BEIGE": (245, 245, 220),
    "TURQUOISE": (64, 224, 208),
    "INDIGO": (75, 0, 130),
    "VIOLET": (238, 130, 238),
    "MINT": (189, 252, 201),
    "SALMON": (250, 128, 114),
    "CHOCOLATE": (210, 105, 30)
}


# フォント設定
font = pygame.font.SysFont("Arial", 24)

# スクロール量の設定
scroll_y = 0
scroll_speed = 20

# ゲームループ
running = True
while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # ホイールアップ
                scroll_y = min(scroll_y + scroll_speed, 0)  # スクロール量が正に行かないように制限
            elif event.button == 5:  # ホイールダウン
                scroll_y -= scroll_speed

    # 画面塗りつぶし
    screen.fill((255, 255, 255))

    # 色と色名の描画（2列で表示）
    y_offset = 20 + scroll_y  # 初期の Y オフセットにスクロール量を加算
    x_offset = 50  # 初期の X オフセット
    column_width = 350  # 列の幅
    for index, (color_name, rgb) in enumerate(colors.items()):
        if index % 2 == 0:
            x_offset = 50  # 左の列
        else:
            x_offset = 50 + column_width  # 右の列

        # 色のブロックを描画
        pygame.draw.rect(screen, rgb, (x_offset, y_offset, 100, 30))
        # 色の名前を描画
        text_surface = font.render(color_name, True, (0, 0, 0))
        screen.blit(text_surface, (x_offset + 120, y_offset))

        # Y 座標のオフセットを次に移動（2列なので偶数行のみ増やす）
        if index % 2 == 1:
            y_offset += 50

    # 画面更新
    pygame.display.flip()

# 終了処理
pygame.quit()
