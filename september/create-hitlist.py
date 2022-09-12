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

# Usage example:
# python3 create-hitlist.py -n <> -i <> -r <> -f hitlist.txt 

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
    # Input files
    parser.add_argument("-n", "--non-aliased-file", required=True, type=argparse.FileType('r'), \
        help="File containing non-aliased prefixes")
    parser.add_argument("-i", "--ip-address-file", required=True, type=argparse.FileType('r'), \
        help="List of IPv6-addresses (https://ipv6hitlist.github.io/) \
        to be matched against (non-)aliased prefixes")
    parser.add_argument("-r", "--routeviews-file", required=True, \
        help="File containing full RouteViews data")
    # Output files
    parser.add_argument("-f", "--hitlist-file", required=True, \
        help="Output file to where the complete hitlist will be written")
    parser.add_argument("-k", "--keyvalue-file", required=False, \
        help="Output file to where the asn-hitlist pair will be written")
    args = parser.parse_args()

    # Store aliased and non-aliased prefixes in a single subnet tree
    tree = SubnetTree.SubnetTree()
    # Read aliased and non-aliased prefixes
    tree = read_non_aliased(tree, args.non_aliased_file)

    unique_as_numbers = set()
    hitlist_dict = {}
    ipaddress_asn_map = {}

    with open(args.routeviews_file, 'r') as file:
        data = file.readlines()
        # Create key-value dictionary
        for line in data:
            line = line.strip()
            line = line.split()
            key = line[0] + "/" + line[1]
            #print(f"{key=}")
            #print("Creating ipaddress_asn_map")
            ipaddress_asn_map[key] = line

    # Read IP address file, match each address to longest prefix and write output to file
    for ip_address in args.ip_address_file:
        ip_address = ip_address.strip()
        try:
            #asn = str(get_asn(tree[ip_address], data))
            longest_matching_prefix = tree[ip_address]
            #print(f"{longest_matching_prefix=}")
            #print(f"ipaddress_asn_map value: {my_hashmap[longest_matching_prefix]}")
            asn = ipaddress_asn_map[longest_matching_prefix]
            asn = asn[2]
            #print(f"{asn=}")
            #unique_as_numbers.add(asn)

            # Check if the prefix length is less than this line's prefix length
            if asn in hitlist_dict:
                if hitlist_dict[asn][-2:] < asn[1]:
                    hitlist_dict[asn] = str(f"{ip_address}/{longest_matching_prefix[-2:]}")
            else:
                hitlist_dict[asn] = str(f"{ip_address}/{longest_matching_prefix[-2:]}")

            # print(f"{asn} {longest_matching_prefix[-2:]} {ip_address} {longest_matching_prefix}")
        except KeyError as e:
            print("Skipped line '" + ip_address + "'", file=sys.stderr)
    
    # Write all key-value pairs
    with open(args.keyvalue_file, 'w') as file:
        print(hitlist_dict)

    # Write only the dictionary values
    with open(args.hitlist_file, 'w') as file:
        [file.write(value + "\n") for value in hitlist_dict.values()]

if __name__ == "__main__":
    main()
