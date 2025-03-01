# game/core.py
from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class Card:
    """Класс для представления карты в игре."""
    name: str           # Название карты
    mana_cost: int      # Стоимость маны для использования
    attack: int         # Атака существа
    health: int         # Здоровье существа
    active: bool = False  # Активно ли существо для атаки (по умолчанию нет)

    def __str__(self) -> str:
        """Строковое представление карты для вывода"""
        return f"{self.name} (Мана: {self.mana_cost}, Атака: {self.attack}, HP: {self.health}, Активно: {self.active})"


@dataclass
class Player:
    """Класс для представления игрока."""
    name: str           # Имя игрока
    health: int = 30    # Начальное здоровье
    mana: int = 0       # Начальная мана

    def can_play_card(self, card: Card) -> bool:
        """Проверка, хватает ли маны для использования карты."""
        return self.mana >= card.mana_cost

    def spend_mana(self, card: Card) -> None:
        """Тратит ману на использование карты."""
        if self.can_play_card(card):
            self.mana -= card.mana_cost

    def take_damage(self, damage: int) -> None:
        """Уменьшает здоровье игрока."""
        self.health = max(0, self.health - damage)


@dataclass
class Opponent(Player):
    """Класс для представления оппонента (AI). Наследуется от Player."""
    def choose_card(self, grid: List[List[Optional[Card]]]) -> tuple[int, int]:
        """Выбор карты AI из своей зоны сетки (верхняя строка 8x1)."""
        from random import choice
        available = [(0, col) for col in range(8) if grid[0][col] and self.can_play_card(grid[0][col])]
        return choice(available) if available else (-1, -1)


class GameField:
    """Класс для представления игрового поля."""
    def __init__(self) -> None:
        self.grid: List[List[Optional[Card]]] = [[None for _ in range(8)] for _ in range(2)]
        self.player_creatures: List[Optional[Card]] = [None] * 8
        self.opponent_creatures: List[Optional[Card]] = [None] * 8

    def place_creature(self, card: Card, slot: int, is_player: bool) -> bool:
        """Размещает существо в указанный слот."""
        target = self.player_creatures if is_player else self.opponent_creatures
        if 0 <= slot < 8 and target[slot] is None:
            target[slot] = card
            return True
        return False

    def get_grid(self) -> List[List[Optional[Card]]]:
        """Возвращает текущую сетку карт."""
        return self.grid

    def get_creatures(self, is_player: bool) -> List[Optional[Card]]:
        """Возвращает список существ игрока или оппонента."""
        return self.player_creatures if is_player else self.opponent_creatures