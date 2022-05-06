#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys

try:
    import SubnetTree
except Exception as e:
    print(e, file=sys.stderr)
    print("Use `pip install pysubnettree` to install the required module", file=sys.stderr)
    sys.exit(1)

def create_hashmap(rv_file):
    my_hashmap = {}
    with open(rv_file, "r") as file:
        data = file.readlines()
        # Create hashmap (python dictonary)
        for line in data:
            line = line.strip()
            line = line.split()
            key = line[0] + "/" + line[1]
            my_hashmap[key] = line[2]
    return my_hashmap

def get_asn(prefix, my_hashmap):
    asn = 0
    try:
        return my_hashmap[prefix]
    except KeyError as e:
        print(f"KeyError: prefix {prefix} not found in hashmap", file=sys.stderr)
    return asn

def fill_tree(tree, fh):
    for line in fh:
        line = line.strip()
        try:
            tree[line] = line
        except ValueError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)
    return tree


def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument("-n", "--non-aliased-file", required=True, type=argparse.FileType('r'), help="File containing non-aliased RouteViews prefixes")
    parser.add_argument("-a", "--aliased-file", required=True, type=argparse.FileType('r'), help="File containing aliased RouteViews prefixes")
    parser.add_argument("-i", "--ip-address-file", required=True, type=argparse.FileType('r'), help="File containing IP addresses to be matched against RouteViews prefixes")
    parser.add_argument("-r", "--routeviews-file", required=True, type=argparse.FileType('r'), help="File containing full RouteViews data")
    args = parser.parse_args()

    # Store aliased and non-aliased prefixes in a single subnet tree
    tree = SubnetTree.SubnetTree()

    # Read aliased and non-aliased prefixes
    tree = fill_tree(tree, args.aliased_file)
    my_hashmap = create_hashmap(str(args.routeviews_file))

    # Read IP address file, match each address to longest prefix and print output
    for line in args.ip_address_file:
        line = line.strip()
        try:
            print(f"{get_asn(tree[line], my_hashmap)}{line},{tree[line]}")
        except KeyError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)

if __name__ == "__main__":
    main()
