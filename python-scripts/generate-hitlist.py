#!/usr/bin/env python

# Generates an IPv6 hitlist based on a list of RouteViews prefixes and the 
# list of responsive IPv6-addresses from https://ipv6hitlist.github.io/.
# The end result is a list containing one responsive address per ASN.
# Final format: <responsive ip> <prefix length> <asn>
# Example: 600:6001:110b::1	48	11351

from __future__ import print_function
from pathlib import Path

import argparse
import sys

try:
    import SubnetTree
except Exception as e:
    print(e, file=sys.stderr)
    print("Use `pip install pysubnettree` to install the required module", file=sys.stderr)
    sys.exit(1)


def fill_tree(tree, fh):
    for line in fh:
        line = line.strip()
        try:
            tree[line] = line
        except ValueError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)
    return tree

# gets the asn from an IP prefix
def get_asn(prefix):
    asn = 0
    return asn



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix-file", required=True, type=argparse.FileType('r'), help="File containing list of RouteViews prefixes")
    parser.add_argument("-i", "--ip-address-file", required=True, type=argparse.FileType('r'), help="File containing IP addresses to be matched against (non-)aliased prefixes")
    args = parser.parse_args()

    tree = SubnetTree.SubnetTree()
    tree = fill_tree(tree, args.prefix_file)

    # Set up outputfile
    # filename = f"{str(Path.home())}/python-programming/subnettree-output.txt"

    # Read IP address file, match each address to longest prefix and print output
    for line in args.ip_address_file:
        line = line.strip()
        try:
            print(line + "," + tree[line] + "," + get_asn(tree[line]))
            #file.write(line + "," + tree[line])
        except KeyError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)

if __name__ == "__main__":
    main()
