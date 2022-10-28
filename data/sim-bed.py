"""Script for generating a random BED file."""

import argparse
from random import randint


def main() -> None:
    """Run the script."""
    argparser = argparse.ArgumentParser(
        description="Simulate a random BED file")

    argparser.add_argument('-n', '--no-chrom',
                           help="number of chromosomes to simulate",
                           metavar='N', type=int, default=5)
    argparser.add_argument('-l', '--length',
                           help="the length of the chromosomes",
                           metavar='L', type=int, default=1000)
    argparser.add_argument('-m', '--lines',
                           help="number of lines in the output",
                           metavar='M', type=int, default=1000)

    args = argparser.parse_args()

    for feature in range(args.lines):
        chrom = f"chrom{randint(0,args.no_chrom)}"
        start = randint(0, args.length)
        print(chrom, start, start + 1, f"Feature-{feature}", sep='\t')


if __name__ == '__main__':
    main()
