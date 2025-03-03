# game/engine.py
from typing import Optional
from game.core import Player, Opponent, Card, GameField
from game.events import GameEvents
from data.config import DELAY_BETWEEN_ACTIONS, DELAY_AI_ACTION

import copy
import random

class GameEngine:
    """Класс для управления логикой игры."""
    def __init__(self, player_name: str) -> None:
        self.player = Player(name=player_name)
        self.opponent = Opponent(name="AI")
        self.field = GameField()
        self.turn = 1
        self.opponent_turn = 0
        self.events = GameEvents()

    def set_gui(self, gui: 'GUI') -> None:
        """Устанавливает GUI для событий.

        Аргументы:
            gui (GUI): Объект графического интерфейса.
        """
        self.events.set_gui(gui)

    def start_game(self) -> None:
        """Запускает игру, инициализируя поле."""
        from data.cards import get_initial_grid
        self.field.grid = get_initial_grid()
        self.player.mana = min(self.turn, 10)
        self.opponent.mana = 0

    def next_turn(self) -> None:
        """Ход игрока: действия, атака активных, активация для следующего хода, передача хода AI."""
        self.turn += 1
        self.player.mana = min(self.turn, 10)
        self.resolve_combat(is_player_turn=True)
        for creature in self.field.get_creatures(True):
            if creature:
                creature.active = True
        self.events.delay(DELAY_BETWEEN_ACTIONS)
        self.ai_turn()

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
            card_copy.active = False
            if self.field.place_creature(card_copy, slot, is_player):
                print(f"{player.name} разыграл: {card_copy} в слот {slot}")
                return card_copy
            else:
                print(f"Слот {slot} занят!")
        else:
            print(f"{player.name}: Недостаточно маны для карты {card.name}!")
        return None

    def ai_turn(self) -> None:
        """Ход AI: действия, атака активных, активация для следующего хода."""
        self.opponent_turn += 1
        self.opponent.mana = min(self.opponent_turn, 10)

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
                    self.events.ai_action_delay()
                    self.play_card(0, best_card_idx, slot, is_player=False)
                    break

        self.resolve_combat(is_player_turn=False)
        for creature in self.field.get_creatures(False):
            if creature:
                creature.active = True
        self.events.delay(DELAY_AI_ACTION)  # Задержка после хода AI

    def resolve_combat(self, is_player_turn: bool) -> None:
        """Разрешает бои между существами и урон по HP с задержками."""
        player_creatures = self.field.get_creatures(True)
        opponent_creatures = self.field.get_creatures(False)
        attacking_creatures = player_creatures if is_player_turn else opponent_creatures
        defending_creatures = opponent_creatures if is_player_turn else player_creatures
        defender = self.opponent if is_player_turn else self.player

        for slot in range(8):
            attacker = attacking_creatures[slot]
            defender_creature = defending_creatures[slot]

            attacker_alive = attacker and attacker.health > 0
            defender_alive = defender_creature and defender_creature.health > 0

            if attacker_alive and attacker.active:
                self.events.delay(DELAY_BETWEEN_ACTIONS)
                if defender_alive:
                    defender_creature.health -= attacker.attack
                    print(f"{attacker} атакует {defender_creature}")
                    attacker.health -= defender_creature.attack
                    print(f"{defender_creature} контратакует {attacker}")
                else:
                    defender.take_damage(attacker.attack)
                    print(f"{attacker} атакует {defender.name}: HP {defender.health}")

            self.events.mark_dead_creature(attacking_creatures, slot, is_player=is_player_turn)
            self.events.mark_dead_creature(defending_creatures, slot, is_player=not is_player_turn)

        self.events.resolve_pending_removals(player_creatures, opponent_creatures)

    def is_game_over(self) -> bool:
        """Проверяет, закончилась ли игра."""
        return self.player.health <= 0 or self.opponent.health <= 0