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

def get_asn(prefix, filename):
    #for line in filename.readlines():
        ##print("Entering for-loop")
        ##print(f"{line=}")
        #list = line.split()
        #ip = list[0]
        ##print(f"{ip=}")
        #prefix_length = list[1]
        ##print(f"{prefix_length=}")
        #asn = list[2]
        ##print(f"{asn=}")
        #ip_with_prefix = ip + "/" + prefix_length

        #if prefix == ip_with_prefix:
            #return asn

    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            list = line.split()
            ip = list[0]
            prefix_length = list[1]
            asn = list[2]
            ip_with_prefix = ip + "/" + prefix_length

            if prefix == ip_with_prefix:
                return asn
    return 0

def read_non_aliased(tree, fh):
    return fill_tree(tree, fh)

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
    parser.add_argument("-n", "--non-aliased-file", required=True, type=argparse.FileType('r'), help="File containing non-aliased prefixes")
    parser.add_argument("-i", "--ip-address-file", required=True, type=argparse.FileType('r'), help="File containing IP addresses to be matched against (non-)aliased prefixes")
    parser.add_argument("-r", "--routeviews-file", required=True, help="File containing full RouteViews data")
    args = parser.parse_args()

    # Store aliased and non-aliased prefixes in a single subnet tree
    tree = SubnetTree.SubnetTree()

    # Read aliased and non-aliased prefixes
    tree = read_non_aliased(tree, args.non_aliased_file)

    # Read IP address file, match each address to longest prefix and print output
    for line in args.ip_address_file:
        line = line.strip()
        try:
            print(f"{str(get_asn(tree[line], args.routeviews_file))} {tree[line][-2:]} {line} {tree[line]}")
            #print(line + ", " + tree[line] + ", " + str(get_asn(line, args.routeviews_file)))
        except KeyError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)

if __name__ == "__main__":
    main()
