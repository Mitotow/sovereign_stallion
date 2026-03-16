import getopt
from sys import argv
from core.game import Game


def main():
    options = "d:"
    long_options = ["debug"]
    debug_mode = False

    try:
        args, values = getopt.getopt(argv[:1], options, long_options)
        for currentArg, currentVal in args:
            if currentArg in ("-d", "--debug"):
                debug_mode = True
    except getopt.error as err:
        print(str(err))

    game = Game((1280, 720), debug_mode=True)
    game.setup()
    game.run()


if __name__ == "__main__":
    main()
