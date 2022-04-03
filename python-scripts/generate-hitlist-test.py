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

    tuple_list = []
    hitlist = []

    for line in args.ip_address_file:
        line = line.strip()
        try:
            asn = get_asn(tree[line])

            print(line + "," + tree[line] + "," + asn)

            # save the prefix & asn as a tuple
            tup = (tree[line], asn)

            # add the tuple to a list
            tuple_list.append(tup)
            
            # get the last 2 characters (the prefix length)
            last_chars = tree[line][-2:]
            
            # if the prefix length is greater than the one that already exists for this (prefix - tuple)-pair,
            # and the ASNs are equal
            # replace the item in the list
            for item in tuple_list:
                # tuple structure: (prefix, asn)
                if tup[1] == item[1] and tup[0][-2:] < last_chars:
                    hitlist.append(line)
        except KeyError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)

if __name__ == "__main__":
    main()