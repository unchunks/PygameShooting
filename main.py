import tkinter as tk
import random
from actor import *
from bullet import *
import time

# ウィンドウの作成
window = tk.Tk()
window.title("2Dシューティングゲーム")
window.resizable(False, False)

# キャンバスを作成
canvas = tk.Canvas(window, width=values.WIDTH, height=values.HEIGHT, bg="black")
canvas.pack()

# ゲームの初期設定
player = Player(canvas)
bullets = []
enemies = []
enemy_bullets = []
keys_pressed = {}

def key_press(event):
    keys_pressed[event.keysym] = True

def key_release(event):
    if event.keysym in keys_pressed:
        del keys_pressed[event.keysym]

def setup_events():
    # キーが押されたときと離されたときのイベントバインド
    window.bind("<KeyPress>", key_press)
    window.bind("<KeyRelease>", key_release)

def input():
    # プレイヤーの動きをキーの状態に基づいて更新する
    if keys_pressed.get("w"):
        player.move("up")
    if keys_pressed.get("s"):
        player.move("down")
    if keys_pressed.get("a"):
        player.move("left")
    if keys_pressed.get("d"):
        player.move("right")
    if keys_pressed.get("space"):
        player.fire(bullets)
    if keys_pressed.get("q"):
        window.quit()

# ゲームオーバー画面の処理
def game_over():
    canvas.delete("all")
    game_over_text = canvas.create_text(values.WIDTH / 2, values.HEIGHT / 2, text="GAME OVER", fill="red", font=("Arial", 48))
    restart_button = tk.Button(window, text="Restart", command=start_game)
    canvas.create_window(values.WIDTH / 2, values.HEIGHT / 2 + 50, window=restart_button)

# ゲームを初期化して開始する
def start_game():
    global player, bullets, enemies, enemy_bullets, keys_pressed, lives_text
    lives_text = None
    canvas.delete("all")
    player = Player(canvas)
    lives_text = canvas.create_text(10, 10, anchor='nw', text=f"Lives: {player.lives}", fill="white", font=("Arial", 16))
    bullets = []
    enemies = []
    enemy_bullets = []
    keys_pressed = {}
    game_loop()

def game_loop():
    if player.lives <= 0:
        game_over()
        return    
    input()

    # プレイヤーの弾の処理
    for bullet in bullets[:]:
        if not bullet.move():
            bullets.remove(bullet)
        for enemy in enemies[:]:
            if bullet.hit_test(enemy):
                canvas.delete(enemy.enemy_shape)
                canvas.delete(bullet.bullet_shape)
                enemies.remove(enemy)
                bullets.remove(bullet)
                break

    # 敵の生成と移動
    if random.random() < 0.02:  # 敵がランダムに出現
        enemies.append(Enemy(canvas))

    for enemy in enemies[:]:
        if not enemy.move():
            enemies.remove(enemy)
        else:
            enemy.fire(enemy_bullets)  # 敵が弾を発射

    # 敵の弾の処理
    for enemy_bullet in enemy_bullets[:]:
        if not enemy_bullet.move():
            enemy_bullets.remove(enemy_bullet)
        elif enemy_bullet.hit_test(player):
            player.lives -= 1
            canvas.itemconfig(lives_text, text=f"Lives: {player.lives}")
            if player.lives <= 0:
                canvas.delete(player.player_shape)
                game_over()
                return
            canvas.delete(enemy_bullet.bullet_shape)
            enemy_bullets.remove(enemy_bullet)
            break

    if player.lives > 0:
        window.after(30, game_loop)

# イベントのバインディング
window.bind("<KeyPress>", key_press)
window.bind("<KeyRelease>", key_release)

# ゲームループ開始
start_game()

window.mainloop()