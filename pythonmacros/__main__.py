import sys
from .main import main_loop


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        args.append("macros")
    main_loop(args)


if __name__ == "__main__":
    sys.exit(main())
