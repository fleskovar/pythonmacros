import sys
from .main import main_loop


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    main_loop()


if __name__ == "__main__":
    sys.exit(main())
