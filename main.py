# Main.py

from dwarfgame import DwarfGame

if __name__ == "__main__":
    game = DwarfGame()

    try:
        game.Run()

    except KeyboardInterrupt:
        print("Game interrupted")
        quit()
