import random
import sys

import pygame
from pygame.locals import *

# 初始化pygame
pygame.init()

# 设置屏幕大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("键盘字母游戏")

# 定义颜色
BACKGROUND_COLOR = (25, 25, 40)
LETTER_COLORS = [
    (231, 76, 60),  # 红色
    (46, 204, 113),  # 绿色
    (52, 152, 219),  # 蓝色
    (155, 89, 182),  # 紫色
    (241, 196, 15),  # 黄色
    (230, 126, 34),  # 橙色
]
TEXT_COLOR = (236, 240, 241)
UI_BG_COLOR = (44, 62, 80, 180)
UI_BORDER_COLOR = (52, 152, 219)

# 游戏参数
FALL_SPEED = 2
LETTER_SIZE = 40
SPAWN_RATE = 30  # 每多少帧生成一个新字母
MAX_LETTERS = 10  # 屏幕上最大字母数


class FallingLetter:
    def __init__(self):
        self.letter = chr(random.randint(65, 90))  # A-Z
        self.x = random.randint(LETTER_SIZE, SCREEN_WIDTH - LETTER_SIZE)
        self.y = -LETTER_SIZE
        self.speed = random.uniform(FALL_SPEED, FALL_SPEED + 1.5)
        self.color = random.choice(LETTER_COLORS)
        self.size = LETTER_SIZE
        self.active = True

    def update(self):
        if self.active:
            self.y += self.speed

    def draw(self, surface):
        if self.active:
            # 绘制字母背景圆圈
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size // 2 + 5)

            # 创建字体对象
            font = pygame.font.SysFont(None, self.size)
            text_surface = font.render(self.letter, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(self.x, self.y))
            surface.blit(text_surface, text_rect)

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.size


class Game:
    def __init__(self):
        self.falling_letters = []
        self.score = 0
        self.lives = 3
        self.spawn_counter = 0
        self.game_over = False
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)

    def spawn_letter(self):
        if len(self.falling_letters) < MAX_LETTERS and self.spawn_counter >= SPAWN_RATE:
            self.falling_letters.append(FallingLetter())
            self.spawn_counter = 0
        else:
            self.spawn_counter += 1

    def handle_input(self, key):
        if self.game_over:
            return

        # 将按键转换为大写字母
        letter = key.upper()

        # 查找匹配的字母并移除
        for falling_letter in self.falling_letters:
            if falling_letter.letter == letter and falling_letter.active:
                falling_letter.active = False
                self.score += 10
                return

        # 如果没有匹配，扣生命值
        if not any(f.lower() == letter.lower() for f in [l.letter for l in self.falling_letters]):
            # 检查是否有其他未被击中的字母到达底部
            for falling_letter in self.falling_letters:
                if falling_letter.active and falling_letter.y > SCREEN_HEIGHT - 50:
                    self.lives -= 1
                    falling_letter.active = False
                    if self.lives <= 0:
                        self.game_over = True
                    break

    def update(self):
        if self.game_over:
            return

        # 更新所有掉落字母
        for falling_letter in self.falling_letters[:]:
            falling_letter.update()

            # 检查是否到达底部
            if falling_letter.y > SCREEN_HEIGHT and falling_letter.active:
                self.lives -= 1
                self.falling_letters.remove(falling_letter)
                if self.lives <= 0:
                    self.game_over = True

        # 移除不活跃的字母
        self.falling_letters = [f for f in self.falling_letters if f.active or not f.is_off_screen()]

        # 生成新字母
        self.spawn_letter()

    def draw(self, surface):
        # 绘制背景
        surface.fill(BACKGROUND_COLOR)

        # 添加渐变背景效果
        for y in range(0, SCREEN_HEIGHT, 4):
            alpha = 100 - int(y / SCREEN_HEIGHT * 100)
            s = pygame.Surface((SCREEN_WIDTH, 4))
            s.set_alpha(alpha)
            s.fill((60, 60, 90))
            surface.blit(s, (0, y))

        # 绘制网格线作为装饰
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(surface, (40, 40, 60), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(surface, (40, 40, 60), (0, y), (SCREEN_WIDTH, y), 1)

        # 绘制所有掉落字母
        for falling_letter in self.falling_letters:
            falling_letter.draw(surface)

        # 绘制UI面板
        self.draw_ui(surface)

        # 游戏结束画面
        if self.game_over:
            self.draw_game_over(surface)

    def draw_ui(self, surface):
        # 绘制分数和生命值背景
        ui_surface = pygame.Surface((SCREEN_WIDTH, 50), pygame.SRCALPHA)
        ui_surface.fill(UI_BG_COLOR)
        surface.blit(ui_surface, (0, 0))

        # 绘制边框
        pygame.draw.line(surface, UI_BORDER_COLOR, (0, 50), (SCREEN_WIDTH, 50), 3)

        # 绘制分数
        score_text = self.font.render(f"得分: {self.score}", True, TEXT_COLOR)
        surface.blit(score_text, (20, 10))

        # 绘制生命值
        lives_text = self.font.render(f"生命: {self.lives}", True, TEXT_COLOR)
        surface.blit(lives_text, (SCREEN_WIDTH - 120, 10))

        # 绘制说明文字
        instruction = self.small_font.render("输入键盘上的字母来消除掉落的字母", True, TEXT_COLOR)
        surface.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT - 30))

    def draw_game_over(self, surface):
        # 半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # 游戏结束文本
        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("游戏结束", True, (231, 76, 60))
        surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - 60))

        # 最终得分
        final_score = self.font.render(f"最终得分: {self.score}", True, TEXT_COLOR)
        surface.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2,
                                   SCREEN_HEIGHT // 2 + 20))

        # 重新开始提示
        restart_text = self.small_font.render("按 R 键重新开始", True, TEXT_COLOR)
        surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                                    SCREEN_HEIGHT // 2 + 80))


def main():
    clock = pygame.time.Clock()
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if game.game_over and event.key == K_r:
                    # 重新开始游戏
                    game = Game()
                elif not game.game_over:
                    game.handle_input(event.unicode)

        game.update()
        game.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
