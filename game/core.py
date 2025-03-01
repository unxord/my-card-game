from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Card:
    """Класс для представления карты в игре."""
    name: str           # Название карты
    mana_cost: int      # Стоимость маны для использования
    attack: int         # Атака существа
    health: int         # Здоровье существа

    def __str__(self) -> str:
        """Строковое представление карты для вывода"""
        return f"{self.name} (Мана: {self.mana_cost}, Атака: {self.attack}, HP: {self.health})"


@dataclass
class Player:
    """Класс для представления игрока."""
    name: str           # Имя игрока
    health: int = 30    # Начальное здоровье
    mana: int = 0       # Начальная мана

    def can_play_card(self, card: Card) -> bool:
        """Проверка, хватает ли маны для использования карты.
        
        Аргументы:
            card (Card): Карта, которую хотят разыграть.
        Возвращает:
            bool: True, если мана позволяет, иначе False.
        """
        return self.mana >= card.mana_cost

    def spend_mana(self, card: Card) -> None:
        """Тратит ману на использование карты.
        
        Аргументы:
            card (Card): Карта, которую разыгрывают.
        """
        if self.can_play_card(card):
            self.mana -= card.mana_cost


class GameField:
    """Класс для представления игрового поля."""
    def __init__(self) -> None:
        # Сетка 4x4 для статичных карт (будет заполнена из data/cards.py)
        self.grid: List[List[Optional[Card]]] = [[None for _ in range(4)] for _ in range(4)]
        # Поле для размещенных существ
        self.creatures: List[Card] = []

    def place_creature(self, card: Card) -> None:
        """Размещает существо на поле.
        
        Аргументы:
            card (Card): Карта существа для размещения.
        """
        self.creatures.append(card)

    def get_grid(self) -> List[List[Optional[Card]]]:
        """Возвращает текущую сетку карт.
        
        Возвращает:
            List[List[Optional[Card]]]: Сетка 4x4.
        """
        return self.grid

    def get_creatures(self) -> List[Card]:
        """Возвращает список существ на поле.
        
        Возвращает:
            List[Card]: Список размещенных существ.
        """
        return self.creatures