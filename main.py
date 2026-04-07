from core.game import Game
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Activer le mode debug")
    parser.add_argument("--fullscreen", action="store_true", help="Activer le mode plein écran")
    parser.add_argument("--skip", action="store_true", help="Skip l'introduction et le premier menu")
    args = parser.parse_args()

    game = Game(debug_mode=args.debug, fullscreen=args.fullscreen, skip=args.skip)
    game.run()
