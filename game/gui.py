# game/gui.py
import pygame
from typing import Optional
from game.core import Card
from game.engine import GameEngine

pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 80, 100
SLOT_SIZE = 80
FONT = pygame.font.SysFont("Arial", 16)
WHITE, BLACK, GRAY, GREEN, RED = (255, 255, 255), (0, 0, 0), (150, 150, 150), (0, 255, 0), (255, 0, 0)
YELLOW = (255, 255, 0)  # Добавляем желтый цвет для активных существ

class GUI:
    """Класс для управления графическим интерфейсом."""
    def __init__(self, engine: GameEngine) -> None:
        self.engine = engine
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Card Game")
        self.clock = pygame.time.Clock()
        self.running = True

    def draw_card(self, card: Optional[Card], x: int, y: int, clickable: bool = False) -> pygame.Rect:
        """Рисует карту на экране."""
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        # Определяем цвет: желтый для активных, зеленый для кликабельных неактивных, серый для остальных
        if card and card.active:
            color = YELLOW
        elif clickable and card and self.engine.player.can_play_card(card):
            color = GREEN
        else:
            color = GRAY
        pygame.draw.rect(self.screen, color, rect)
        if card:
            name_text = FONT.render(f"{card.name}", True, BLACK)
            stats_text = FONT.render(f"M:{card.mana_cost} A:{card.attack} H:{card.health}", True, BLACK)
            self.screen.blit(name_text, (x + 5, y + 5))
            self.screen.blit(stats_text, (x + 5, y + 25))
        return rect

    def draw_field(self) -> None:
        """Рисует игровое поле: сетку, слоты и статистику."""
        self.screen.fill(WHITE)

        # Отображение маны и HP
        player_stats = FONT.render(f"{self.engine.player.name}: Mana {self.engine.player.mana}, HP {self.engine.player.health}", True, BLACK)
        opp_stats = FONT.render(f"{self.engine.opponent.name}: Mana {self.engine.opponent.mana}, HP {self.engine.opponent.health}", True, BLACK)
        self.screen.blit(player_stats, (10, HEIGHT - 40))
        self.screen.blit(opp_stats, (10, 10))

        # Оппонент: сетка карт
        self.grid_rects = []
        for row in range(2):
            row_rects = []
            for col in range(8):
                card = self.engine.field.grid[row][col]
                x = col * (CARD_WIDTH + 10) + 50
                y = 50 if row == 0 else 420  # Оппонент: y=50, Игрок: y=420
                clickable = (row == 1)
                rect = self.draw_card(card, x, y, clickable)
                row_rects.append(rect)
            self.grid_rects.append(row_rects)

        # Поле оппонента
        self.opp_slots = []
        for slot in range(8):
            card = self.engine.field.get_creatures(False)[slot]
            x = slot * (SLOT_SIZE + 10) + 50
            rect = self.draw_card(card, x, 170)
            self.opp_slots.append(rect)

        # Поле игрока
        self.player_slots = []
        for slot in range(8):
            card = self.engine.field.get_creatures(True)[slot]
            x = slot * (SLOT_SIZE + 10) + 50
            rect = self.draw_card(card, x, 300)
            self.player_slots.append(rect)

        # Кнопка "Конец хода"
        self.end_turn_btn = pygame.Rect(WIDTH - 150, HEIGHT - 50, 100, 30)
        pygame.draw.rect(self.screen, GREEN, self.end_turn_btn)
        text = FONT.render("Конец хода", True, BLACK)
        self.screen.blit(text, (WIDTH - 140, HEIGHT - 40))

    def handle_click(self, pos: tuple[int, int]) -> None:
        """Обрабатывает клики мыши."""
        for col, rect in enumerate(self.grid_rects[1]):
            if rect.collidepoint(pos):
                self.selected_card = (1, col)
                return

        if hasattr(self, 'selected_card'):
            for slot, rect in enumerate(self.player_slots):
                if rect.collidepoint(pos):
                    row, col = self.selected_card
                    self.engine.play_card(row, col, slot, is_player=True)
                    del self.selected_card
                    return

        if self.end_turn_btn.collidepoint(pos):
            self.engine.next_turn()

    def run(self) -> None:
        """Основной цикл игры."""
        self.engine.start_game()
        while self.running and not self.engine.is_game_over():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.draw_field()
            pygame.display.flip()
            self.clock.tick(60)

        if self.engine.player.health <= 0:
            print("Поражение: Игрок проиграл!")
        elif self.engine.opponent.health <= 0:
            print("Победа: Оппонент побежден!")
        pygame.quit()