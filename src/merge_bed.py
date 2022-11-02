"""Tool for cleaning up a BED file."""

import argparse  # we use this module for option parsing. See main for details.
import sys
from typing import TextIO
from bed import (parse_line, print_line, BedLine, Table)


def read_bed_file(f: TextIO):
    """Read an entire sorted bed file."""
    # Handle first line...
    line = f.readline()
    if not line:
        return []

    res = [parse_line(line)]
    for line in f:
        feature = parse_line(line)
        prev_feature = res[-1]
        assert prev_feature.chrom < feature.chrom or \
            (prev_feature.chrom == feature.chrom and
             prev_feature.chrom_start <= feature.chrom_start), \
            "Input files must be sorted"
        res.append(feature)

    return res


def merge(f1, f2, outfile: TextIO):
    """Merge features and write them to outfile."""
    j = 0
    for i in range(len(f1)):
        if f1[i][0] == f2[j][0] and f1[i][1] >= f2[j][1] and f1[i+1][1] <= f2[j][1]:
            f1.insert(i, f2[j])
            j+=1
            

def main():
    """Run the program."""
    # Setting up the option parsing using the argparse module
    argparser = argparse.ArgumentParser(description="Merge two BED files")
    argparser.add_argument('f1', type=argparse.FileType('r'))
    argparser.add_argument('f2', type=argparse.FileType('r'))
    argparser.add_argument('-o', '--outfile',  # use an option to specify this
                           metavar='output',   # name used in help text
                           type=argparse.FileType('w'),  # file for writing
                           default=sys.stdout)

    # Parse options and put them in the table args
    args = argparser.parse_args()

    # With all the options handled, we just need to do the real work
    features1 = read_bed_file(args.f1)
    features2 = read_bed_file(args.f2)
    merge(features1, features2, args.outfile)


if __name__ == '__main__':
    main()
