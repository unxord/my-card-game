# game/engine.py
from typing import Optional
from game.core import Player, Opponent, Card, GameField
import copy
import random

class GameEngine:
    """Класс для управления логикой игры."""
    def __init__(self, player_name: str) -> None:
        self.player = Player(name=player_name)
        self.opponent = Opponent(name="AI")
        self.field = GameField()
        self.turn = 1

    def start_game(self) -> None:
        """Запускает игру, инициализируя поле."""
        from data.cards import get_initial_grid
        self.field.grid = get_initial_grid()
        # Удаляем вызов next_turn(), чтобы игрок начинал первым

    def next_turn(self) -> None:
        """Переход к следующему ходу."""
        self.turn += 1
        self.player.mana = min(self.turn, 10)
        self.opponent.mana = min(self.turn, 10)
        self.ai_turn()  # Ход AI после игрока
        self.resolve_combat()

    def play_card(self, row: int, col: int, slot: int, is_player: bool) -> Optional[Card]:
        """Разыгрывает карту из сетки в указанный слот."""
        if not (0 <= row < 2 and 0 <= col < 8 and 0 <= slot < 8):
            print("Ошибка: Неверные координаты!")
            return None

        card = self.field.grid[row][col]
        if card is None:
            print("Ошибка: Карта отсутствует!")
            return None

        player = self.player if is_player else self.opponent
        if player.can_play_card(card):
            player.spend_mana(card)
            card_copy = copy.deepcopy(card)
            if self.field.place_creature(card_copy, slot, is_player):
                print(f"{player.name} разыграл: {card_copy} в слот {slot}")
                return card_copy
            else:
                print(f"Слот {slot} занят!")
        else:
            print(f"{player.name}: Недостаточно маны для карты {card.name}!")
        return None

    def ai_turn(self) -> None:
        """Ход AI: разыгрывает карту с учетом состояния поля."""
        opponent_grid = self.field.grid[0]
        player_creatures = self.field.get_creatures(True)
        opponent_creatures = self.field.get_creatures(False)

        for slot in range(8):
            if opponent_creatures[slot] is None:
                best_card_idx = -1
                best_attack = -1
                for col, card in enumerate(opponent_grid):
                    if (self.opponent.can_play_card(card) and 
                        card.attack > best_attack and 
                        (player_creatures[slot] or random.random() > 0.3)):
                        best_card_idx = col
                        best_attack = card.attack
                
                if best_card_idx != -1:
                    self.play_card(0, best_card_idx, slot, is_player=False)
                    return

        print("AI пропускает ход: все слоты заняты или недостаточно маны.")

    def resolve_combat(self) -> None:
        """Разрешает бои между существами и урон по HP."""
        player_creatures = self.field.get_creatures(True)
        opponent_creatures = self.field.get_creatures(False)

        for slot in range(8):
            player_creature = player_creatures[slot]
            opponent_creature = opponent_creatures[slot]

            # Сохраняем начальные значения существ для проверки после боя
            player_alive = player_creature and player_creature.health > 0
            opponent_alive = opponent_creature and opponent_creature.health > 0

            # Если оба существа живы, они атакуют друг друга
            if player_alive and opponent_alive:
                player_creature.health -= opponent_creature.attack
                opponent_creature.health -= player_creature.attack
                print(f"Бой в слоте {slot}: {player_creature} vs {opponent_creature}")

            # Проверяем состояние после боя
            player_alive_after = player_creature and player_creature.health > 0
            opponent_alive_after = opponent_creature and opponent_creature.health > 0

            # Урон по HP только если одно существо выжило или изначально не было противника
            if player_alive_after and not opponent_alive:
                self.opponent.take_damage(player_creature.attack)
                print(f"{player_creature} атакует оппонента: HP {self.opponent.health}")
            elif opponent_alive_after and not player_alive:
                self.player.take_damage(opponent_creature.attack)
                print(f"{opponent_creature} атакует игрока: HP {self.player.health}")

            # Удаляем погибших существ
            if player_creature and player_creature.health <= 0:
                player_creatures[slot] = None
                print(f"{player_creature.name} погиб!")
            if opponent_creature and opponent_creature.health <= 0:
                opponent_creatures[slot] = None
                print(f"{opponent_creature.name} погиб!")

    def is_game_over(self) -> bool:
        """Проверяет, закончилась ли игра."""
        return self.player.health <= 0 or self.opponent.health <= 0