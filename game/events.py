# game/events.py
import pygame
from typing import List, Optional
from game.core import Card
from data.config import DELAY_BETWEEN_ACTIONS, DELAY_BEFORE_REMOVE, DELAY_AI_ACTION, RED

class GameEvents:
    """Класс для управления игровыми событиями и анимациями."""
    
    def __init__(self) -> None:
        """Инициализация событийного менеджера."""
        self.gui = None  # Будет установлен позже через GameEngine
        self.pending_removals: List[tuple[bool, int]] = []

    def set_gui(self, gui: 'GUI') -> None:
        """Устанавливает объект GUI после инициализации.

        Аргументы:
            gui (GUI): Объект графического интерфейса.
        """
        self.gui = gui

    def delay(self, milliseconds: int) -> None:
        """Создает задержку с обработкой событий Pygame."""
        pygame.time.wait(milliseconds)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def mark_dead_creature(self, creatures: List[Optional[Card]], slot: int, is_player: bool) -> None:
        """Помечает существо как убитое и добавляет его в список для удаления."""
        if creatures[slot] and creatures[slot].health <= 0:
            creatures[slot].active = False
            self.pending_removals.append((is_player, slot))

    def resolve_pending_removals(self, player_creatures: List[Optional[Card]], 
                               opponent_creatures: List[Optional[Card]]) -> None:
        """Обрабатывает отложенное удаление существ с задержкой и отрисовкой."""
        if self.pending_removals and self.gui:
            self.gui.draw_field()  # Перерисовываем поле
            pygame.display.flip()
            self.delay(DELAY_BEFORE_REMOVE)
            for is_player, slot in self.pending_removals:
                target = player_creatures if is_player else opponent_creatures
                if target[slot]:
                    print(f"{target[slot].name} удален с поля!")
                    target[slot] = None
            self.pending_removals.clear()

    def ai_action_delay(self) -> None:
        """Добавляет задержку перед действиями AI."""
        self.delay(DELAY_AI_ACTION)