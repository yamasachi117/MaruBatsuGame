import pygame
import sys
import os
import random
import time

# Pygameの初期化
pygame.init()

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("○×ゲーム")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
YELLOW = (255, 215, 0)
GRAY = (200, 200, 200)

# フォント設定
try:
    default_font = pygame.font.SysFont(None, 24)
    large_font = pygame.font.SysFont(None, 32)
    title_font = pygame.font.SysFont(None, 48)
except:
    default_font = pygame.font.SysFont(None, 24)
    large_font = pygame.font.SysFont(None, 32)
    title_font = pygame.font.SysFont(None, 48)

# 画像の読み込み
def load_image(name):
    path = os.path.join("assets", "images", name)
    try:
        image = pygame.image.load(path)
        return image
    except pygame.error as e:
        print(f"画像の読み込みに失敗しました: {path}")
        print(e)
        return None

# 画像の読み込み
background_img = load_image("background.png")
grid_img = load_image("grid.png")
maru_img = load_image("maru.png")
batsu_img = load_image("batsu.png")
title_img = load_image("title.png")
restart_button_img = load_image("restart_button.png")

# 勝利ラインの画像
win_lines = {
    "h1": load_image("win_line_h1.png"),  # 横1段目
    "h2": load_image("win_line_h2.png"),  # 横2段目
    "h3": load_image("win_line_h3.png"),  # 横3段目
    "v1": load_image("win_line_v1.png"),  # 縦1列目
    "v2": load_image("win_line_v2.png"),  # 縦2列目
    "v3": load_image("win_line_v3.png"),  # 縦3列目
    "d1": load_image("win_line_d1.png"),  # 斜め（左上から右下）
    "d2": load_image("win_line_d2.png")   # 斜め（右上から左下）
}

# ゲームの状態
class GameState:
    TITLE = 0
    PLAYING = 1
    GAME_OVER = 2

# プレイヤー
PLAYER_MARU = 1
PLAYER_BATSU = 2

