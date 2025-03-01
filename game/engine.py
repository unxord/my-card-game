from typing import Optional
from game.core import Player, Card, GameField
import copy  # Добавляем для создания копий карт

class GameEngine:
    """Класс для управления логикой игры."""
    def __init__(self, player_name: str) -> None:
        """Инициализация игрового движка.

        Аргументы:
            player_name (str): Имя игрока.
        """
        self.player = Player(name=player_name)
        self.field = GameField()
        self.turn = 0  # Счетчик ходов

    def start_game(self) -> None:
        """Запускает игру, инициализируя поле."""
        from data.cards import get_initial_grid
        self.field.grid = get_initial_grid()
        self.next_turn()

    def next_turn(self) -> None:
        """Переход к следующему ходу."""
        self.turn += 1
        self.player.mana += 1  # Увеличение маны на +1 каждый ход
        print(f"Ход {self.turn}. Мана: {self.player.mana}, HP: {self.player.health}")

    def play_card(self, row: int, col: int) -> Optional[Card]:
        """Разыгрывает карту из сетки на поле.

        Аргументы:
            row (int): Номер строки в сетке (0-3).
            col (int): Номер столбца в сетке (0-3).
        Возвращает:
            Optional[Card]: Карта, если успешно разыграна, иначе None.
        """
        if not (0 <= row < 4 and 0 <= col < 4):
            print("Ошибка: Неверные координаты!")
            return None

        card = self.field.grid[row][col]
        if card is None:  # На случай, если в будущем сетка будет содержать пустые ячейки
            print("Ошибка: Карта отсутствует!")
            return None

        if self.player.can_play_card(card):
            self.player.spend_mana(card)
            # Создаем копию карты, чтобы оригинал остался в сетке
            card_copy = copy.deepcopy(card)
            self.field.place_creature(card_copy)
            print(f"Разыграна карта: {card_copy}")
            return card_copy
        else:
            print(f"Недостаточно маны для карты {card.name}!")
            return None