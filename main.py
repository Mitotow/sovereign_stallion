from core.game import Game
import argparse  # Module standard pour parser les arguments

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Activer le mode debug")
    args = parser.parse_args()

    game = Game((1280, 720), debug_mode=args.debug)
    game.run()
