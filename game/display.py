from typing import List, Optional
from game.core import Card, GameField, Player

def display_game_state(engine: 'GameEngine') -> None:
    """Отображает текущее состояние игры в консоли.

    Аргументы:
        engine (GameEngine): Экземпляр игрового движка.
    """
    print(f"\n=== Состояние игры (Игрок: {engine.player.name}) ===")
    print(f"Ход: {engine.turn} | Мана: {engine.player.mana} | HP: {engine.player.health}")
    
    # Отображение сетки карт 4x4
    print("\nСетка карт (4x4):")
    grid = engine.field.get_grid()
    for row in grid:
        row_display = [str(card) if card else "Пусто" for card in row]
        print(" | ".join(row_display))
    
    # Отображение поля с существами
    print("\nПоле существ:")
    creatures = engine.field.get_creatures()
    if creatures:
        for creature in creatures:
            print(f" - {creature}")
    else:
        print("Поле пусто")

def clear_console() -> None:
    """Очищает консоль (работает на Windows)."""
    import os
    os.system('cls')  # Для Windows 10