from typing import List
from game.core import Card

def get_initial_grid() -> List[List[Card]]:
    """Создает статичную сетку карт 4x4.

    Возвращает:
        List[List[Card]]: Сетка 4x4 с предопределенными картами.
    """
    # Пример статичных карт для сетки
    cards = [
        Card("Гоблин", mana_cost=1, attack=2, health=1),
        Card("Орк", mana_cost=2, attack=3, health=2),
        Card("Тролль", mana_cost=3, attack=4, health=3),
        Card("Дракон", mana_cost=4, attack=6, health=5),
        Card("Крыса", mana_cost=1, attack=1, health=1),
        Card("Волк", mana_cost=2, attack=2, health=3),
        Card("Медведь", mana_cost=3, attack=3, health=4),
        Card("Огр", mana_cost=4, attack=5, health=4),
        Card("Скелет", mana_cost=1, attack=1, health=2),
        Card("Зомби", mana_cost=2, attack=2, health=2),
        Card("Призрак", mana_cost=3, attack=3, health=1),
        Card("Вампир", mana_cost=4, attack=4, health=4),
        Card("Кот", mana_cost=1, attack=1, health=1),
        Card("Собака", mana_cost=2, attack=2, health=2),
        Card("Бык", mana_cost=3, attack=3, health=3),
        Card("Лев", mana_cost=4, attack=5, health=5),
    ]

    # Формируем сетку 4x4 из списка карт
    grid: List[List[Card]] = []
    for i in range(0, 16, 4):
        grid.append(cards[i:i + 4])
    
    return grid