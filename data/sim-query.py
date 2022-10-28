"""Script for generating a random query file."""

import argparse
from random import randint


def main() -> None:
    """Run the script."""
    argparser = argparse.ArgumentParser(
        description="Simulate a random query file")

    argparser.add_argument('-n', '--no-chrom',
                           help="number of chromosomes to simulate",
                           metavar='N', type=int, default=5)
    argparser.add_argument('-l', '--length',
                           help="the length of the chromosomes",
                           metavar='L', type=int, default=1000)
    argparser.add_argument('-m', '--lines',
                           help="number of lines in the output",
                           metavar='M', type=int, default=50)

    args = argparser.parse_args()

    for _ in range(args.lines):
        chrom = f"chrom{randint(0,args.no_chrom)}"
        start = randint(0, args.length)
        end = randint(start, args.length)
        print(chrom, start, end, sep='\t')


if __name__ == '__main__':
    main()
