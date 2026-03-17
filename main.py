from core.game import Game
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Activer le mode debug")
    parser.add_argument("--fullscreen", action="store_true", help="Activer le mode plein écran")
    args = parser.parse_args()

    game = Game((1280, 720), debug_mode=args.debug, fullscreen=args.fullscreen)
    game.run()