# ゲームクラス
class MaruBatsuGame:
    def __init__(self):
        self.state = GameState.TITLE
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.current_player = PLAYER_MARU
        self.winner = None
        self.winning_line = None
        self.vs_cpu = True
        self.cpu_level = 1  # 1: ランダム, 2: 少し賢い
        self.cpu_thinking = False  # CPUが考え中かどうか
        self.cpu_think_start_time = 0  # CPUが考え始めた時間
        self.cpu_think_duration = 1000  # CPUが考える時間（ミリ秒）
        
        # グリッドの位置
        self.grid_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 150, 300, 300)
        
        # リスタートボタンの位置
        self.restart_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 100, 200, 50)
        
        # ホームボタンの位置
        self.home_button_rect = pygame.Rect(WIDTH - 120, 20, 100, 40)
        
        # モード選択ボタンの位置
        self.vs_player_button_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2, 140, 50)
        self.vs_cpu_button_rect = pygame.Rect(WIDTH//2 + 10, HEIGHT//2, 140, 50)
        
        # CPU難易度選択ボタンの位置
        self.easy_button_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 120, 140, 50)
        self.hard_button_rect = pygame.Rect(WIDTH//2 + 10, HEIGHT//2 + 120, 140, 50)
    
    def reset_game(self):
        """ゲームをリセット"""
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        
        # CPUとの対戦時は先手後手をランダムに決定
        if self.vs_cpu:
            self.current_player = random.choice([PLAYER_MARU, PLAYER_BATSU])
            # CPUが先手の場合は、CPUの手を打つ準備
            if self.current_player == PLAYER_BATSU:
                # 少し待ってからCPUが手を打つ
                self.cpu_thinking = True
                self.cpu_think_start_time = pygame.time.get_ticks()
        else:
            self.current_player = PLAYER_MARU
            
        self.winner = None
        self.winning_line = None
        self.state = GameState.PLAYING
        self.cpu_thinking = self.vs_cpu and self.current_player == PLAYER_BATSU
    
    def update(self):
        """ゲーム状態の更新"""
        # CPUが考え中の場合
        if self.state == GameState.PLAYING and self.cpu_thinking:
            current_time = pygame.time.get_ticks()
            # 一定時間経過したらCPUの手を打つ
            if current_time - self.cpu_think_start_time >= self.cpu_think_duration:
                self.cpu_thinking = False
                self.cpu_move()
    
    def make_move(self, row, col):
        """指定した位置に手を打つ"""
        if self.board[row][col] == 0:
            self.board[row][col] = self.current_player
            
            # 勝敗チェック
            if self.check_winner():
                self.state = GameState.GAME_OVER
            elif self.is_board_full():
                self.state = GameState.GAME_OVER
                self.winner = 0  # 引き分け
            else:
                # プレイヤー交代
                self.current_player = PLAYER_BATSU if self.current_player == PLAYER_MARU else PLAYER_MARU
                
                # CPUの手番
                if self.vs_cpu and self.current_player == PLAYER_BATSU and self.state == GameState.PLAYING:
                    # CPUが考え始める時間を記録
                    self.cpu_thinking = True
                    self.cpu_think_start_time = pygame.time.get_ticks()
    
    def cpu_move(self):
        """CPUの手を決定"""
        if self.cpu_level == 1:
            # ランダム戦略
            empty_cells = []
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == 0:
                        empty_cells.append((row, col))
            
            if empty_cells:
                row, col = random.choice(empty_cells)
                self.make_move(row, col)
        else:
            # 少し賢い戦略
            # 1. 自分が勝てる手があれば打つ
            # 2. 相手が次に勝てる手があればブロック
            # 3. 中央を取る
            # 4. 角を取る
            # 5. それ以外はランダム
            
            # 自分が勝てる手を探す
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == 0:
                        self.board[row][col] = PLAYER_BATSU
                        if self.check_winner(False):
                            self.board[row][col] = 0
                            self.make_move(row, col)
                            return
                        self.board[row][col] = 0
            
            # 相手が勝てる手をブロック
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == 0:
                        self.board[row][col] = PLAYER_MARU
                        if self.check_winner(False):
                            self.board[row][col] = 0
                            self.make_move(row, col)
                            return
                        self.board[row][col] = 0
            
            # 中央を取る
            if self.board[1][1] == 0:
                self.make_move(1, 1)
                return
            
            # 角を取る
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            random.shuffle(corners)
            for row, col in corners:
                if self.board[row][col] == 0:
                    self.make_move(row, col)
                    return
            
            # それ以外はランダム
            empty_cells = []
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == 0:
                        empty_cells.append((row, col))
            
            if empty_cells:
                row, col = random.choice(empty_cells)
                self.make_move(row, col)
    
    def check_winner(self, set_winning_line=True):
        """勝者をチェック"""
        # 横のチェック
        for row in range(3):
            if self.board[row][0] != 0 and self.board[row][0] == self.board[row][1] == self.board[row][2]:
                if set_winning_line:
                    self.winner = self.board[row][0]
                    self.winning_line = f"h{row+1}"
                return True
        
        # 縦のチェック
        for col in range(3):
            if self.board[0][col] != 0 and self.board[0][col] == self.board[1][col] == self.board[2][col]:
                if set_winning_line:
                    self.winner = self.board[0][col]
                    self.winning_line = f"v{col+1}"
                return True
        
        # 斜めのチェック（左上から右下）
        if self.board[0][0] != 0 and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if set_winning_line:
                self.winner = self.board[0][0]
                self.winning_line = "d1"
            return True
        
        # 斜めのチェック（右上から左下）
        if self.board[0][2] != 0 and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            if set_winning_line:
                self.winner = self.board[0][2]
                self.winning_line = "d2"
            return True
        
        return False
    
    def is_board_full(self):
        """ボードが埋まっているかチェック"""
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    return False
        return True
    
    def handle_event(self, event):
        """イベント処理"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # マウスクリック処理
            # ホームボタン（どの画面からでもタイトルに戻れる）
            if self.home_button_rect.collidepoint(event.pos) and self.state != GameState.TITLE:
                self.state = GameState.TITLE
                return
                
            if self.state == GameState.TITLE:
                # VS プレイヤーボタン
                if self.vs_player_button_rect.collidepoint(event.pos):
                    self.vs_cpu = False
                    self.reset_game()
                
                # VS CPUボタン
                elif self.vs_cpu_button_rect.collidepoint(event.pos):
                    self.vs_cpu = True
                    self.reset_game()
                
                # 難易度選択ボタン（CPUモードのみ）
                elif self.vs_cpu:
                    if self.easy_button_rect.collidepoint(event.pos):
                        self.cpu_level = 1
                    elif self.hard_button_rect.collidepoint(event.pos):
                        self.cpu_level = 2
            
            elif self.state == GameState.PLAYING:
                # CPUが考え中の場合はクリックを無視
                if self.vs_cpu and self.cpu_thinking:
                    return
                    
                # グリッド内のクリック
                if self.grid_rect.collidepoint(event.pos):
                    # クリック位置からセルの位置を計算
                    x = event.pos[0] - self.grid_rect.x
                    y = event.pos[1] - self.grid_rect.y
                    col = x // 100
                    row = y // 100
                    
                    # 手を打つ
                    if 0 <= row < 3 and 0 <= col < 3:
                        self.make_move(row, col)
            
            elif self.state == GameState.GAME_OVER:
                # リスタートボタン
                if self.restart_button_rect.collidepoint(event.pos):
                    # タイトル画面に戻らずに直接ゲームをリセット
                    self.reset_game()
    
    def draw(self, screen):
        """描画処理"""
        # 背景を描画
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(WHITE)
        
        if self.state == GameState.TITLE:
            # タイトル画面
            if title_img:
                title_rect = title_img.get_rect(center=(WIDTH//2, HEIGHT//4))
                screen.blit(title_img, title_rect)
            else:
                title_text = title_font.render("○×ゲーム", True, BLACK)
                title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
                screen.blit(title_text, title_rect)
            
            # モード選択テキスト
            mode_text = large_font.render("モードを選択してください", True, BLACK)
            mode_rect = mode_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            screen.blit(mode_text, mode_rect)
            
            # VS プレイヤーボタン
            pygame.draw.rect(screen, BLUE, self.vs_player_button_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, self.vs_player_button_rect, 2, border_radius=10)
            vs_player_text = default_font.render("対人戦", True, WHITE)
            vs_player_rect = vs_player_text.get_rect(center=self.vs_player_button_rect.center)
            screen.blit(vs_player_text, vs_player_rect)
            
            # VS CPUボタン
            pygame.draw.rect(screen, RED, self.vs_cpu_button_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, self.vs_cpu_button_rect, 2, border_radius=10)
            vs_cpu_text = default_font.render("CPU戦", True, WHITE)
            vs_cpu_rect = vs_cpu_text.get_rect(center=self.vs_cpu_button_rect.center)
            screen.blit(vs_cpu_text, vs_cpu_rect)
            
            # CPU難易度選択（CPUモードのみ）
            if self.vs_cpu:
                difficulty_text = default_font.render("難易度を選択", True, BLACK)
                difficulty_rect = difficulty_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 90))
                screen.blit(difficulty_text, difficulty_rect)
                
                # 簡単ボタン
                color = GREEN if self.cpu_level == 1 else GRAY
                pygame.draw.rect(screen, color, self.easy_button_rect, border_radius=10)
                pygame.draw.rect(screen, BLACK, self.easy_button_rect, 2, border_radius=10)
                easy_text = default_font.render("簡単", True, WHITE)
                easy_rect = easy_text.get_rect(center=self.easy_button_rect.center)
                screen.blit(easy_text, easy_rect)
                
                # 難しいボタン
                color = GREEN if self.cpu_level == 2 else GRAY
                pygame.draw.rect(screen, color, self.hard_button_rect, border_radius=10)
                pygame.draw.rect(screen, BLACK, self.hard_button_rect, 2, border_radius=10)
                hard_text = default_font.render("難しい", True, WHITE)
                hard_rect = hard_text.get_rect(center=self.hard_button_rect.center)
                screen.blit(hard_text, hard_rect)
        
        elif self.state == GameState.PLAYING or self.state == GameState.GAME_OVER:
            # ホームボタン
            pygame.draw.rect(screen, BLUE, self.home_button_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, self.home_button_rect, 2, border_radius=10)
            home_text = default_font.render("ホーム", True, WHITE)
            home_rect = home_text.get_rect(center=self.home_button_rect.center)
            screen.blit(home_text, home_rect)
            
            # グリッドを描画
            if grid_img:
                screen.blit(grid_img, self.grid_rect)
            else:
                pygame.draw.rect(screen, WHITE, self.grid_rect)
                # 格子線
                for i in range(1, 3):
                    pygame.draw.line(screen, BLACK, 
                                    (self.grid_rect.x + i * 100, self.grid_rect.y),
                                    (self.grid_rect.x + i * 100, self.grid_rect.y + 300), 5)
                    pygame.draw.line(screen, BLACK, 
                                    (self.grid_rect.x, self.grid_rect.y + i * 100),
                                    (self.grid_rect.x + 300, self.grid_rect.y + i * 100), 5)
            
            # 駒を描画
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == PLAYER_MARU:
                        if maru_img:
                            screen.blit(maru_img, 
                                      (self.grid_rect.x + col * 100 + 10, 
                                       self.grid_rect.y + row * 100 + 10))
                        else:
                            pygame.draw.circle(screen, BLUE, 
                                             (self.grid_rect.x + col * 100 + 50, 
                                              self.grid_rect.y + row * 100 + 50), 40, 5)
                    elif self.board[row][col] == PLAYER_BATSU:
                        if batsu_img:
                            screen.blit(batsu_img, 
                                      (self.grid_rect.x + col * 100 + 10, 
                                       self.grid_rect.y + row * 100 + 10))
                        else:
                            pygame.draw.line(screen, RED, 
                                           (self.grid_rect.x + col * 100 + 15, 
                                            self.grid_rect.y + row * 100 + 15),
                                           (self.grid_rect.x + col * 100 + 85, 
                                            self.grid_rect.y + row * 100 + 85), 5)
                            pygame.draw.line(screen, RED, 
                                           (self.grid_rect.x + col * 100 + 85, 
                                            self.grid_rect.y + row * 100 + 15),
                                           (self.grid_rect.x + col * 100 + 15, 
                                            self.grid_rect.y + row * 100 + 85), 5)
            
            # 勝利ラインを描画
            if self.winning_line and self.winning_line in win_lines and win_lines[self.winning_line]:
                screen.blit(win_lines[self.winning_line], self.grid_rect)
            
            # 現在のプレイヤー表示
            if self.state == GameState.PLAYING:
                if self.current_player == PLAYER_MARU:
                    player_text = large_font.render("○の番です", True, BLUE)
                else:
                    player_text = large_font.render("×の番です", True, RED)
                player_rect = player_text.get_rect(center=(WIDTH//2, 100))
                screen.blit(player_text, player_rect)
                
                # CPUが考え中の表示
                if self.vs_cpu and self.cpu_thinking:
                    thinking_text = default_font.render("CPUが考え中...", True, RED)
                    thinking_rect = thinking_text.get_rect(center=(WIDTH//2, 140))
                    screen.blit(thinking_text, thinking_rect)
            
            # ゲーム終了時の表示
            if self.state == GameState.GAME_OVER:
                if self.winner == PLAYER_MARU:
                    result_text = large_font.render("○の勝ち！", True, BLUE)
                elif self.winner == PLAYER_BATSU:
                    result_text = large_font.render("×の勝ち！", True, RED)
                else:
                    result_text = large_font.render("引き分け！", True, BLACK)
                result_rect = result_text.get_rect(center=(WIDTH//2, 100))
                screen.blit(result_text, result_rect)
                
                # リスタートボタン
                if restart_button_img:
                    screen.blit(restart_button_img, self.restart_button_rect)
                else:
                    pygame.draw.rect(screen, GREEN, self.restart_button_rect, border_radius=10)
                    restart_text = default_font.render("もう一度プレイ", True, WHITE)
                    restart_rect = restart_text.get_rect(center=self.restart_button_rect.center)
                    screen.blit(restart_text, restart_rect)

# ゲームの初期化
game = MaruBatsuGame()

# ゲームループ
clock = pygame.time.Clock()
running = True

while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        game.handle_event(event)
    
    # ゲーム状態の更新
    game.update()
    
    # 描画
    game.draw(screen)
    
    # 画面の更新
    pygame.display.flip()
    clock.tick(60)

# Pygameの終了
pygame.quit()
sys.exit()
