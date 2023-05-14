#!/usr/bin/env python
from __future__ import print_function
import json
import argparse
import sys
try:
    import SubnetTree
except Exception as e:
    print(e, file=sys.stderr)
    print("Use `pip install pysubnettree` to install the required module", file=sys.stderr)
    sys.exit(1)

# Usage example:
# python3 create-hitlist.py -n <> -i <> -r <> -f hitlist.txt


# def read_non_aliased(tree, fh):
    # return fill_tree(tree, fh)


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
    # Input files
    # parser.add_argument("-n", "--non-aliased-file", required=True, type=argparse.FileType('r'),
    # help="File containing non-aliased prefixes")
    parser.add_argument("-i", "--ip-address-file", required=True, type=argparse.FileType('r'),
                        help="List of IPv6-addresses (https://ipv6hitlist.github.io/) \
        to be matched against non-aliased prefixes")
    parser.add_argument("-r", "--routeviews-file", required=True,
                        help="File containing RouteViews prefix2as data")
    # Output files
    parser.add_argument("-f", "--hitlist-file", required=True,
                        help="Output file to where the complete hitlist will be written")
    parser.add_argument("-k", "--keyvalue-file", required=False,
                        help="Output file to where the asn-hitlist pair will be written")
    args = parser.parse_args()

    # Store aliased and non-aliased prefixes in a single subnet tree
    # Create subnet tree consisting of all prefixes in RouteViews prefix2as dataset
    tree = SubnetTree.SubnetTree()
    with open(args.routeviews_file, 'r') as file:
        data = file.readlines()

        # TODO: strip ASN and add just the prefixes to list
        prefixes = list()
        for line in data:
            line = line.strip()
            line = line.split()
            rv_prefix = line[0] + "/" + line[1]
            prefixes.append(rv_prefix)
        # Fill tree with routeviews data
        tree = fill_tree(tree, prefixes)

    # Read aliased and non-aliased prefixes
    #tree = read_non_aliased(tree, args.non_aliased_file)

    hitlist_dict = {}
    ipaddress_asn_map = {}

    with open(args.routeviews_file, 'r') as file:
        data = file.readlines()
        # Create key-value dictionary
        for line in data:
            line = line.strip()
            line = line.split()
            key = line[0] + "/" + line[1]
            # print(f"{key=}")
            #print("Creating ipaddress_asn_map")
            ipaddress_asn_map[key] = line

    # Read input IP-address file and perform ASN-lookup on each IP-address.
    # Save the result as a python-dictionary where each ASN is a key and the
    # IP-address is the value.
    for ip_address in args.ip_address_file:
        ip_address = ip_address.strip()
        try:
            longest_matching_prefix = tree[ip_address]
            asn = ipaddress_asn_map[longest_matching_prefix][2]

            # Check if the prefix length is less than this line's prefix length
            if asn in hitlist_dict:
                if hitlist_dict[asn][-2:] < asn[1]:
                    hitlist_dict[asn] = str(
                        f"{ip_address}/{longest_matching_prefix[-2:]}")
            else:
                hitlist_dict[asn] = str(
                    f"{ip_address}/{longest_matching_prefix[-2:]}")
        except KeyError as e:
            print("Skipped line '" + ip_address + "'", file=sys.stderr)

    # Output ASN-IPaddress pairs to file in JSON-format:
    with open(args.keyvalue_file, 'w') as file:
        json.dump(hitlist_dict, file)

    # Output only IP-addresses to file:
    with open(args.hitlist_file, 'w') as file:
        [file.write(value + "\n") for value in hitlist_dict.values()]


if __name__ == "__main__":
    main()
