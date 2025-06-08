import pygame
import os
import math

# Pygameの初期化
pygame.init()

# 画面設定（画像生成用）
WIDTH, HEIGHT = 800, 600
screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
YELLOW = (255, 215, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_RED = (255, 182, 193)

def create_background():
    """背景画像を生成"""
    surface = pygame.Surface((WIDTH, HEIGHT))
    
    # グラデーション背景
    for y in range(HEIGHT):
        # 上から下へのグラデーション（水色から白へ）
        r = int(LIGHT_BLUE[0] + (WHITE[0] - LIGHT_BLUE[0]) * (y / HEIGHT))
        g = int(LIGHT_BLUE[1] + (WHITE[1] - LIGHT_BLUE[1]) * (y / HEIGHT))
        b = int(LIGHT_BLUE[2] + (WHITE[2] - LIGHT_BLUE[2]) * (y / HEIGHT))
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))
    
    return surface

def create_grid():
    """○×ゲームのグリッドを生成"""
    size = 300
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # 背景を白に
    surface.fill(WHITE)
    
    # 格子線を描画
    pygame.draw.line(surface, BLACK, (size//3, 0), (size//3, size), 5)
    pygame.draw.line(surface, BLACK, (2*size//3, 0), (2*size//3, size), 5)
    pygame.draw.line(surface, BLACK, (0, size//3), (size, size//3), 5)
    pygame.draw.line(surface, BLACK, (0, 2*size//3), (size, 2*size//3), 5)
    
    # 外枠
    pygame.draw.rect(surface, BLACK, (0, 0, size, size), 5)
    
    return surface

def create_maru():
    """○（マル）を生成"""
    size = 80
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # 透明な背景
    surface.fill((0, 0, 0, 0))
    
    # ○を描画
    pygame.draw.circle(surface, BLUE, (size//2, size//2), size//2 - 5, 5)
    
    return surface

def create_batsu():
    """×（バツ）を生成"""
    size = 80
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # 透明な背景
    surface.fill((0, 0, 0, 0))
    
    # ×を描画
    pygame.draw.line(surface, RED, (5, 5), (size-5, size-5), 5)
    pygame.draw.line(surface, RED, (size-5, 5), (5, size-5), 5)
    
    return surface

def create_title():
    """タイトル画像を生成"""
    width, height = 400, 100
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # 背景を透明に
    surface.fill((0, 0, 0, 0))
    
    # タイトルテキスト
    try:
        font = pygame.font.Font("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 60)
    except:
        font = pygame.font.SysFont(None, 60)
    
    # ○の部分
    maru_text = font.render("○", True, BLUE)
    maru_rect = maru_text.get_rect(midleft=(0, height//2))
    surface.blit(maru_text, maru_rect)
    
    # ×の部分
    batsu_text = font.render("×", True, RED)
    batsu_rect = batsu_text.get_rect(midleft=(maru_rect.right, height//2))
    surface.blit(batsu_text, batsu_rect)
    
    # ゲームの部分
    game_text = font.render("ゲーム", True, BLACK)
    game_rect = game_text.get_rect(midleft=(batsu_rect.right, height//2))
    surface.blit(game_text, game_rect)
    
    return surface

def create_button(width, height, text, color=BLUE):
    """ボタンを生成"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # ボタンの背景
    pygame.draw.rect(surface, color, (0, 0, width, height), border_radius=15)
    pygame.draw.rect(surface, BLACK, (0, 0, width, height), 3, border_radius=15)
    
    # テキスト
    try:
        font = pygame.font.Font("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", 24)
    except:
        font = pygame.font.SysFont(None, 24)
    
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(width//2, height//2))
    surface.blit(text_surface, text_rect)
    
    return surface

def create_win_line():
    """勝利ラインを生成"""
    size = 300
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # 透明な背景
    surface.fill((0, 0, 0, 0))
    
    # 勝利ラインを描画（横線の例）
    pygame.draw.line(surface, GREEN, (10, size//6), (size-10, size//6), 10)
    
    return surface

def generate_all_images():
    """全ての画像を生成して保存"""
    # 保存先ディレクトリ
    if not os.path.exists('.'):
        os.makedirs('.')
    
    # 背景
    background = create_background()
    pygame.image.save(background, "background.png")
    print("Generated background.png")
    
    # グリッド
    grid = create_grid()
    pygame.image.save(grid, "grid.png")
    print("Generated grid.png")
    
    # ○
    maru = create_maru()
    pygame.image.save(maru, "maru.png")
    print("Generated maru.png")
    
    # ×
    batsu = create_batsu()
    pygame.image.save(batsu, "batsu.png")
    print("Generated batsu.png")
    
    # タイトル
    title = create_title()
    pygame.image.save(title, "title.png")
    print("Generated title.png")
    
    # リスタートボタン
    restart_button = create_button(200, 50, "もう一度プレイ", GREEN)
    pygame.image.save(restart_button, "restart_button.png")
    print("Generated restart_button.png")
    
    # 勝利ライン（横）
    win_line_h = pygame.Surface((300, 300), pygame.SRCALPHA)
    win_line_h.fill((0, 0, 0, 0))
    pygame.draw.line(win_line_h, GREEN, (10, 50), (290, 50), 10)
    pygame.image.save(win_line_h, "win_line_h1.png")
    print("Generated win_line_h1.png")
    
    win_line_h = pygame.Surface((300, 300), pygame.SRCALPHA)
    win_line_h.fill((0, 0, 0, 0))
    pygame.draw.line(win_line_h, GREEN, (10, 150), (290, 150), 10)
    pygame.image.save(win_line_h, "win_line_h2.png")
    print("Generated win_line_h2.png")
    
    win_line_h = pygame.Surface((300, 300), pygame.SRCALPHA)
    win_line_h.fill((0, 0, 0, 0))
    pygame.draw.line(win_line_h, GREEN, (10, 250), (290, 250), 10)
    pygame.image.save(win_line_h, "win_line_h3.png")
    print("Generated win_line_h3.png")
    
    # 勝利ライン（縦）
    win_line_v = pygame.Surface((300, 300), pygame.SRCALPHA)
    win_line_v.fill((0, 0, 0, 0))
    pygame.draw.line(win_line_v, GREEN, (50, 10), (50, 290), 10)
    pygame.image.save(win_line_v, "win_line_v1.png")
    print("Generated win_line_v1.png")
    
    win_line_v = pygame.Surface((300, 300), pygame.SRCALPHA)
    win_line_v.fill((0, 0, 0, 0))
    pygame.draw.line(win_line_v, GREEN, (150, 10), (150, 290), 10)
    pygame.image.save(win_line_v, "win_line_v2.png")
    print("Generated win_line_v2.png")
    
    win_line_v = pygame.Surface((300, 300), pygame.SRCALPHA)
    win_line_v.fill((0, 0, 0, 0))
    pygame.draw.line(win_line_v, GREEN, (250, 10), (250, 290), 10)
    pygame.image.save(win_line_v, "win_line_v3.png")
    print("Generated win_line_v3.png")
    
    # 勝利ライン（斜め）
    win_line_d1 = pygame.Surface((300, 300), pygame.SRCALPHA)
    win_line_d1.fill((0, 0, 0, 0))
    pygame.draw.line(win_line_d1, GREEN, (10, 10), (290, 290), 10)
    pygame.image.save(win_line_d1, "win_line_d1.png")
    print("Generated win_line_d1.png")
    
    win_line_d2 = pygame.Surface((300, 300), pygame.SRCALPHA)
    win_line_d2.fill((0, 0, 0, 0))
    pygame.draw.line(win_line_d2, GREEN, (290, 10), (10, 290), 10)
    pygame.image.save(win_line_d2, "win_line_d2.png")
    print("Generated win_line_d2.png")

if __name__ == "__main__":
    generate_all_images()
    print("All images generated successfully!")
