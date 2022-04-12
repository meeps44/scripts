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


# Ideally you'd only have to give the program the routeviews-file once,
# the program would then clean the routeviews-file, generate the list of addresses
# and create the tree based on that.
def main():
    parser = argparse.ArgumentParser()
    # Input files
    parser.add_argument("-n", "--non-aliased-file", required=True, type=argparse.FileType('r'), help="File containing non-aliased prefixes")
    parser.add_argument("-i", "--ip-address-file", required=True, type=argparse.FileType('r'), help="File containing IP addresses to be matched against (non-)aliased prefixes")
    parser.add_argument("-r", "--routeviews-file", required=True, help="File containing full RouteViews data")
    # Output files
    parser.add_argument("-h", "--hitlist-file", required=False, help="Output file to where the complete hitlist will be written")
    parser.add_argument("-k", "--keyvalue-file", required=False, help="Output file to where the asn-hitlist pair will be written")
    args = parser.parse_args()

    # Store aliased and non-aliased prefixes in a single subnet tree
    tree = SubnetTree.SubnetTree()

    # Read aliased and non-aliased prefixes
    tree = read_non_aliased(tree, args.non_aliased_file)

    unique_as_numbers = set()
    my_hitlist = {}
    my_hashmap = {}

    with open(args.routeviews_file, "r") as file:
        data = file.readlines()
        # Create hashmap (dictonary in python)
        for line in data:
            line = line.strip()
            line = line.split()
            key = line[0] + "/" + line[1]
            #print(f"{key=}")
            #print("Creating my_hashmap")
            my_hashmap[key] = line

    # Read IP address file, match each address to longest prefix and print output
    for ip_address in args.ip_address_file:
        ip_address = ip_address.strip()
        try:
            #asn = str(get_asn(tree[ip_address], data))
            longest_matching_prefix = tree[ip_address]
            #print(f"{longest_matching_prefix=}")
            #print(f"My_hashmap value: {my_hashmap[longest_matching_prefix]}")
            asn = my_hashmap[longest_matching_prefix]
            asn = asn[2]
            #print(f"{asn=}")
            #unique_as_numbers.add(asn)

            # Check if the prefix length is less than this line's prefix length
            if asn in my_hitlist:
                if my_hitlist[asn][-2:] < asn[1]:
                    my_hitlist[asn] = str(f"{ip_address}/{longest_matching_prefix[-2:]}")
            else:
                my_hitlist[asn] = str(f"{ip_address}/{longest_matching_prefix[-2:]}")

            # print(f"{asn} {longest_matching_prefix[-2:]} {ip_address} {longest_matching_prefix}")

        except KeyError as e:
            print("Skipped line '" + ip_address + "'", file=sys.stderr)
    
    # print all dictionary key-value pairs
    #print(my_hitlist)

    # print only the dictionary values
    with open(args.hitlist_file, "w") as file:
        #[print(value) for value in my_hitlist.values()]
        [file.write(value) for value in my_hitlist.values()]

if __name__ == "__main__":
    main()
