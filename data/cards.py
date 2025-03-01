from typing import List
from game.core import Card

def get_initial_grid() -> List[List[Card]]:
    """Создает статичную сетку карт 8x2.

    Возвращает:
        List[List[Card]]: Сетка 8x2 (верхняя строка — оппонент, нижняя — игрок).
    """
    # Карты для оппонента (верхняя строка, row 0)
    opponent_cards = [
        Card("Гоблин", mana_cost=1, attack=2, health=1),
        Card("Орк", mana_cost=2, attack=3, health=2),
        Card("Тролль", mana_cost=3, attack=4, health=3),
        Card("Дракон", mana_cost=4, attack=6, health=5),
        Card("Крыса", mana_cost=1, attack=1, health=1),
        Card("Волк", mana_cost=2, attack=2, health=3),
        Card("Медведь", mana_cost=3, attack=3, health=4),
        Card("Огр", mana_cost=4, attack=5, health=4),
    ]

    # Карты для игрока (нижняя строка, row 1)
    player_cards = [
        Card("Скелет", mana_cost=1, attack=1, health=2),
        Card("Зомби", mana_cost=2, attack=2, health=2),
        Card("Призрак", mana_cost=3, attack=3, health=1),
        Card("Вампир", mana_cost=4, attack=4, health=4),
        Card("Кот", mana_cost=1, attack=1, health=1),
        Card("Собака", mana_cost=2, attack=2, health=2),
        Card("Бык", mana_cost=3, attack=3, health=3),
        Card("Лев", mana_cost=4, attack=5, health=5),
    ]

    # Формируем сетку 8x2
    grid: List[List[Card]] = [opponent_cards, player_cards]
    return grid