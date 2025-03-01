from game.engine import GameEngine
from game.gui import GUI

def main() -> None:
    """Основная функция для запуска игры."""
    engine = GameEngine(player_name="Игрок 1")
    gui = GUI(engine)
    gui.run()

if __name__ == "__main__":
    main()