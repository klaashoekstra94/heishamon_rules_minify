import sys
from argparse import ArgumentParser

from .minifier import Minifier


def main_cli():
    parser = ArgumentParser()
    parser.add_argument("input", help="input rules file")
    parser.add_argument("output", help="output rules file")
    parser.add_argument("-p", "--print", action="store_true", help="print the output on the commandline")
    parser.add_argument("-c", "--comments_only", action="store_true", help="only remove comments from the input")
    args = parser.parse_args()

    with open(args.input, "r") as i:
        text = Minifier.minify(i.read(), args.comments_only)

    with open(args.output, "w") as o:
        o.write(text)

    if args.print:
        print(text)

    return 0


if __name__ == "__main__":
    sys.exit(main_cli())
