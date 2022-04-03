from __future__ import print_function
from pathlib import Path

import argparse
import sys
import SubnetTree

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
    path = "/mnt/c/Users/Erlend/Downloads/RouteViews data/"
    filename = "routeviews-rv6-20220312-2200-short.txt" 
    full = path + filename
    with open(full, "r") as file:
        lines = file.readlines()
        for line in lines:
            list = line.split()
            ip = list[0]
            prefix_length = list[1]
            ip_with_prefix = ip + "/" + prefix_length
            asn = list[2]

            if prefix == ip_with_prefix:
                return asn
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix-file", required=True, type=argparse.FileType('r'), help="File containing list of RouteViews prefixes")
    parser.add_argument("-i", "--ip-address-file", required=True, type=argparse.FileType('r'), help="File containing IP addresses to be matched against (non-)aliased prefixes")
    args = parser.parse_args()

    tree = SubnetTree.SubnetTree()
    tree = SubnetTree.fill_tree(tree, args.prefix_file)

    for line in args.ip_address_file:
        line = line.strip()
        try:
            print(line + "," + tree[line] + "," + get_asn(tree[line]))
        except KeyError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)

if __name__ == "__main__":
    main()