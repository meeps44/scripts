#!/usr/bin/env python

# gets all AS numbers from a routeviews-file and writes
# them to a file

from __future__ import print_function
import argparse

def get_asnumbers(filename):
    as_numbers = {}
    for line in filename:
        list = line.split()
        ip = list[0]
        prefix_length = list[1]
        asn = list[2]
        as_numbers.add(asn)
    return as_numbers

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--routeviews-file", required=True, type=argparse.FileType('r'), help="File containing RouteViews data")
    parser.add_argument("-o", "--output-file", required=True, help="File we want to write the output to")
    args = parser.parse_args()
    asns = get_asnumbers(args.routeviews_file)

    with open(args.output_file, "w") as file:
        file.write(asns)


if __name__ == "__main__":
    main()
