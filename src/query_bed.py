"""Tool for cleaning up a BED file."""

import argparse  # we use this module for option parsing. See main for details.
import math
import sys
from sort_bed import sort_file
from bed import (read_bed_file, print_line, BedLine)


def extract_region(features, start: int, end: int):
    """Extract region chrom[start:end] and write it to outfile."""
    
    # Binary search:
    hi, lo = len(features), 0
    match = None
    B = 0 
    while lo < hi and B == 0:
        mid = (lo + hi) // 2
        if start <= features[mid][1] < end:
            match = mid
            B=1
        elif start > features[mid][1]:
            lo = mid + 1
        else:
            hi = mid

    positions = []
    upstream = []
    downstream = []
    if match != None:
        k=0
        while match-k >= 0:
            if start <= features[match-k][1] < end:  # or start <= features[match-k][2] < end:?
                upstream.append(features[match-k])
            k+=1
        k=1
        while match+k <= len(features)-1:
            if start <= features[match+k][1] < end:  # or start <= features[match+k][2] < end:?
                downstream.append(features[match+k])
            k+=1
        positions = upstream[::-1]
        positions.extend(downstream)
    return positions


def main() -> None:
    """Run the program."""
    # Setting up the option parsing using the argparse module
    argparser = argparse.ArgumentParser(
        description="Extract regions from a BED file")
    argparser.add_argument('bed', type=argparse.FileType('r'))
    argparser.add_argument('query', type=argparse.FileType('r'))

    # 'outfile' is either provided as a file name or we use stdout
    argparser.add_argument('-o', '--outfile',  # use an option to specify this
                            metavar='output',  # name used in help text
                            type=argparse.FileType('w'),  # file for writing
                            default=sys.stdout)

    # Parse options and put them in the table args
    args = argparser.parse_args()

    # With all the options handled, we just need to do the real work
    table = read_bed_file(args.bed)
    sort_file(table)

    for query in args.query:
        chrom, start, end = query.split()
        # Extract the region from the chromosome, using your extract_region()
        # function. If you did your job well, this should give us the features
        # that we want.
        region = extract_region(table.get_chrom(chrom), int(start), int(end))
        for line in region:
            print_line(line, args.outfile)


if __name__ == '__main__':
    main()
