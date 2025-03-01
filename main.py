# main.py
from game.engine import GameEngine
from game.display import display_game_state, clear_console

def main() -> None:
    """Основная функция для запуска игры."""
    # Создаем игровой движок с именем игрока
    engine = GameEngine(player_name="Игрок 1")
    engine.start_game()

    while True:
        clear_console()
        display_game_state(engine)
        
        # Ввод команды от игрока
        action = input("\nДействие (play <row> <col> / next / quit): ").strip().lower()
        
        if action == "quit":
            print("Игра завершена!")
            break
        elif action == "next":
            engine.next_turn()
        elif action.startswith("play"):
            try:
                _, row, col = action.split()
                row, col = int(row), int(col)
                engine.play_card(row, col)
            except (ValueError, IndexError):
                print("Ошибка: Введите 'play <row> <col>', например 'play 0 1'")
        
        input("Нажмите Enter для продолжения...")

if __name__ == "__main__":
    main()