#!/usr/bin/env python

# Usage example: python3 asnlookup.py -i=ip_addresses_short.txt -r=routeviews-rv6-20220411-1200.pfx2as.txt

from __future__ import print_function

import argparse
import sys

try:
    import SubnetTree
except Exception as e:
    print(e, file=sys.stderr)
    print("Use `pip install pysubnettree` to install the required module", file=sys.stderr)
    sys.exit(1)

def create_hashmap(tree, rv_file):
    for line in rv_file:
        line = line.strip()
        line = line.split()
        key = line[0] + "/" + line[1]
        try:
            tree[key] = line[2]
        except ValueError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)
    return tree

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip-address-file", required=True, type=argparse.FileType('r'), help="File containing IP addresses to be matched against RouteViews prefixes")
    parser.add_argument("-r", "--routeviews-file", required=True, type=argparse.FileType('r'), help="File containing full RouteViews data")
    args = parser.parse_args()

    tree = SubnetTree.SubnetTree()
    tree = create_hashmap(tree, args.routeviews_file)

    # Read IP address file, match each address to longest prefix and print output
    for line in args.ip_address_file:
        line = line.strip()
        try:
            print(f"ASN: {tree[line]}")
        except KeyError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)

if __name__ == "__main__":
    main()
