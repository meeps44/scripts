#!/usr/bin/env python

# gets one "active" IP per AS from RouteViews and https://ipv6hitlist.github.io/ data
# example usage: python3 generate-hitlist.py -a=routeviews_prefixes.txt -i=responsive-addresses.txt -r=routeviews-rv6-20220411-1200.pfx2as.txt > hitlist.txt

from __future__ import print_function

import argparse
import sys

try:
    import SubnetTree
except Exception as e:
    print(e, file=sys.stderr)
    print("Use `pip install pysubnettree` to install the required module", file=sys.stderr)
    sys.exit(1)

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
    parser.add_argument("-a", "--aliased-file", required=True, type=argparse.FileType('r'), help="File containing RouteViews prefixes")
    parser.add_argument("-i", "--ip-address-file", required=True, type=argparse.FileType('r'), help="File containing IP addresses to be matched against RouteViews prefixes")
    parser.add_argument("-r", "--routeviews-file", required=True, help="File containing full RouteViews data")
    args = parser.parse_args()

    as_numbers = set()

    # Store aliased and non-aliased prefixes in a single subnet tree
    tree = SubnetTree.SubnetTree()

    # Read aliased and non-aliased prefixes
    tree = fill_tree(tree, args.aliased_file)

    #my_hashmap = create_hashmap(args.routeviews_file)
    my_hashmap = {}
    with open(args.routeviews_file, "r") as file:
        data = file.readlines()
        # Create hashmap (python dictonary)
        for line in data:
            line = line.strip()
            line = line.split()
            key = line[0] + "/" + line[1]
            my_hashmap[key] = line[2]

    # Read IP address file, match each address to longest prefix and print output
    for line in args.ip_address_file:
        line = line.strip()
        try:
            prefix = tree[line]
            tmp_asn = get_asn(prefix, my_hashmap) 
            if tmp_asn not in as_numbers:
                as_numbers.add(tmp_asn)
                #print(f"{get_asn(prefix, my_hashmap)},{line},{prefix}") # if you want to print the corresponding AS-number and prefix as well
                print(f"{line}")
        except KeyError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)

if __name__ == "__main__":
    main()
